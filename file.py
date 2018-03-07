#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import atexit
import datetime
import itertools
import json
import logging
import random
import signal
import sys
import sqlite3
import time
import requests
from fake_useragent import UserAgent

class InstaBot:
    database_name = "follows_db.db"
    follows_db = None
    follows_db_c = None

    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_likes = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'
    api_user_detail = 'https://i.instagram.com/api/v1/users/%s/info/'

    user_agent = "" ""
    accept_language = 'en-US,en;q=0.5'

    # If instagram ban you - query return 400 error.
    error_400 = 0
    # If you have 3 400 error in row - looks like you banned.
    error_400_to_ban = 3
    # If InstaBot think you are banned - going to sleep.
    ban_sleep_time = 2 * 60 * 60

    # All counter.
    bot_mode = 0
    like_counter = 0
    follow_counter = 0
    unfollow_counter = 0
    comments_counter = 0
    current_user = 'hajka'
    current_index = 0
    current_id = 'abcds'
    # List of user_id, that bot follow
    bot_follow_list = []
    user_info_list = []
    user_list = []
    ex_user_list = []
    unwanted_username_list = []
    is_checked = False
    is_selebgram = False
    is_fake_account = False
    is_active_user = False
    is_following = False
    is_follower = False
    is_rejected = False
    is_self_checking = False
    is_by_tag = False
    is_follower_number = 0

    self_following = 0
    self_follower = 0

    # Log setting.
    logging.basicConfig(filename='errors.log', level=logging.INFO)
    log_file_path = ''
    log_file = 0

    # Other.
    user_id = 0
    media_by_tag = 0
    media_on_feed = []
    media_by_user = []
    login_status = False

    # Running Times
    start_at_h = 0,
    start_at_m = 0,
    end_at_h = 23,
    end_at_m = 59,

    # For new_auto_mod
    next_iteration = {"Like": 0, "Follow": 0, "Unfollow": 0, "Comments": 0}

    def __init__(self,
                 login,
                 password,
                 like_per_day=1000,
                 media_max_like=50,
                 media_min_like=0,
                 follow_per_day=0,
                 follow_time=5 * 60 * 60,
                 unfollow_per_day=0,
                 start_at_h=0,
                 start_at_m=0,
                 end_at_h=23,
                 end_at_m=59,
                 database_name='follows_db.db',
                 max_like_for_one_tag=5,
                 unfollow_break_min=15,
                 unfollow_break_max=30,
                 log_mod=0,
                 proxy=""):

        self.database_name = database_name
        self.follows_db = sqlite3.connect(database_name, timeout=0, isolation_level=None)
        self.follows_db_c = self.follows_db.cursor()
        fake_ua = UserAgent()
        self.user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
        self.bot_start = datetime.datetime.now()
        self.start_at_h = start_at_h
        self.start_at_m = start_at_m
        self.end_at_h = end_at_h
        self.end_at_m = end_at_m
        self.unfollow_break_min = unfollow_break_min
        self.unfollow_break_max = unfollow_break_max

        self.time_in_day = 24 * 60 * 60
        # Like
        self.like_per_day = like_per_day
        if self.like_per_day != 0:
            self.like_delay = self.time_in_day / self.like_per_day

        # Follow
        self.follow_time = follow_time
        self.follow_per_day = follow_per_day
        if self.follow_per_day != 0:
            self.follow_delay = self.time_in_day / self.follow_per_day

        # Unfollow
        self.unfollow_per_day = unfollow_per_day
        if self.unfollow_per_day != 0:
            self.unfollow_delay = self.time_in_day / self.unfollow_per_day

        # Don't like if media have more than n likes.
        self.media_max_like = media_max_like
        # Don't like if media have less than n likes.
        self.media_min_like = media_min_like
        # Auto mod seting:
        # Default list of tag.
        # Get random tag, from tag_list, and like (1 to n) times.
        self.max_like_for_one_tag = max_like_for_one_tag
        # log_mod 0 to console, 1 to file
        self.log_mod = log_mod
        self.s = requests.Session()
        # if you need proxy make something like this:
        # self.s.proxies = {"https" : "http://proxyip:proxyport"}
        # by @ageorgios
        if proxy != "":
            proxies = {
                'http': 'http://' + proxy,
                'https': 'http://' + proxy,
            }
            self.s.proxies.update(proxies)
        # convert login to lower
        self.user_login = login.lower()
        self.user_password = password
        self.bot_mode = 0
        self.media_by_tag = []
        self.media_on_feed = []
        self.media_by_user = []
        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.2.0 started at %s:' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        self.login()


    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.user_login)
        self.login_post = {
            'username': self.user_login,
            'password': self.user_password
        }

        self.s.headers.update({
            'Accept': '*/*',
            'Accept-Language': self.accept_language,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Content-Length': '0',
            'Host': 'www.instagram.com',
            'Origin': 'https://www.instagram.com',
            'Referer': 'https://www.instagram.com/',
            'User-Agent': self.user_agent,
            'X-Instagram-AJAX': '1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'XMLHttpRequest'
        })

        r = self.s.get(self.url)
        self.s.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
        time.sleep(5 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True)
        print('Login', login.json())
        self.s.headers.update({'X-CSRFToken': login.cookies['csrftoken']})
        self.csrftoken = login.cookies['csrftoken']
        #ig_vw=1536; ig_pr=1.25; ig_vh=772;  ig_or=landscape-primary;
        self.s.cookies['ig_vw'] = '1536'
        self.s.cookies['ig_pr'] = '1.25'
        self.s.cookies['ig_vh'] = '772'
        self.s.cookies['ig_or'] = 'landscape-primary'
        time.sleep(5 * random.random())

        if login.status_code == 200:
            r = self.s.get('https://www.instagram.com/')
            finder = r.text.find(self.user_login)
            if finder != -1:
                self.login_status = True
                print('%s login success!' % self.user_login)
                try:print(r.text)
                except: print('cant print')
            else:
                self.login_status = False
                print('Login error! Check your login data!')
        else:
            print('Login error! Connection error!')

    def logout(self):
        now_time = datetime.datetime.now()
        log_string = 'Logout: likes - %i, follow - %i, unfollow - %i, comments - %i.' % \
                     (self.like_counter, self.follow_counter,
                      self.unfollow_counter, self.comments_counter)
        print(log_string)
        work_time = datetime.datetime.now() - self.bot_start
        log_string = 'Bot work time: %s' % (work_time)
        print(log_string)

        try:
            logout_post = {'csrfmiddlewaretoken': self.csrftoken}
            logout = self.s.post(self.url_logout, data=logout_post)
            print("Logout success!")
            try: print('json', logout.json())
            except: print(logout.content)
            self.login_status = False

        except:
            logging.exception("Logout error!")


    def unlike(self, media_id):
        """ Send http request to unlike media by ID """
        if self.login_status:
            url_unlike = self.url_unlike % (media_id)
            try:
                unlike = self.s.post(url_unlike)
            except:
                logging.exception("Except on unlike!")
                unlike = 0
            return unlike

    def comment(self, media_id, comment_text):
        """ Send http request to comment """
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % (media_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    self.comments_counter += 1
                    log_string = 'Write: "%s". #%i.' % (comment_text,
                                                        self.comments_counter)
                return comment
            except:
                logging.exception("Except on comment!")
        return False

    def follow(self, user_id):
        """ Send http request to follow """
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                username = self.get_username_by_user_id(user_id=user_id)
                return follow
            except:
                pass
        return False

    def get_username_by_user_id(self, user_id):
        """ Get username by user_id """
        if self.login_status:
            try:
                url_info = self.api_user_detail % user_id
                r = self.s.get(url_info, headers="")
                all_data = json.loads(r.text)
                username = all_data["user"]["username"]
                return username
            except:
                return False
        else:
            return False

    def unfollow(self, user_id):
        """ Send http request to unfollow """
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    self.unfollow_counter += 1
                return unfollow
            except:
                logging.exception("Exept on unfollow!")
        return False

if __name__ =='__main__':
    bot = InstaBot('pkemey', '6Foo**kwargs')
    bot.login()
    print(' = = '*10000)
    bot.logout()
    print('finished')


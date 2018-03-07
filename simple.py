#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import
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

class GetInfo(object):
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    logging.basicConfig(filename='errors.log', level=logging.INFO)
    login_status = False
    accept_language = 'en-US,en;q=0.5'
    url = 'https://www.instagram.com/'
    url_tag = 'https://www.instagram.com/explore/tags/%s/?__a=1'
    url_like = 'https://www.instagram.com/web/likes/%s/like/'
    url_unlike = 'https://www.instagram.com/web/likes/%s/unlike/'
    url_comment = 'https://www.instagram.com/web/comments/%s/add/'
    url_follow = 'https://www.instagram.com/web/friendships/%s/follow/'
    url_unfollow = 'https://www.instagram.com/web/friendships/%s/unfollow/'
    url_login = 'https://www.instagram.com/accounts/login/ajax/'
    url_logout = 'https://www.instagram.com/accounts/logout/'
    url_media_detail = 'https://www.instagram.com/p/%s/?__a=1'
    url_user_detail = 'https://www.instagram.com/%s/?__a=1'
    api_user_detail = 'https://i.instagram.com/api/v1/users/%s/info/'
    database_name = "follows_db.db"
    follows_db = None
    follows_db_c = None

    def __init__(self, username, password):
        self.username = username.lower()
        self.password = password
        self.s = requests.Session()
        now_time = datetime.datetime.now()
        log_string = '\n\nGetInfo v1.2.0 started at %s:\n' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        logging.info(log_string)
        self.login()

    def login(self):
        log_string = 'Trying to login as %s...' % (self.username)
        logging.info(log_string)
        self.login_post = {
            'username': self.username,
            'password': self.password
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
        time.sleep(4 * random.random())
        login = self.s.post(
            self.url_login, data=self.login_post, allow_redirects=True, timeout=10)
        try:
            log_string = json.dumps(login.json())
        except:
            log_string = 'Login responded with {0}'.format(login.status_code)
        logging.info(log_string)
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
            finder = r.text.find(self.username)
            if finder != -1:
                self.login_status = True
                log_string = '%s login success!' % self.username
            else:
                self.login_status = False
                log_string = 'Login error! Check your login data!'
            logging.debug(log_string)
        else:
            logging.WARNING('Login error! Connection error!')

    def __tag_posts__(self, url):
        logging.info('Fetching posts for the hastag')
        if not self.login_post:
            logging.info('Not authenticated hence cant fetch homepage')
            return 'error', False
        logging.info('Was authenticated')
        responce = self.s.get(url, timeout=100)
        if responce.status_code == 200:
            r = json.loads(responce.content.decode())
            logging.info('Successfully fetched {0}'.format(url))
            return r, True
            self.s.headers['']
        return 'Failed with status code {0}'.format(responce.status_code), False

    def get_top_post(self, tag):
        data, success = self.__tag_posts__(self.url_tag % tag)
        if success:
            logging.info('Trying to process the posts for the hastag')
            edges = data['graphql']['hashtag']['edge_hashtag_to_media']['edges']
            edges += data['graphql']['hashtag']['edge_hashtag_to_top_posts']['edges']

            full = []
            unique = set()
            for post in edges:
                node = post['node']
                item = {}
                item['id'] = node['id']
                item['shortcode'] = node['shortcode']
                item['comments'] = node['edge_media_to_comment']['count']
                item['likes'] = node['edge_liked_by']['count']
                time_stamp = node['taken_at_timestamp']
                item['timestamp'] = datetime.datetime.fromtimestamp(time_stamp).isoformat()
                item['owner_id'] = node['owner']['id']
                item['image'] = node['display_url']
                try:
                    item['caption'] = node['edge_media_to_caption']['edges'][0]['node']['text']
                except:
                    item['caption'] = None

                if item['id'] in unique:
                    continue
                full.append(item)
            logging.info('successfully processed and returned {0} items'.format(len(full)))
            return full, True

        logging.info('Trying to get posts for %s and it was not successfull' % (tag))
        return 'An error occured when getting posts', False

    def get_tag_posts_to_like(self, tag,  min_likes=50, max_likes=100):
        posts, success = self.get_top_post(tag)
        if success:
            likeable = []
            for item in posts:
                if item['likes'] >= min_likes and item['likes'] >= max_likes:
                    likeable.append(item['id'])
            logging.info('Items satisfying conditions of liking the posts are %s' % (json.dumps(likeable)))
            return likeable, True

        return posts, success

    def like(self, post_id):
        logging.info('Trying to like post id %s' % post_id)
        if self.login_status:
            url_like = self.url_like % (post_id)
            try:
                liked = self.s.post(url_like)
                logging.info("Success")
            except:
                logging.exception("Except on like!")
                liked = 0
            print(liked)
            return liked
        return False

    def unlike(self, post_id):
        logging.info('Trying to unlike post id %s' % post_id)
        if self.login_status:
            url_unlike = self.url_unlike % (post_id)
            try:
                unlike = self.s.post(url_unlike)
                logging.info(json.dumps(unlike.content))
            except:
                logging.exception("Except on unlike!")
                unlike = 0
            return unlike
        return False

    def comment(self, post_id, comment_text):
        logging.info('Trying to comment post id %s' % post_id)
        if self.login_status:
            comment_post = {'comment_text': comment_text}
            url_comment = self.url_comment % (post_id)
            try:
                comment = self.s.post(url_comment, data=comment_post)
                if comment.status_code == 200:
                    logging.info('Success')
                return comment
            except:
                logging.exception("Except on comment!")
        return False

    def follow(self, user_id):
        logging.info('Trying to follow user id %s' % user_id)
        if self.login_status:
            url_follow = self.url_follow % (user_id)
            try:
                follow = self.s.post(url_follow)
                username = self.get_username_by_user_id(user_id=user_id)
                print(username)
                return follow
            except:
                pass
            logging.error('Failed')
        return False

    def get_username_by_user_id(self, user_id):
        logging.info('Trying to get username of user id %s' % user_id)
        if self.login_status:
            try:
                url_info = self.api_user_detail % user_id
                r = self.s.get(url_info, headers="")
                all_data = json.loads(r.text)
                username = all_data["user"]["username"]
                logging.info('Success')
                return username
            except:
                logging.error('Error')
                return False
        else:
            return False

    def unfollow(self, user_id):
        logging.info('Trying to get username of user id %s' % user_id)
        if self.login_status:
            url_unfollow = self.url_unfollow % (user_id)
            try:
                unfollow = self.s.post(url_unfollow)
                if unfollow.status_code == 200:
                    logging.info('Successfully unfollowed')
                return unfollow
            except:
                logging.exception("Exept on unfollow!")
        return False

if __name__ == '__main__':
    bot = GetInfo('pkemey', '6Foo**kwargs')
    # likeable, success = bot.get_tag_posts_to_like('mombasarally', min_likes=2, max_likes=200)
    # id = 3062814478
    # bot.unfollow(id)
    # if success:
    #     print(bot.s.headers)
    #     for post in likeable:
    #         print('Am liking %s' % post)
    #         l = bot.like(post)
    #         print(l)
    #         time.sleep(5*random.random())


headers = {
    'authority': 'www.instagram.com',
    'method': 'POST',
    'path': '/web/likes/1495824916354940003/like/',
    'scheme': 'https',
    'accept': '*/*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'content-length': '0',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://www.instagram.com',
    'referer': 'https://www.instagram.com/p/BTCPNYRg7xj/?taken-at=7092025',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36',
    'x-csrftoken': 'WV4tEaI0nNOKWmWxZwIYzXt0qGf1N8sI',
    'x-instagram-ajax': '1',
    'x-requested-with': 'XMLHttpRequest',
}





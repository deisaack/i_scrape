from __future__ import absolute_import
import requests
import os
import logging
import time
import datetime
import random
import json

class GetInfo:
    user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
    logging.basicConfig(filename='errors.log', level=logging.INFO)
    login_status = False
    accept_language = 'en-US,en;q=0.5'
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

    def __int__(self, username, password):
        self.username = username.lower()
        self.password = password.lower()
        self.s = requests.Session()
        now_time = datetime.datetime.now()
        log_string = 'Instabot v1.2.0 started at %s:\n' % \
                     (now_time.strftime("%d.%m.%Y %H:%M"))
        logging.info(log_string)
        self.login()

    def login(self):
        log_string = 'Trying to login as %s...\n' % (self.username)
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
        logging.debug(log_string)
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

if __name__ =='__main__':
    GetInfo('pkemey', '6Foo**kwargs')












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


if __name__ == '__main__':
    GetInfo('pkemey', '6Foo**kwargs')












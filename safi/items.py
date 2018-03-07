# -*- coding: utf-8 -*-

import scrapy
from newsfeeds.apps.fees.models import Post
from scrapy_djangoitem import DjangoItem


class PostItem(DjangoItem):
    django_model = Post


class User(scrapy.Item):
    username = scrapy.Field()
    posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    description = scrapy.Field()


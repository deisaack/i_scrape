# -*- coding: utf-8 -*-

import scrapy


class Post(scrapy.Item):
    id = scrapy.Field()
    shortcode = scrapy.Field()
    comments = scrapy.Field()
    likes = scrapy.Field()
    timestamp = scrapy.Field()
    owner_id = scrapy.Field()
    tags = scrapy.Field()
    caption = scrapy.Field()
    image = scrapy.Field()


class User(scrapy.Item):
    username = scrapy.Field()
    posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    description = scrapy.Field()


# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SafiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class User(scrapy.Item):
    username = scrapy.Field()
    posts = scrapy.Field()
    followers = scrapy.Field()
    following = scrapy.Field()
    description = scrapy.Field()

class Post(scrapy.Item):
    photo = scrapy.Field()
    tags = scrapy.Field()
    imageset = scrapy.Field()
    url = scrapy.Field()

# -*- coding: utf-8 -*-
from scrapy import signals
import os, sys
import django
import json
from collections import OrderedDict

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsfeeds.settings")
# sys.path.insert(0, os.path.abspath(os.path.join(BASE_DIR, os.pardir)))
#
# script_path = os.path.dirname(__file__)
# django.setup()

from scrapy.exceptions import DropItem
from newsfeeds.apps.fees.models import Post


class DuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()
        self.file = open('duplicate.jl', 'w')

    def process_item(self, item, spider):
        if item['id'] in self.ids_seen:
            line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
            self.file.write(line)
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['id'])
            return item


class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('data.json', 'w')
        self.file.write('[')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + ",\n"
        self.file.write(line)
        # del post['id']
        # del post['shortcode']
        # obj = Post.objects.create(
        #     id = post.pop('id'),  shortcode = post('shortcode'),
        #     defaults=post
        # )
        # obj.save()
        return item

    def close_spider(self, spider):
        self.file.write(']\n\n')
        self.file.close()

# -*- coding: utf-8 -*-

from scrapy import signals


import json
import codecs
from collections import OrderedDict
from scrapy.exceptions import DropItem

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
        return item

    def close_spider(self, spider):
        self.file.write(']\n\n')
        self.file.close()


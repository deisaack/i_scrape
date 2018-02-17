# -*- coding: utf-8 -*-

from scrapy import signals


import json
import codecs
from collections import OrderedDict

class SafiPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'a', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(OrderedDict(item), ensure_ascii=False, sort_keys=False) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        self.file.write('\n\n')
        self.file.close()




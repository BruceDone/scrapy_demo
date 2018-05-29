# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from .signals import ITEM_ERROR


class CnblogsPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.process_error_item, signal=ITEM_ERROR)
        return s

    def process_item(self, item, spider):
        if 'error' in item.get('result', ''):
            spider.crawler.signals.send_catch_log(signal=ITEM_ERROR, item=item, spider=spider)

        return item

    def process_error_item(self, item, spider):
        print 'get the error item'
        raise DropItem('i do not need the error item')

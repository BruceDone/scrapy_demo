# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
import json
import os

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request


class DoubanImgDownloadPipeline(ImagesPipeline):
    default_headers = {
        'accept': 'image/webp,image/*,*/*;q=0.8',
        'accept-encoding': 'gzip, deflate, sdch, br',
        'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'cookie': 'bid=yQdC/AzTaCw',
        'referer': 'https://www.douban.com/photos/photo/2370443040/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            self.default_headers['referer'] = image_url
            yield Request(image_url, headers=self.default_headers)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]

        if not image_paths:
            raise DropItem("Item contains no images")

        item['image_paths'] = image_paths
        item['download_time'] = time.time()

        return item


class DoubanItemPipeline():

    def __init__(self, images_store):
        self.images_store = images_store
        self.file_name = os.path.join(images_store, str(int(time.time())) + '.txt')
        self.handler = open(self.file_name, 'w')

    def process_item(self, item, spider):
        self.handler.write(json.dumps(dict(item)) + '\n')

        return item

    def close_spider(self, spider):
        self.handler.close()

    @classmethod
    def from_crawler(cls, crawler):
        images_store = crawler.settings.get('IMAGES_STORE')
        if not images_store:
            raise ValueError("not find the images_store, please check")

        return cls(
            images_store=images_store
        )

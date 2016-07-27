# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from settings import MONGODB


class GoogleplayPipeline(object):
    def __init__(self):
        self._db = MONGODB.get('db')
        self._collection = MONGODB.get('collection')
        self._host = MONGODB.get('host')
        self._port = MONGODB.get('port')
        self._client = pymongo \
            .MongoClient(host=self._host, port=self._port) \
            .get_database(self._db) \
            .get_collection(self._collection)

    def process_item(self, item, spider):
        self._client.create_index([('id', pymongo.DESCENDING)], background=True)
        self._client.update_one(filter={'app_id': item['app_id']}, update={'$set': dict(item)}, upsert=True)
        # self._client.save(dict(item))
        return item

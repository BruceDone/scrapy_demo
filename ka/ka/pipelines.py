# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.serialize import ScrapyJSONEncoder

from kafka.client import SimpleClient
from kafka.producer import SimpleProducer


class KaPipeline(object):
    def process_item(self, item, spider):
        return item


class KafkaPipeline(object):
    """
    Publishes a serialized item into a Kafka topic
    :param producer: The Kafka producer
    :type producer: kafka.producer.Producer
    :param topic: The Kafka topic being used
    :type topic: str or unicode
    """

    def __init__(self, producer, topic):
        """
        :type producer: kafka.producer.Producer
        :type topic: str or unicode
        """
        self.producer = producer
        self.topic = topic

        self.encoder = ScrapyJSONEncoder()

    def process_item(self, item, spider):
        """
        Overriden method to process the item
        :param item: Item being passed
        :type item: scrapy.item.Item
        :param spider: The current spider being used
        :type spider: scrapy.spider.Spider
        """
        # put spider name in item
        item = dict(item)
        item['spider'] = spider.name
        msg = self.encoder.encode(item)
        self.producer.send_messages(self.topic, msg)

    @classmethod
    def from_settings(cls, settings):
        """
        :param settings: the current Scrapy settings
        :type settings: scrapy.settings.Settings
        :rtype: A :class:`~KafkaPipeline` instance
        """
        k_hosts = settings.get('SCRAPY_KAFKA_HOSTS', 'localhost:9092')
        topic = settings.get('SCRAPY_KAFKA_ITEM_PIPELINE_TOPIC', 'scrapy_kafka_item')
        client = SimpleClient(k_hosts)
        producer = SimpleProducer(client)
        return cls(producer, topic)

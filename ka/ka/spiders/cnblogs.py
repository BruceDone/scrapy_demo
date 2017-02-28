# -*- coding: utf-8 -*-
import scrapy
from scrapy import signals
from scrapy.exceptions import DontCloseSpider
from scrapy.spider import Spider
from .. import items
from kafka.client import KafkaClient, SimpleClient
from kafka.consumer import SimpleConsumer
from scrapy.log import logger


class ListeningKafkaSpider(Spider):
    """
    Spider that reads urls from a kafka topic when idle.
    This spider will exit only if stopped, otherwise it keeps
    listening to messages on the given topic
    Specify the topic to listen to by setting the spider's `kafka_topic`.
    Messages are assumed to be URLS, one by message. To do custom
    processing of kafka messages, override the spider's `process_kafka_message`
    method
    """

    """
    Mixin class to implement reading urls from a kafka queue.
    :type kafka_topic: str
    """
    kafka_topic = None

    def process_kafka_message(self, message):
        """"
        Tell this spider how to extract urls from a kafka message
        :param message: A Kafka message object
        :type message: kafka.common.OffsetAndMessage
        :rtype: str or None
        """
        if not message:
            return None

        return message.message.value

    def setup_kafka(self, settings):
        """Setup redis connection and idle signal.
        This should be called after the spider has set its crawler object.
        :param settings: The current Scrapy settings being used
        :type settings: scrapy.settings.Settings
        """
        if not hasattr(self, 'topic') or not self.topic:
            self.topic = '%s-starturls' % self.name

        hosts = settings.get('SCRAPY_KAFKA_HOSTS', 'localhost:9092')
        consumer_group = settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP', 'scrapy-kafka')
        _kafka = SimpleClient(hosts)
        # wait at most 1sec for more messages. Otherwise continue
        self.consumer = SimpleConsumer(_kafka, consumer_group, self.topic,
                                       auto_commit=True, iter_timeout=1.0)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from kafka topic
        self.crawler.signals.connect(self.spider_idle, signal=signals.spider_idle)
        self.crawler.signals.connect(self.item_scraped, signal=signals.item_scraped)
        logger.info("Reading URLs from kafka topic '%s'" % self.kafka_topic)

    def next_request(self):
        """
        Returns a request to be scheduled.
        :rtype: str or None
        """
        message = self.consumer.get_message(True)
        url = self.process_kafka_message(message)
        if not url:
            return None
        return self.make_requests_from_url(url)

    def schedule_next_request(self):
        """Schedules a request if available"""
        req = self.next_request()
        if req:
            self.crawler.engine.crawl(req, spider=self)

    def spider_idle(self):
        """Schedules a request if available, otherwise waits."""
        self.schedule_next_request()
        raise DontCloseSpider

    def item_scraped(self, *args, **kwargs):
        """Avoids waiting for the spider to  idle before scheduling the next request"""
        self.schedule_next_request()

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(ListeningKafkaSpider, cls).from_crawler(crawler, *args, **kwargs)

        if not hasattr(spider, 'topic') or not spider.topic:
            spider.topic = '%s-starturls' % spider.name

        hosts = crawler.settings.get('SCRAPY_KAFKA_HOSTS', 'localhost:9092')
        consumer_group = crawler.settings.get('SCRAPY_KAFKA_SPIDER_CONSUMER_GROUP', 'scrapy-kafka')
        _kafka = SimpleClient(hosts)
        # wait at most 1sec for more messages. Otherwise continue
        spider.consumer = SimpleConsumer(_kafka, consumer_group, spider.topic,
                                         auto_commit=True, iter_timeout=1.0)
        # idle signal is called when the spider has no requests left,
        # that's when we will schedule new requests from kafka topic
        crawler.signals.connect(spider.spider_idle, signal=signals.spider_idle)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        logger.info("Reading URLs from kafka topic '%s'" % spider.kafka_topic)

        return spider


class CnblogsSpider(ListeningKafkaSpider):
    name = "cnblogs"
    allowed_domains = ["cnblogs.com"]

    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):
        for p in response.xpath('//a/@href').extract()[2:]:
            item = items.KaItem()
            url = response.urljoin(p)

            item['link'] = url
            item['title'] = ''.join(response.xpath('//title/text()').extract())

            yield item
            break

# -*- coding: utf-8 -*-
import scrapy


class BlogsSpider(scrapy.Spider):
    name = 'blogs'
    allowed_domains = ['cnblogs.com']
    start_urls = ['https://www.cnblogs.com/']

    def parse(self, response):
        print 'get response'
        pass

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GoogleplayItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    app_id = scrapy.Field()
    app_name = scrapy.Field()
    url = scrapy.Field()
    mail = scrapy.Field()
    company_name = scrapy.Field()
    rating_count = scrapy.Field()
    download_count = scrapy.Field()


class GoogleItem(scrapy.Item):
    url = scrapy.Field()
    mail = scrapy.Field()
    company_name = scrapy.Field()

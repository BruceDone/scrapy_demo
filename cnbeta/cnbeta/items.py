# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class CnbetaItem(scrapy.Item):
    # define the fields for your item here like:
    catid = Field()
    comments = Field()
    counter = Field()
    mview = Field()
    rate_sum = Field()
    source =Field()
    score = Field()
    score_story = Field()
    thumb =Field()
    topic = Field()
    inputtime = Field()
    hometext = Field()
    title = Field()
    url_show = Field()
    crawled_datetime = Field()

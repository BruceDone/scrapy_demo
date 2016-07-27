# -*- coding: utf-8 -*-

from scrapy.spider import CrawlSpider,Rule
from scrapy.contrib.linkextractors import LinkExtractor
from GooglePlay.items import GoogleplayItem
import logging

class GoogleSpider(CrawlSpider):
    name = "google"
    allowed_domains = ["play.google.com"]
    start_urls = [
        'https://play.google.com/store',
        'https://play.google.com/store/apps/category/GAME/collection/topselling_free',
        'https://play.google.com/store/apps/details?id=com.viber.voip'
    ]

    rules = [
        Rule(LinkExtractor(allow=("https://play\.google\.com/store/apps/details", )), callback='parse_app',follow=True),
    ] #  CrawlSpider 会根据 rules 规则爬取页面并调用函数进行处理


    def parse_app(self, response):
        # 在这里只获取页面的 URL 以及下载数量
        item = GoogleplayItem()
        item['url'] = response.url

        app_id = response.url.split('=')[-1]
        if app_id:
            item['app_id'] = app_id
        else:
            item['app_id'] = ''

        rate_count = response.xpath('//span[@class="rating-count"]/text()')
        if rate_count:
            rate_count = rate_count.extract()[0].replace(',')
            item['rating_count'] = rate_count

        app_name_div = response.xpath('//div[@class="id-app-title"]/text()')
        if not app_name_div:
            logging.error(msg='not find the app name')
            return
        item['app_name'] = app_name_div.extract()[0].strip()

        mail_a = response.xpath('//div[@class="content contains-text-link"]/a[2]/@href')
        if not mail_a:
            return

        mail_text = mail_a.extract()[0]
        if 'mailto:' in mail_text:
            mail_text = mail_text.replace('mailto:','')
        item['mail'] = mail_text

        company_name_span = response.xpath('//span[@itemprop="name"]/text()')
        if company_name_span:
           item['company_name'] = company_name_span.extract()[0]

        download_count = response.xpath('//div[@itemprop="numDownloads"]/text()')
        if download_count:
            item['download_count'] = download_count.extract()[0]
        else:
            item['download_count'] = '0'

        yield item
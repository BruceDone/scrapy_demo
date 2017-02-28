# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from .. import settings
from scrapy.log import logger
import json
from .. import items
from datetime import datetime


class Cnbeta(scrapy.Spider):
    name = "cnbeta"

    allowed_domains = ["cnbeta.com"]

    url_template = 'http://www.cnbeta.com/home/more?&type=all&page={page}&_csrf=TXBQSUNmV24rPz0PCgMNQ3Q4BC0tMGckeyc8ACRLBBl8N30fGyIHBA%3D%3D&_=1488269056276'

    default_headers = {
        'Accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'BDTUJIAID=eb405c44ccb88e6987c8ad1d4042a13a; _gat=1; bfd_g=8a7bc81f66bd068d00003d73000602395673aaf2; _ga=GA1.2.1861316168.1451968385; Hm_lvt_4216c57ef1855492a9281acd553f8a6e=1455950219; Hm_lpvt_4216c57ef1855492a9281acd553f8a6e=1455950225; tmc=2.208385984.24805108.1455950219294.1455950219294.1455950224798; tma=208385984.88585069.1451968386004.1451968386004.1455950219299.2; tmd=3.208385984.88585069.1451968386004.; bfd_s=208385984.91899638.1455950219291; csrf_token=28d4f7ca7334939614cc2ccd33fa52dc5deb32aa; PHPSESSID=q403ddla7aqcl41j5trst60n34',
        'Host': 'www.cnbeta.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.cnbeta.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    start_urls = [
         url_template.format(page=x) for x in xrange(1, settings.MAX_PAGE_COUNT)
        ]

    def start_requests(self):
        for p in self.start_urls:
            yield Request(url=p, headers=self.default_headers, callback=self.parse)

    def parse(self, response):

        if not response.body:
            logger.error(msg='there is no response body ,please go and check it ')
            return

        json_object = json.loads(response.body_as_unicode())
        if not json_object:
            logger.error(msg='there is no json object')
            return

        result = json_object.get('result', None)
        if not result:
            return

        item_list = result.get('list')
        if not items:
            return

        for tmp_item in item_list:
            item = items.CnbetaItem()
            item['catid'] = tmp_item.get('catid', None)
            item['comments'] = tmp_item.get('comments', None)
            item['counter'] = tmp_item.get('counter', None)
            item['mview'] = tmp_item.get('mview', None)
            item['rate_sum'] = tmp_item.get('rate_sum', None)
            item['source'] = tmp_item.get('source', None)
            item['score'] = tmp_item.get('score', None)
            item['thumb'] = tmp_item.get('thumb', None)
            item['topic'] = tmp_item.get('topic', None)
            item['inputtime'] = tmp_item.get('inputtime', None)
            item['hometext'] = tmp_item.get('hometext', None)
            item['title'] = tmp_item.get('title', None)
            item['url_show'] = 'http://www.cnbeta.com' + tmp_item.get('url_show', '')
            item['crawled_datetime'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            yield item

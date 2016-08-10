# coding=utf-8
from scrapy.spiders import Spider
import re
from scrapy import Request
from douban_imgs.items import DoubanImgsItem


class download_douban(Spider):
    name = 'download_douban'

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    }

    def __init__(self, url='152686895', *args, **kwargs):
        self.allowed_domains = ['douban.com']
        self.start_urls = [
            'http://www.douban.com/photos/album/%s/' % (url)]
        # call the father base function
        self.url = url
        super(download_douban, self).__init__(*args, **kwargs)

    def start_requests(self):

        for url in self.start_urls:
            yield Request(url=url, headers=self.default_headers, callback=self.parse)

    def parse(self, response):
        list_imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src').extract()
        if list_imgs:
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            yield item

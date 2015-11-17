# coding=utf-8
from scrapy.spiders import Spider
import re
from douban_imgs.items import DoubanImgsItem
from scrapy.http.request import Request


# please pay attention to the encoding of info,otherwise raise error
import sys

reload(sys)

sys.setdefaultencoding('utf8')


class download_douban(Spider):
    name = 'download_douban'

    def __init__(self, url='152686895', *args, **kwargs):
        self.allowed_domains = ['douban.com']
        self.start_urls = [
            'http://www.douban.com/photos/album/%s/' % (url)]
        # call the father base function
        self.url = url
        super(download_douban, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        :type response: response infomation
        """
        list_imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src').extract()
        if list_imgs:
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            yield item

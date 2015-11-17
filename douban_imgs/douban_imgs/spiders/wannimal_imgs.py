# coding=utf-8
from scrapy.spiders import Spider
import re
from douban_imgs.items import DoubanImgsItem
from scrapy.http.request import Request

# please pay attention to the encoding of info,otherwise raise error
import sys

reload(sys)

sys.setdefaultencoding('utf8')


class Wannimal_Imgs(Spider):
    name = 'wannimal_imgs'

    def __init__(self, tag='wanimal1983', *args, **kwargs):
        self.allowed_domains = ['tumblr.com']
        self.start_urls = [
            'http://%s.tumblr.com/' % (tag)]
        # call the father base function
        self.tag = tag
        super(Wannimal_Imgs, self).__init__(*args, **kwargs)

    def parse(self, response):
        """
        :type response: response infomation
        """
        list_imgs = response.xpath('//div[@class="content"]//img/@src').extract()
        if list_imgs:
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            yield item

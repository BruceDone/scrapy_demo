# coding=utf-8
from scrapy.spiders import Spider
import re
from scrapy import Request
from ..items import DoubanImgsItem


class Douban(Spider):
    name = 'douban'

    default_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
        'Cache-Control': 'no-cache',
        'Cookie': 'll="118282"; bid=UptK4kDEzj0; ue="cnhacker499@163.com"; gr_user_id=72bc77c5-d8e3-400e-abd3-5833aae9f885; ap=1; _vwo_uuid_v2=F7FF3E3B4FF64E68D5236A13BA96204A|4dfe5cca086f3d59f4b36a85ed3a90b7; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1488266010%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D_DuWJ5rsiaxCIdv1pj1hT7ytR63fdl15ChB0apCmpGvCevamdZ5Ws3V2tBVh_tiI%26wd%3D%26eqid%3Dd372c3980001d16800000006589b21d9%22%5D; _pk_id.100001.8cb4=e321643b0837abd0.1480306554.80.1488266010.1487570926.; _pk_ses.100001.8cb4=*',
        'Host': 'www.douban.com',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    }

    def __init__(self, url='152686895', *args, **kwargs):
        self.allowed_domains = ['douban.com']
        self.start_urls = [
            'https://www.douban.com/photos/album/%s/' % (url)]
        self.url = url
        super(Douban, self).__init__(*args, **kwargs)

    def start_requests(self):

        for url in self.start_urls:
            yield Request(url=url, headers=self.default_headers, callback=self.parse)

    def parse(self, response):

        list_imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src').extract()

        if list_imgs:
            item = DoubanImgsItem()
            item['image_urls'] = list_imgs
            yield item

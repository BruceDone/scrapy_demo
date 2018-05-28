# -*- coding: utf-8 -*-
import scrapy


class DoubanImgOssSpider(scrapy.Spider):
    name = 'douban_img_oss'
    allowed_domains = ['douban.com']
    start_urls = ['https://www.douban.com/photos/album/57756464/']

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'bid=FyYqXADVlZw; _pk_id.100001.8cb4=87c25eac992a186a.1527238453.1.1527238453.1527238453.; _pk_ses.100001.8cb4=*; __utma=30149280.343087314.1527238454.1527238454.1527238454.1; __utmc=30149280; __utmz=30149280.1527238454.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=30149280.1.10.1527238454',
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    }

    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(url=u, headers=self.headers, callback=self.parse)

    def parse(self, response):
        if not response.body:
            self.logger.warning(
                'can not find any response from current request {}'.format(response.request.url))
            return

        imgs = response.xpath('//div[@class="photolst clearfix"]//img/@src')
        if not imgs:
            self.logger.error('can not find any imgs')
            return

        imgs_url = imgs.extract()
        if not imgs_url:
            self.logger.error('can not find any url')
            return

        for url in imgs_url:
            # transfer the webp to jpg
            if 'webp' in url:
                url = url.replace('webp', 'jpg')

            yield {"url": url, "source": response.request.url}

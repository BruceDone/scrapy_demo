# -*- coding: utf-8 -*-
from scrapy import cmdline

cmd = 'scrapy crawl cnblogs'
cmdline.execute(cmd.split(' '))

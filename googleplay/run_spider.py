# -*- coding: utf-8 -*-
from scrapy import cmdline

cmd = 'scrapy crawl google'
cmdline.execute(cmd.split(' '))

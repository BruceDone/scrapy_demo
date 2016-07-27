from scrapy import cmdline
cmd_str = 'scrapy crawl download_douban'
cmdline.execute(cmd_str.split(' '))
from scrapy import cmdline
cmd_str = 'scrapy crawl blogs'
cmdline.execute(cmd_str.split(' '))
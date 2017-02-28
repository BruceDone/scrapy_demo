from scrapy import cmdline


cmdstr = " scrapy crawl cnbeta "
#cmdstr += " -o cnbeta.csv -t csv  "
cmdline.execute(cmdstr.split())

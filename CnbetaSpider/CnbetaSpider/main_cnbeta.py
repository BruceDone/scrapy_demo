from scrapy import cmdline


cmdstr = " scrapy crawl crawl_cnbeta "
#cmdstr += " -o cnbeta.csv -t csv  "
cmdline.execute(cmdstr.split())

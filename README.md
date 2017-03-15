# Scrapy_demo

this project scrapes a list of websites I used to crawl most often
if this project helped you, please give it a star, thanks :)

# Spider list

* douban
* googleplay
* cnbeta
* ka

# Project Feature

* google play uses the crawl spider and pymongo
* douban image use the imagepiepline to download image (use the headers in case of being banned)
* cnbeta uses sqlalchmey to save items to mysql database (or other database if sqlalchemy supports)
* ka uses the kafka , this is a demo spider how to use the scrapy and kafka together , this spider will not close , if you push a message to the kafka ,the spider will start to crawl the url you just give

# How to use

for each project there is a run_spider.py script, just run it and enjoy :)

```
python run_spider.py
```

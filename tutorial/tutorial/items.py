# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BaseItem(scrapy.Item):
    post_title = Field()
    post_time = Field()
    post_url = Field()
    last_time = Field()

class DoubanItem(scrapy.Item):
    post_title = Field()
    last_time = Field()
    # reply_no = Field()
    post_url = Field()

class DoubanPostItem(DoubanItem):
    author = Field()
    content = Field()

class NowcoderItem(scrapy.Item):
    post_url = Field()
    post_title = Field()
    post_time = Field()
    author = Field()
    content = Field()

class ShuimuItem(BaseItem):
    author = Field()
    content = Field()

    pass

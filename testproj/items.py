# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TestprojItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _source = scrapy.Field()
    _title = scrapy.Field()
    _abstract = scrapy.Field()
    _author = scrapy.Field()
    _date = scrapy.Field()
    _views = scrapy.Field()
    _likes = scrapy.Field()
    

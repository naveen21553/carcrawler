# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem

class AutocarindiaspiderSpider(CrawlSpider):
    name = 'autocarindiaspider'
    allowed_domains = ['autocarindia.com']
    start_urls = ['http://autocarindia.com/car-news/']

    rules = (
        Rule(LinkExtractor(restrict_css='.next a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for news in response.xpath('//div[@class="blog row"]'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.inner a::text')
            loader.add_css('_abstract', '.inner .text-justify::text')
            loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.blogger-name span::text')
            loader.add_css('_image', 'figure.img img::attr(src)')
            loader.add_css('_date', '.inner time::text')

            loader.add_value('_source', response.url)
            yield loader.load_item()

# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem


class CarmagazinespiderSpider(CrawlSpider):
    name = 'carmagazinecrawler'
    allowed_domains = ['carmagazine.co.uk']
    start_urls = ['https://www.carmagazine.co.uk/car-news/']

    rules = (
        Rule(LinkExtractor(restrict_css='.infinite-more-link'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for news in response.css('.panel'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.title a::text')
            loader.add_css('_abstract', '.desc::text')
            # No views tracked
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.author::text')
            loader.add_css('_image', '#pageGrid img::attr(src)')
            loader.add_css('_date', '.date::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()

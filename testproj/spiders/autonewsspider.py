# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem


class AutonewsspiderSpider(CrawlSpider):
    name = 'autonewsspider'
    allowed_domains = ['autonews.com']
    start_urls = ['https://www.autonews.com/news/']

    rules = (
        Rule(LinkExtractor(restrict_css=".button.omnitrack"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for news in response.css('.feature-article-full-width-wrapper'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.feature-article-headline .omnitrack::text')
            # loader.add_css('_abstract', '.inner .text-justify::text')
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            # loader.add_css('_author', '.blogger-name span::text')
            # loader.add_css('_image', 'figure.img img::attr(src)')
            loader.add_css('_date', '.divider-gray::attr(data-lastupdated)')

            loader.add_value('_source', response.url)
            yield loader.load_item()
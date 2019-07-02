# -*- coding: utf-8 -*-

# Not Working

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem
from scrapy_splash import SplashRequest

class AutolistspiderSpider(CrawlSpider):
    name = 'autolistcrawler'
    allowed_domains = ['autolist.com']
    start_urls = ['https://www.autolist.com/news-and-analysis/']

    rules = (
        Rule(LinkExtractor(restrict_css='.next a'), callback='parse_item', follow=True),
    )

    # def start_requests(self):
    #     scrapy.Request(url='https://www.autolist.com/news-and-analysis/', callback=self.parse_item)

    def parse_item(self, response):
        for news in response.xpath('//div[@class=["jsx-342853689 article"]'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.data .title::text')
            # loader.add_css('_abstract', '.inner .text-justify::text')
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.byline::text')
            loader.add_css('_image', 'img::attr(src).data')
            loader.add_css('_date', '.byline::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()


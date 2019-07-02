# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from ..items import TestprojItem

class CarwalespiderSpider(scrapy.Spider):
    name = 'carwalecrawler'
    allowed_domains = ['carwale.com']

    def start_requests(self):
        for i in range(1, 20):
            yield SplashRequest(url='https://www.carwale.com/news/page/{}'.format(i), callback=self.parse_item, args={'wait': 0.5})


    def parse_item(self, response):
        for news in response.css('.blogItem'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '#viewUl .text-black::text')
            # No abstract
            # loader.add_css('_abstract', '#ajax-posts p::text')
            # No views tracked
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.author-data span::text')
            loader.add_css('_image', '.img-wrap img::attr(src)')
            loader.add_css('_date', 'abbr::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()
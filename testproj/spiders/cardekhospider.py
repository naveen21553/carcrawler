# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem

class CardekhospiderSpider(CrawlSpider):
    name = 'cardekhocrawler'
    # allowed_domains = ['cardekho.com']
    start_urls = [
        'https://www.cardekho.com/india-car-news.htm/',
        'https://www.cardekho.com/features-stories.htm',
        'https://www.cardekho.com/car-videos.htm',
        'https://www.cardekho.com/road-test.htm'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='li:nth-child(12) a'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        for news in response.css('.card.card_news.shadowWPadding'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.holder a::text')
            loader.add_css('_abstract', '.holder .hidden-xs::text')
            # No views tracked
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.name::text')
            loader.add_css('_image', '.paddingnone .active , .LazyLoadUpperDiv .hover::attr(src)')
            loader.add_css('_date', '.dotlist span::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()

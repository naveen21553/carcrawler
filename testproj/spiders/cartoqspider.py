# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem

class CartoqspiderSpider(scrapy.Spider):
    name = 'cartoqcrawler'
    allowed_domains = ['cartoq.com']
    start_urls = ['http://www.cartoq.com/category/reviews/']

    def parse(self, response):
        for i in range(1, 20):
            yield scrapy.FormRequest.from_response(response=response,
                                                   formdata={'cat': '2280', 'pageNumber': '{}'.format(i), 'ppp': '20', 'action': 'more_post_ajax'},
                                                   callback=self.parse_item)


    def parse_item(self, response):
        for news in response.css('.blogItem'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.entry-title a::text')
            # Supposed to work but not working
            loader.add_css('_abstract', '#ajax-posts p::text')
            # No views tracked
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.entry-date span a::text')
            loader.add_css('_image', '.wp-post-image::attr(src)')
            loader.add_css('_date', '.entry-date > a::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()
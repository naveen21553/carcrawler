# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from ..items import TestprojItem

class CargurusspiderSpider(scrapy.Spider):
    name = 'carguruscrawler'
    allowed_domains = ['cargurus.com/Cars/autos']
    start_urls = ['https://cargurus.com/Cars/autos/']

    def parse(self, response):
        for news in response.css('.cg-research-article-link'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.cg-research-article-title::text')
            loader.add_css('_abstract', '.cg-research-article-excerpt::text')
            # No views tracked
            # loader.add_css('_views', '.body li:nth-child(1)::text')
            loader.add_css('_author', '.name::text')
            loader.add_css('_image', '.cg-research-article-image::attr(style)')
            loader.add_css('_date', '.dotlist span::text')
            loader.add_value('_source', response.url)
            yield loader.load_item()


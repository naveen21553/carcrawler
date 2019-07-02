# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import TestprojItem
from scrapy_splash import SplashRequest


class CrawlerspiderSpider(CrawlSpider):
    name = 'autoblogcrawler'
    start_urls = [
        'https://www.autoblog.com/archive/'
    ]

    rules = (
        Rule(LinkExtractor(restrict_css='.pagi-next a'), callback='parse_item', follow=True),
        # Rule(LinkExtractor(restrict_css='.card-content a'), callback='parse_item', follow=True),
        # 'autoblog': {'title': 'div.record-heading span::text', 'abstract': 'div.record_details p.abstract::text', 'author': 'div.record_details span.fn::text', },
    )

    def parse_item(self, response):
        # try:
        #     current_page = int(response.css('.totalRecords::text').extract_first())
        #     total_pages = int(response.css('.totalResults::text').extract_first()) 
        # except:
        #     pass
        # sitename = response.url.split('.')[1]
        
        for news in response.css('.record_details'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = news)
            loader.add_css('_title', '.record-heading span::text')
            loader.add_css('_abstract', '.subTitle::text')
            loader.add_css('_author', '.blogger-name span::text')
            loader.add_css('_image', '.record_image svg::attr(data-original)')
            loader.add_value('_source', response.url)
            yield loader.load_item()
        
        # if current_page < total_pages:
        #     yield response.follow(response.urljoin('pg{}/'.format(current_page+1)), callback=self.parse_autoblog)
        # yield items


# from scrapy.contrib.spiders import CrawlSpider, Rule
import scrapy
from scrapy_splash import SplashRequest
import scrapy_splash
import os 
import pysolr
import logging
from scrapy.loader import ItemLoader
from scrapy.conf import settings
from ..items import TestprojItem

dir_path = os.path.dirname(os.path.realpath(__file__))

class carCrawler(scrapy.Spider):
    name = 'carcrawler'
    ignore_duplicates = settings['SOLR_IGNORE_DUPLICATES'] or False
    solr = pysolr.Solr(settings['SOLR_URL'], timeout=10)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    def start_requests(self):
        urls = []
        # with open(dir_path+'/websites.txt', 'r') as file:
        #     for website in file:
        #         if(website.find('#') == -1):
        #             urls.append(website.replace('\n', ''))
        
        urls = ['https://www.gaadi.com/car-news']
        for url in urls:

            sitename = url.split('.')[1] 

            if sitename == 'autoblog':
                yield SplashRequest(url = url, callback = self.parse_autoblog, args = {"wait": 3}, endpoint='render.html')        

            elif sitename == 'autocarindia':
                yield SplashRequest(url = url, callback = self.parse_autoblog, args = {"wait": 3}, endpoint='render.html')        
            
            # elif sitename == 'autolist':
            #     self.parse_autolist(response)
            
            elif sitename == 'autonews':
                yield SplashRequest(url = url, callback = self.parse_autonews, args = {"wait": 3}, endpoint='render.html')        
                
            # elif sitename == 'autotrader':
            #     self.parse_autotrader(response)
            
            elif sitename == 'cardekho':
                yield SplashRequest(url = url, callback = self.parse_cardekho, args = {"wait": 3}, endpoint='render.html')        
                
            
            elif sitename == 'cargurus':
                yield SplashRequest(url = url, callback = self.parse_cargurus, args = {"wait": 3}, endpoint='render.html')        
                
            
            elif sitename == 'carmagazine':
                yield SplashRequest(url = url, callback = self.parse_carmagazine, args = {"wait": 3}, endpoint='render.html')        
                            
            elif sitename == 'cartoq':
                yield SplashRequest(url = url, callback = self.parse_cartoq, args = {"wait": 3}, endpoint='render.html')        
            
            elif sitename == 'carwale':
                yield SplashRequest(url = url, callback = self.parse_carwale, args = {"wait": 3}, endpoint='render.html')        
                
            
            elif sitename == 'gaadi':
                yield SplashRequest(url = url, callback = self.parse_gaadi, args = {"wait": 3}, endpoint='render.html')        


    def parse_autoblog(self, response):
        try:
            current_page = int(response.css('.totalRecords::text').extract_first())
            total_pages = int(response.css('.totalResults::text').extract_first()) 
        except:
            pass
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        if current_page < total_pages:
            yield response.follow(response.urljoin('pg{}/'.format(current_page+1)), callback=self.parse_autoblog)
        yield items

    def parse_autocarindia(self, response):
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        next_page = response.css('#MainContent_PostList_Paging_ToNext::attr(href)').extract_first()
        yield items
        if next_page is not None:
            yield response.follow(response.urljoin(next_page), callback=self.parse_autoblog)

    def parse_autonews(self, response):

        # Load more button, no change in url
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        # next_page = response.css('.button.omnitrack::attr(href)').extract_first()
        yield items
        # if next_page is not None:
        #     SplashRequest(response.urljoin(next_page), callback=self.parse_autonews, args = {"wait": 3}, endpoint='render.html')
        
    def parse_cardekho(self, response):
        current_page = int(response.css('.pagination p::text').extract()[2])
        total_pages = int(response.css('.pagination p::text').extract()[-3]) 
        
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        if current_page < total_pages:
            yield response.follow(response.urljoin('/{}/'.format(current_page+1)), callback=self.parse_cardekho)
        yield items
    
    def parse_cargurus(self, response):
        # current_page = int(response.css('.pagination p::text').extract()[2])
        # total_pages = int(response.css('.pagination p::text').extract()[-3]) 
        
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        # if current_page < total_pages:
        #     SplashRequest(response.urljoin('/{}/'.format(current_page+1)), callback=self.parse_cardekho, args = {"wait": 3}, endpoint='render.html')
        yield items

    def parse_carmagazine(self, response):

        # url change page doesn't https://www.carmagazine.co.uk/car-news/?page=1&rpp='''288'''
        current_page = int(response.css('.pagination p::text').extract()[2])
        total_pages = int(response.css('.pagination p::text').extract()[-3]) 
        
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract
        yield items
        if current_page < total_pages:
            yield response.follow(response.urljoin('/{}/'.format(current_page+1)), callback=self.parse_cardekho)
        
    # Form request ajax
    def parse_cartoq(self, response): 
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract
        yield items
        for i in range(2, 501):
            yield scrapy.FormRequest.from_response(response=response, 
                                                formdata={'cat': 2280, 'pageNumber': i, 'ppp':20, 'action': 'more_post_ajax'},
                                                callback=self.parse_cartoq_ajax)

    def parse_cartoq_ajax(self, response):
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  

        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        yield items

    def parse_carwale(self, response):
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract
    
        yield items

        yield response.follow(response.urljoin('/page/2/'), callback=self.parse_carwale_ajax, args = {"wait": 3}, endpoint='render.html')
    
    def parse_carwale_ajax(self, response):
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        source = response.url  
        items = TestprojItem()
        items['_source'] = source
        items['_title'] = title
        items['_author'] = author
        items['_abstract'] = abstract

        yield items

        page = response.url.split('/')[-1]
        while page != 'news':
            SplashRequest(response.urljoin('/page/{}'.format(page)), callback=self.parse_carwale_ajax, args = {"wait": 3}, endpoint='render.html')

    def parse_gaadi(self, response):
        sitename = response.url.split('.')[1]
        css_dict = self.getcss(sitename)
        title = response.css(css_dict.get('title')).extract()
        abstract = response.css(css_dict.get('abstract')).extract()
        author = response.css(css_dict.get('author')).extract()
        image = response.css(css_dict.get('image')).extract()
        source = response.url  
        # for t in title:
        #     results = self.solr.search('_title:{}'.format(t))
        
        #     if len(results) > 1:
        #         self.logger.debug('\n\nArticle already exists! Aborting...\n\n')
        #         return None

        # items = TestprojItem()
        # items['_source'] = source
        # items['_title'] = title
        # items['_author'] = author
        # items['_abstract'] = abstract
        # items['_image'] = image

        for news in response.css('.card-news'):
            loader = ItemLoader(item = TestprojItem(), selector = news, response = response)
            loader.add_css('_title', 'a.card-title::text')
            loader.add_css('_abstract', 'p::text')
            loader.add_css('_author', 'div.publish a::text')
            loader.add_css('_image', 'img::attr(src)')
            loader.add_value('_source', response.url)
            yield loader.load_item()

        try:
            current_page = int(response.url.split('=')[-1])
        except:
            current_page = 1

        # if current_page < 15:
        #     yield response.follow(response.urljoin('?page={}'.format(current_page + 1)), callback=self.parse_gaadi)
        if title:
            # if title[-1]
            yield response.follow(response.urljoin('?page={}'.format(current_page + 1)), callback=self.parse_gaadi)
            # , args = {"wait": 3}, endpoint='render.html'


    def getcss(self, site):
        switcher = {
            'autoblog': {'title': 'div.record-heading span::text', 'abstract': 'div.record_details p.abstract::text', 'author': 'div.record_details span.fn::text', },
            'autocarindia': {'title': 'div.blog div.inner a::text', 'abstract': 'p.text-justify::text', 'author': 'title::text', },
            # not scraped 'autolist': {'title': 'div.jsx-342853689 div.title::text', 'abstract': '', 'author': 'div.jsx-342853689 div.byline::text' },
            'autonews': {'title': 'div.feature-article-headline a.omnitrack::text', 'abstract': 'div.feature-article-summary a.omnitrack::text', 'author':'title::text'},
            # 'autotrader': {'title': ''},
            'cardekho': {'title': 'div.gsc_col-lg-8 a::text', 'abstract': 'div.holder p::text', 'author': 'div.authorSummary div.name::text'},

            'cargurus': {'title': '.title .slnk::text, h3.cg-research-article-title::text', 'abstract': 'p.cg-research-article-excerpt::text', 'author': 'p.desc span.slnk::attr(title)'},
            'carmagazine': {'title': 'article.panel h3.title a::text', 'abstract': 'article.panel p.desc::text', 'author': 'article.panel p.info span.author::text'},
            'cartoq': {'title': 'div.entry-title a::text', 'abstract': 'div.desc p::text', 'author': '.entry-date+ span a::text , .infade , #post-237873 .entry-date a::text', 'date': 'span.entry-date a::text'},
            'carwale': {'title': 'div.news-inner-box a.text-black::text', 'abstract': 'none', 'author': '.author-data span::text'},
            'gaadi': {'title': '.card-title::text', 'abstract': 'div.card-content p::text', 'author': 'div.card-content div.publish a::text', 'image': '.card-image img::attr(src)'},
            # 'goodcarbadcar': {},
            # 'not scraped hemmings': {'title': 'div.row a > h3::text', 'abstract': 'div.row p::text', 'author': 'div.row div.meta::text'},
            # 'motortrend': {'title': ''},
            # response.css('div.block-post-summary').xpath('//span[@itemprop="name headline"]/text()').extract()
            # 'news': [],
            'nissan': {'title': '.c_001 div div p::text', 'abstract': 'none', 'author': '_nissan', 'date':'.section+ .section .introduction p , .heliostext:nth-child(1) .c_001 div div p'},
            # 'summitracing': {}, need to parse categories on this page, each rendered with js
            # 'tesla': {'title': ''},
            # 'topwheels': {},
            # 'zigwheels': {'title': 'div.zw-sl-title a::text', 'abstract': 'none', 'author': 'span.reviewer a::text', },
            'zigwheels': {'title': '#news .lnk-hvr::text', 'abstract': 'none', 'author': '#news .lnk-c::text', 'date': '#news .clr::text', 'views': '.clr+ li::text' },
        }
        return switcher.get(site, [])
    
        

          
        # elif sitename == 'goodcarbadcar':
        #     self.parse_goodcarbadcar(response)
        
        # elif sitename == 'hemmings':
        #     self.parse_hemmings(response)
        
        # elif sitename == 'motortrend':
        #     self.parse_motortrend(response)
        
        # elif sitename == 'news':
        #     self.parse_news(response)
        
        # elif sitename == 'nissan':
        #     self.parse_nissan(response)
        
        # elif sitename == 'summitracing':
        #     self.parse_summitracing(response)
        
        # elif sitename == 'tatamotors':
        #     self.parse_tatamotors(response)
        
        # elif sitename == 'tesla':
        #     self.parse_tesla(response)
        
        # elif sitename == 'topspeed':
        #     self.parse_topspeed(response)
        
        # elif sitename == 'zigwheels':
        #     self.parse_zigwheels(response)
        
        # css_dict = self.getcss(sitename)
        # title = response.css(css_dict.get('title')).extract()
        # abstract = response.css(css_dict.get('abstract')).extract()
        # author = response.css(css_dict.get('author')).extract()
        # fname = 'html/site_{}.html'.format(response.url.split('.')[1])
        # linkfile = 'links/site_{}.txt'.format(response.url.split('.')[1])
        # source = response.url


        # items['_source'] = source
        # items['_title'] = title
        # items['_author'] = author
        # items['_abstract'] = abstract

        # with open(linkfile, 'w') as lf:
        #     for url in response.css('a::attr(href)').extract():
        #         lf.write(url+'\n')

        # with open(fname, 'wb') as f:
        #     f.write(response.body)

        # yield items


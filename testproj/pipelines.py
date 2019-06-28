# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
# import pymongo

import pysolr
import logging
from scrapy.conf import settings

class TestprojPipeline(object):
    
    # collection_name = 'all_about_cars'
    # def __init__(self):
    #     self.conn = pymongo.MongoClient('localhost', 27017)
    #     db = self.conn['carsdb']
    #     self.collection = db['cars_table']

    # def process_item(self, item, spider):
        # d = dict(item)
        # authors = d['_author']
        # titles = d['_title']
        # abstracts = d['_abstract']
        # source = d['_source']

        # article = {}
        # for i in range(len(authors)):
        #     article['source'] = source
        #     article['_title'] = titles[i]
        #     article['_author'] = authors[i]
        #     article['_abstract'] = abstracts[i]

        #     self.collection.insert(article)
        
    #     return item

    # _id
    # articles: [{
    #     title:
    #     author:
    #     abstract:
    # }]

    def __init__(self):
        # self.mapping = settings['SOLR_MAPPING'].items()
        self.ignore_duplicates = settings['SOLR_IGNORE_DUPLICATES'] or False
        self.id_fields = ['_title']
        # if self.ignore_duplicates and not self.id_fields:
        #     raise RuntimeError('To ignore duplicates SOLR_DUPLICATES_KEY_FIELDS has to be defined')
        self.solr = pysolr.Solr(settings['SOLR_URL'], timeout=10)

    def process_item(self, item, spider):
        # if self.ignore_duplicates:
        #     dup_keys_values = [str(dst) + ':' + '"' + self.__get_item_value__(item, src) + '"' for dst, src in
        #                        self.mapping
        #                        if dst in self.id_fields]
        #     query = " ".join(dup_keys_values)
        #     result = self.solr.search(query)
        #     if len(result) != 0:
        #         logging.info('Skipping duplicate')
        #         return item

        d = dict(item)
        authors = d['_author']
        titles = d['_title']
        abstracts = d['_abstract']
        source = d['_source']
        images = d['_image']


        for i in range(len(authors)):
            article = {}
            article['source'] = source
            article['_title'] = titles[i]
            article['_author'] = authors[i]
            article['_abstract'] = abstracts[i]
            article['_image'] = images[i]
            self.solr.add([article], commit=True)            

        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.debug('\n\nadding articles\n\n')

        logger.debug('\n\nadded articles\n\n')       

        # solr_item = {}
        # for dst, src in self.mapping:
        #     solr_item[dst] = self.__get_item_value__(item, src)
        # self.solr.add([solr_item])
        return item

    def __get_item_value__(self, item, src):
        if type(src) is str:
            return item[src] if src in item else None
        elif type(src) is list:
            return [item[i] if i in item else None for i in src]
        else:
            raise TypeError('Only string and list are valid mapping source')

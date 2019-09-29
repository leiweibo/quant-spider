# -*- coding: utf-8 -*-
import scrapy


class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']

    def parse(self, response):
        pass

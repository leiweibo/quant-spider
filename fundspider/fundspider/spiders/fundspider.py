# coding:utf-8
import scrapy
from fundspider.items import FundspiderItem
import json
import re

class fundspider(scrapy.Spider):
    name = 'fund-spider'
    allowed_domains = ["http://www.eastmoney.com/", "http://fund.eastmoney.com"]
    start_urls = [
        'http://fund.eastmoney.com/js/fundcode_search.js'
        # 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=gp&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=200&dx=1'
    ]



    def parse(self, response):
        print(f'-------------------------start to parse reponse.....')
        rawResponse = response.text

        rawJsonResposne = re.findall('var r = (.*])', rawResponse)[0]
        jsonResponse = json.loads(rawJsonResposne)
        
        for response in jsonResponse:
            print(response[0])
           
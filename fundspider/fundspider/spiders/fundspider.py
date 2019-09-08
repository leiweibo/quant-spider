# coding:utf-8
import scrapy
from fundspider.items import FundspiderItem
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup

class fundspider(scrapy.Spider):
    name = 'fund-spider'
    fundtype = 'all'
    allowed_domains = ["www.eastmoney.com/", "fund.eastmoney.com"]
    start_urls = [
        # 'http://fund.eastmoney.com/js/fundcode_search.js'
        f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=100&dx=1'
    ]



    def parse(self, response):
        
        rawResponse = response.text

        allpages = re.findall('allPages:(\d*)', rawResponse)[0]
        currentPage = re.findall('pageIndex:(\d*)', rawResponse)[0]
        print(f'all pages ---->{allpages}, current page->{currentPage}')
        dataJsonReponse = re.findall('var rankData = {datas:(.*])', rawResponse)[0]
        jsonResponse = json.loads(dataJsonReponse)
        for response in jsonResponse:
            array = response.split(',')
            print(array[0] + array[1])
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=110022&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page=1'
            yield scrapy.Request(targetFundNetValueUrl, self.parseHistoryNetvalue)

        
        # if (int(currentPage) < int(allpages)):
        #     targetFundListUrl = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=zzf&st=desc&pi={int(currentPage) + 1}&pn=100&dx=1'
        #     print(f'最终的target: {targetFundListUrl}')
        #     yield scrapy.Request(targetFundListUrl, self.parse)
    
    def parseHistoryNetvalue(self, response):
        rawResponse = response.text
        soup = BeautifulSoup(rawResponse, 'html.parser')
        fundNetvalues = []
        for row in soup.findAll("tbody")[0].findAll('tr'):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents
                # 处理空值
                if val == []:
                    row_records.append('---')
                else:
                    row_records.append(val[0])
            print(f'{row_records[1]}    {row_records[2]}')
            fundNetvalues.append(row_records)
        pages = re.findall('pages:(\d*)', rawResponse)[0]
        curpage = re.findall('curpage:(\d*)', rawResponse)[0]
        print(f'{pages}  {curpage}')
        if (int(curpage) < int(pages)):
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=110022&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page={int(curpage) + 1}'
            yield scrapy.Request(targetFundNetValueUrl, self.parseHistoryNetvalue)

# coding:utf-8
import scrapy
from fundspider.items import FundspiderItem, FundNetValueItem
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
        f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=bb&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=3&dx=1'
    ]



    def parse(self, response):
        
        rawResponse = response.text

        allpages = re.findall('allPages:(\d*)', rawResponse)[0]
        currentPage = re.findall('pageIndex:(\d*)', rawResponse)[0]
        dataJsonReponse = re.findall('var rankData = {datas:(.*])', rawResponse)[0]
        jsonResponse = json.loads(dataJsonReponse)
        count = 0;
        for response in jsonResponse:
            array = response.split(',')
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={array[0]}&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page=1'
            item = FundspiderItem(fund_symbol=array[0], name=array[1])
            yield item
            request = scrapy.FormRequest(targetFundNetValueUrl, self.parseHistoryNetvalue)
            request.meta['fund_code'] = array[0]
            count += 1
            request.meta['count'] = (count)
            yield request

        
        if (int(currentPage) < int(allpages)):
            targetFundListUrl = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=qdii&rs=&gs=0&sc=zzf&st=desc&pi={int(currentPage) + 1}&pn=100&dx=1'
            print(f'最终的target: {targetFundListUrl}')
            yield scrapy.Request(targetFundListUrl, self.parse)
    
    fund_code = ''
    def parseHistoryNetvalue(self, response):
        global fund_code
        if (response.meta.get('fund_code') != None):
            fund_code = response.meta.get('fund_code')
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
            item = FundNetValueItem(fund_symbol = fund_code, fund_date = row_records[0], fund_net_value=row_records[1], fund_accu_net_value=row_records[2], redemption_status = row_records[5], subscription_status = row_records[4])
            yield item
            # print(f'{row_records[1]}    {row_records[2]}')

            
        pages = int(re.findall('pages:(\d*)', rawResponse)[0])
        curpage = int(re.findall('curpage:(\d*)', rawResponse)[0])
        if (int(curpage) < int(pages)):
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={fund_code}&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page={int(curpage) + 1}'
            yield scrapy.Request(targetFundNetValueUrl, self.parseHistoryNetvalue)

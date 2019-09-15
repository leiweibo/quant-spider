# coding:utf-8
import scrapy
from fundspider.items import FundspiderItem, FundNetValueItem
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
import logging

class fundspider(scrapy.Spider):
    name = 'fund-spider'
    fundtype = 'all'
    allowed_domains = ["www.eastmoney.com/", "fund.eastmoney.com"]
    start_urls = [
        # 'http://fund.eastmoney.com/js/fundcode_search.js'
        f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc=zzf&st=desc&pi=1&pn=1000&dx=1'
    ]

    fund_count = 0
    def parse(self, response):
        rawResponse = response.text
        # allpages = min(1, int(re.findall('allPages:(\d*)', rawResponse)[0])) #for test
        allpages = re.findall('allPages:(\d*)', rawResponse)[0]
        currentPage = re.findall('pageIndex:(\d*)', rawResponse)[0]
        dataJsonReponse = re.findall('var rankData = {datas:(.*])', rawResponse)[0]
        jsonResponse = json.loads(dataJsonReponse)
        for response in jsonResponse:
            self.fund_count += 1
            logging.error('the fund count is:' + str(self.fund_count)) #for test
            array = response.split(',')
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={array[0]}&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page=1'
            item = FundspiderItem(fund_symbol=array[0], name=array[1])
            yield item
            request = scrapy.Request(targetFundNetValueUrl, self.parseHistoryNetvalue)
            yield request

        if (int(currentPage) < int(allpages)):
            targetFundListUrl = f'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft={self.fundtype}&rs=&gs=0&sc=zzf&st=desc&pi={int(currentPage) + 1}&pn=1000&dx=1'
            print(f'最终的target: {targetFundListUrl}')
            yield scrapy.Request(targetFundListUrl, self.parse)

    fund_net_value_count_dict = {}
    def parseHistoryNetvalue(self, response):
        fund_net_value_count = 0
        fund_code = re.findall('code=(\d*)', str(response.url))[0]
        rawResponse = response.text
        soup = BeautifulSoup(rawResponse, 'html.parser')
        fundNetvalues = []
        for row in soup.findAll("tbody")[0].findAll('tr'):
            row_records = []
            for record in row.findAll('td'):
                val = record.contents
                # 处理空值
                if val == []:
                    row_records.append('0')
                else:
                    row_records.append(val[0])
            fund_net_value_count += 1
            item = FundNetValueItem(fund_symbol = fund_code, fund_date = row_records[0], fund_net_value=row_records[1], fund_accu_net_value=row_records[2], redemption_status = row_records[5], subscription_status = row_records[4])
            yield item
            # print(f'{row_records[1]}    {row_records[2]}')

        if (fund_code in self.fund_net_value_count_dict):
            self.fund_net_value_count_dict[fund_code] = self.fund_net_value_count_dict[fund_code] + fund_net_value_count
        else:
            self.fund_net_value_count_dict[fund_code] = fund_net_value_count
        #for test
        logging.error('the fund net value count is:' + str(fund_code) + "--->" + str(self.fund_net_value_count_dict[fund_code]))
        pages = int(re.findall('pages:(\d*)', rawResponse)[0])
        # pages = 1 # for test
        curpage = int(re.findall('curpage:(\d*)', rawResponse)[0])
        if (int(curpage) < int(pages)):
            dt = datetime.now()
            targetFundNetValueUrl = f'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code={fund_code}&sdate=2004-01-01&edate={dt.strftime("%Y-%m-%d")}&per=20&page={int(curpage) + 1}'
            yield scrapy.Request(targetFundNetValueUrl, self.parseHistoryNetvalue)

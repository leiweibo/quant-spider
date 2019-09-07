# coding:utf-8
import scrapy
from fundspider.items import FundspiderItem

class fundspider(scrapy.Spider):
    name = 'fund-spider'
    allowed_domains = ["http://www.eastmoney.com/", "http://fund.eastmoney.com"]
    start_urls = [
        'http://fund.eastmoney.com/fund.html'
    ]

    def parse(self, response):
        print(f'-------------------------start to parse reponse.....')
        fundtrs = response.xpath('//*[@id="oTable"]/tbody/tr')
        for tr in fundtrs:
            order = tr.xpath('.//td[3]/text()').extract()[0]
            symbol = tr.xpath('.//td[4]/text()').extract()[0]
            name = tr.xpath('.//td[5]/nobr/a[1]/@title').extract()[0]
            redemption_status = tr.xpath('.//td[12]/text()').extract()[0]
            subscription_status = tr.xpath('.//td[13]/text()').extract()[0]
            subscription_fee = tr.xpath('.//td[14]//a/text()').extract()
            if len(subscription_fee) == 0:
                final_sub_fee = '---'
            else:
                final_sub_fee = subscription_fee[0]
            print(f'{order} {symbol} {name} {redemption_status} {subscription_status} {final_sub_fee}')
            item = FundspiderItem(order=order, symbol = symbol, name=name, redemption_status = redemption_status, subscription_status = subscription_fee, subscription_fee = final_sub_fee)
            yield item

           
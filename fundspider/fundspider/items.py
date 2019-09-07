# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FundspiderItem(scrapy.Item):
    # 顺序
    order = scrapy.Field()
    # 基金代码
    symbol = scrapy.Field()
    # 基金简称
    name = scrapy.Field()
    # 赎回状态
    redemption_status = scrapy.Field()
    # 申购状态
    subscription_status = scrapy.Field()
    # 手续费
    subscription_fee = scrapy.Field()
    pass

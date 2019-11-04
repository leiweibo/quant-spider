# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockCombinationsItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    active_flag = scrapy.Field()
    star = scrapy.Field()
    market = scrapy.Field()
    owner_id = scrapy.Field()
    create_at = scrapy.Field()
    update_at = scrapy.Field()
    last_rb_id = scrapy.Field()
    daily_gain = scrapy.Field()
    month_gain = scrapy.Field()
    total_gain = scrapy.Field()
    net_value = scrapy.Field()
    rank_percent = scrapy.Field()
    annualized_gain_rate = scrapy.Field()
    bb_rate = scrapy.Field()
    follower_count = scrapy.Field()
    view_rebalancing = scrapy.Field()
    last_reblanceing = scrapy.Field()
    last_success_rebalance = scrapy.Field()
    tag = scrapy.Field()
    recomment_reason = scrapy.Field()
    sale_flag = scrapy.Field()
    sell_flag = scrapy.Field()
    commission = scrapy.Field()
    initial_capital = scrapy.Field()
    listed_flag = scrapy.Field()
    countractor_id = scrapy.Field()
    last_user_rb_gid = scrapy.Field()
    performance = scrapy.Field()
    closed_at = scrapy.Field()
    badge_exist = scrapy.Field()
    rankingDate = scrapy.Field()
    owner = scrapy.Field()

class OwnerItem(scrapy.Item):
    id = scrapy.Field()
    screen_name = scrapy.Field()

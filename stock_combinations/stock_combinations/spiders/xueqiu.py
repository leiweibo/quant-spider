# -*- coding: utf-8 -*-
import scrapy
import json
from stock_combinations.crackxueqiulogin import CrackXueqiu
from scrapy.loader import ItemLoader
from stock_combinations.items import StockCombinationsItem
from scrapy.loader.processors import Join, MapCompose, SelectJmes

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']
    login_result = True
    cookiestr = ''
    send_headers = {}

    # dictionary to map UserItem fields to Jmes query paths
    jmes_paths = {
        'id' : 'id',
        'name' : 'name',
        'description' : 'description',
        'active_flag' : 'active_flag',
        'star' : 'star',
        'market' : 'market',
        'owner_id' : 'owner_id',
        'create_at' : 'create_at',
        'update_at' : 'update_at',
        'last_rb_id' : 'last_rb_id',
        'daily_gain' : 'daily_gain',
        'month_gain' : 'month_gain',
        'total_gain' : 'total_gain',
        'net_value' : 'net_value',
        'rank_percent' : 'rank_percent',
        'annualized_gain_rate' : 'annualized_gain_rate',
        'bb_rate' : 'bb_rate',
        'follower_count' : 'follower_count',
        'view_rebalancing' : 'view_rebalancing',
        'last_reblanceing' : 'last_reblanceing',
        'last_success_rebalance' : 'last_success_rebalance',
        'tag' : 'tag',
        'recomment_reason' : 'recomment_reason',
        'sale_flag' : 'sale_flag',
        'sell_flag' : 'sell_flag',
        'commission' : 'commission',
        'initial_capital' : 'initial_capital',
        'listed_flag' : 'listed_flag',
        'countractor_id' : 'countractor_id',
        'last_user_rb_gid' : 'last_user_rb_gid',
        'performance' : 'performance',
        'closed_at' : 'closed_at',
        'badge_exist' : 'badge_exist',
        'rankingDate' : 'rankingDate',
        'owner' : 'owner'
    }

    def __init__(self):
        # crack = CrackXueqiu()
        # self.login_result = crack.crack()
        pass
    

    def start_requests(self):
        if not self.login_result:
            print('自动登录不成功，停止')
            pass

        str=''
        with open('xueqiu_cookie.json','r',encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        cookie = [item["name"] + "=" + item["value"] for item in listCookies]
        self.cookiestr = '; '.join(item for item in cookie)
        print(f'从文件中读取的cookie: {self.cookiestr}')
        combination_adjust_url = 'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389&count=20&page=1'
        url = "https://httpbin.org/get?show_env=1"
        self.send_headers={
            'cookie': self.cookiestr,
            # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        # print(f'headers的内容是：{send_headers}')
        # print({cookiestr})
        currentPage = 1
        url = f'https://xueqiu.com/cubes/discover/rank/cube/list.json?category=14&page={currentPage}&count=20'
        yield scrapy.Request(url, headers = self.send_headers)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        # yield jsonresponse

        for c in jsonresponse['list']:
            loader = ItemLoader(item = StockCombinationsItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')

            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(c))
            item = loader.load_item()
            yield item
            
        
        page = jsonresponse['page']
        maxPage = jsonresponse['maxPage']
        if (page < maxPage):
            self.url = f'https://xueqiu.com/cubes/discover/rank/cube/list.json?category=14&page={page+1}&count=20'
        print('the url is: {self.url}, the headers: {self.headers}')
        yield scrapy.Request(self.url, headers = self.send_headers)


# -*- coding: utf-8 -*-
import scrapy
import json
from stock_cubes.crackxueqiulogin import CrackXueqiu
from scrapy.loader import ItemLoader
from stock_cubes.items import StockCubesItem, OwnerItem
from scrapy.loader.processors import Join, MapCompose, SelectJmes

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']
    login_result = True
    cookiestr = ''
    send_headers = {}
    cube_discover_url = 'https://xueqiu.com/cubes/discover/rank/cube/list.json?category=14&count=20&page='

    # dictionary to map UserItem fields to Jmes query paths
    jmes_paths = {
        'name' : 'name',
        'symbol': 'symbol',
        'market': 'market',
        'net_value' :'net_value',
        'daily_gain' : 'daily_gain',
        'monthly_gain': 'monthly_gain',
        'total_gain' : 'total_gain',
        'annualized_gain': 'annualized_gain',
        'closed_at' : 'closed_at', # 这个字段如果为空，则表示未关闭状态
        'owner': 'owner'
    }

    owner_jmes_paths = {
        'id': 'id',
        'screen_name': 'screen_name'
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
        cube_adjust_url = 'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389&count=20&page=1'
        url = "https://httpbin.org/get?show_env=1"
        self.send_headers={
            'cookie': self.cookiestr,
            # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        # print(f'headers的内容是：{send_headers}')
        # print({cookiestr})
        currentPage = 1
        finalUrl = f'{self.cube_discover_url}{currentPage}'
        yield scrapy.Request(finalUrl, headers = self.send_headers)

    def parse(self, response):
        jsonresponse = json.loads(response.body_as_unicode())
        # yield jsonresponse

        for c in jsonresponse['list']:
            loader = ItemLoader(item = StockCubesItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')

            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(c))
            item = loader.load_item()
            

            ownerLoader = ItemLoader(item = OwnerItem())
            ownerLoader.default_input_processor = MapCompose(str)
            ownerLoader.default_output_processor = Join(' ')
            for (field, path) in self.owner_jmes_paths.items():
                ownerLoader.add_value(field, SelectJmes(path)(c['owner']))
            owner = ownerLoader.load_item()

            item['owner'] = owner
            yield item

            # 开始提取用户信息 
            uid = owner['id']
            # https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid=6626771620&pid=-24（创建的组合）
            createdCubeUrl = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-24'
            #  请求用户创建的组合
            # 通过cb_kwargs的方式，给解析函数传递参数
            yield scrapy.Request(createdCubeUrl, self.parseCubeList, headers = self.send_headers, cb_kwargs = dict(uid =uid, screen_name=owner['screen_name']))

            # 请求用户关注的组合
            # followedCubeUrl = f'https://stock.xueqiu.com/v5/stock/portfolio/stock/list.json?size=1000&category=3&uid={uid}&pid=-120'
            # yield scrapy.Request(followedCubeUrl, self.)
            
            # 组合信息：
            # https://xueqiu.com/cubes/quote.json?code=ZH976766,SP1034535,SP1012810,ZH1160206,ZH2003755,ZH1996976,ZH1079481,ZH1174824,ZH1079472,SP1040320
            
            
        
        page = jsonresponse['page']
        maxPage = jsonresponse['maxPage']
        maxPage = 2
        if (page < maxPage):
            url = f'{self.cube_discover_url}{page+1}'
            yield scrapy.Request(url, headers = self.send_headers)

    #
    # 通过去查找创建的组合以及组合的基本信息
    #
    def parseCubeList(self, response, uid, screen_name): 
        jsonresponse = json.loads(response.body_as_unicode())
        print(jsonresponse)
        print(jsonresponse['data']['stocks'])
        stockJson = jsonresponse['data']['stocks']

        symbolListStr = (",".join(str(s['symbol']) for s in stockJson))
        cubeInfoUrl = 'https://xueqiu.com/cubes/quote.json?code=' + symbolListStr
        symbolList = symbolListStr.split(',')
        yield scrapy.Request(cubeInfoUrl, self.parseCubeInfo, headers = self.send_headers, cb_kwargs = dict(uid =uid, screen_name=screen_name, symbolList = symbolList))
        pass

    def parseCubeInfo(self, response, uid, screen_name, symbolList):
        # print('the url is----->' + response.url +', the symbolList:' + symbolList)
        jsonresponse = json.loads(response.body_as_unicode())
        print(f'---------->{symbolList}')
        for s in symbolList:
            print(jsonresponse[s])
            loader = ItemLoader(item = StockCubesItem())
            loader.default_input_processor = MapCompose(str)
            loader.default_output_processor = Join(' ')
            for (field, path) in self.jmes_paths.items():
                loader.add_value(field, SelectJmes(path)(jsonresponse[s]))
            item = loader.load_item()
            owner = OwnerItem()
            owner['id'] = uid
            owner['screen_name'] = screen_name
            item['owner'] = owner
            yield item
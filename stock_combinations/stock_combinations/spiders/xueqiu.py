# -*- coding: utf-8 -*-
import scrapy
import json
from stock_combinations.crackgeetest import CrackGeetest

class XueqiuSpider(scrapy.Spider):
    name = 'xueqiu'
    allowed_domains = ['xueqiu.com']
    start_urls = ['http://xueqiu.com/']
    login_result = True

    def __init__(self):
        crack = CrackGeetest()
        self.login_result = crack.crack()
    

    def start_requests(self):
        if not self.login_result:
            print('自动登录不成功，停止')
            pass

        str=''
        with open('xueqiu_cookie.json','r',encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        cookie = [item["name"] + "=" + item["value"] for item in listCookies]
        cookiestr = '; '.join(item for item in cookie)
        print(f'从文件中读取的cookie: {cookiestr}')
        combination_adjust_url = 'https://xueqiu.com/cubes/rebalancing/history.json?cube_symbol=ZH010389&count=20&page=1'
        url = "https://httpbin.org/get?show_env=1"
        send_headers={
            'cookie': cookiestr,
            # 'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        # print(f'headers的内容是：{send_headers}')
        # print({cookiestr})
        yield scrapy.Request(combination_adjust_url, headers = send_headers)

    def parse(self, response):
        print(response.text)
        pass

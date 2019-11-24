# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import redis
class StockCubesPipeline(object):
    r = redis.Redis(host='localhost', password = '123456')

    def process_item(self, item, spider):
        if self.r.get(item['symbol']):
            print(f"${item['symbol']} exists, just return.")
            return item
        else:
            self.r.set(item['symbol'], item['symbol'])
        with open('cube.json', 'a') as f:
            f.write(str(item['symbol'] +', ' + item['name']) + ' by ' + str(item['owner']))
            f.write('\n')
            f.close()
        
        return item
    

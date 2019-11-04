# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class StockCombinationsPipeline(object):
    def process_item(self, item, spider):
        print(f"--------------------------{type(item['owner'])}")
        # with open('combination.json', 'a') as f:
        #         f.write(str(item['name']) + ' by ' + str(item['owner']['screen_name']))
        #         f.write('\\n')
        #         f.close()
        return item

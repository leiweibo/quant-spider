# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class StockCubesPipeline(object):
    def process_item(self, item, spider):
        with open('cube.json', 'a') as f:
                f.write(str(item['name']) + ' by ' + str(item['owner']))
                f.write('\n')
                f.close()
        return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import taos
import datetime

from fundspider.items import FundspiderItem, FundNetValueItem
class FundspiderPipelineByTDEngine(object):

    conn = None
    cursor = None
    time_interval = datetime.timedelta(microseconds=1000)
    start_time = datetime.datetime.now()
    type_fund_insert = 'fund_insert'
    type_fund_net_value_insert = 'fund_net_value_insert'
    def open_spider(self, spider):
        print('爬虫开始执行')
        self.conn = taos.connect(host='127.0.0.1', database='db_quant')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, FundspiderItem):
            self._process_fund(item)
        elif isinstance(item, FundNetValueItem):
            self._process_fund_net_value(item)
        return item

    '''
    处理基金数据
    '''
    def _process_fund(self, item):
        exists = self._check_if_data_exist(item['fund_symbol'], self.type_fund_insert)
        if(exists):
            print('数据已经存在，不重复插入')
        else:
            value = f"('{self.start_time}', '{item['fund_symbol']}', '{item['name']}')"
            sql = 'insert into t_fund(fund_timestamp, fund_symbol, fund_name) values ' + value
            self.start_time += self.time_interval
            # 执行事务
            try:
                self.cursor.execute(sql)
                self.conn.commit()
                self._save_to_cache(item['fund_symbol'], self.type_fund_insert)
            except Exception as e:
                print('exception at process fund:' + str(e))
                self.conn.rollback()

    '''
    处理资金净值数据
    '''
    def _process_fund_net_value(self, item):
        if(self._check_if_data_exist(str(item['fund_symbol'] + item['fund_date']), self.type_fund_insert)):
            print('数据已经存在，不重复插入')
        else:
            fundDate = datetime.datetime.strptime(item['fund_date'], '%Y-%m-%d')
            value = f"('{self.start_time}', '{item['fund_symbol']}', '{fundDate}', '{item['fund_net_value']}', '{item['fund_net_value']}', '{item['redemption_status']}', '{item['subscription_status']}')"
            sql = 'insert into t_fund_net_value(net_value_timestamp, fund_symbol, fund_date, fund_net_value, fund_accu_net_value, redemption_status, subscription_status) values ' + value
            self.start_time += self.time_interval
            # 执行事务
            try:
                self.cursor.execute(sql)                
                self.conn.commit()
                self._save_to_cache(str(item['fund_symbol'] + item['fund_date']), self.type_fund_net_value_insert)
            except Exception as e:
                print('exception at process fund net value:' + str(e))
                self.conn.rollback()

    def _save_to_cache(self, c_key, c_type):
        value =  f"('{self.start_time}', '{c_key}', '{c_type}')"
        if (not self._check_if_data_exist(c_key, c_type)):
            sql = 'insert into t_cache(cache_timestamp, c_key, c_type) values ' + value
            self.start_time += self.time_interval
            try:
                self.cursor.execute(sql)
                self.conn.commit()
            except Exception as e:
                print('exception at save to cache:' + str(e))
                self.conn.rollback()

    
    def _check_if_data_exist(self, c_key, c_type):
        sql = 'select count(*) from t_cache where c_key = "{c_key}" and c_type = "{c_type}"'
        
        try: 
            self.cursor.execute(sql)
            for c in self.cursor:
                return c[0] > 0
            return False
        except Exception  as e:
            print('exception at check data if exists:' + str(e))
            return False

    def close_spider(self, spider):
        print('爬虫结束')
        self.cursor.close
        self.conn.close()

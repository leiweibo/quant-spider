# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import taos
import datetime
import logging

from fundspider.items import FundspiderItem, FundNetValueItem
from twisted.internet import defer, reactor
class FundspiderPipelineByTDEngine(object):
    fund_data = []
    fund_net_value_data = []
    fund_cache_data = []

    conn = None
    cursor = None
    batch_size = 400
    type_fund_insert = 'fund_insert'
    type_fund_net_value_insert = 'fundnetvalue_insert'
    insert_fund_sql_prefix = 'insert into t_fund(fund_timestamp, fund_symbol, fund_name) values '
    insert_fund_net_value_sql_prefix = 'insert into t_fund_net_value(net_value_timestamp, fund_symbol, fund_date, fund_net_value, fund_accu_net_value, redemption_status, subscription_status) values '
    insert_cache_prefix = 'insert into t_cache(cache_timestamp, c_key, c_type) values '
    def open_spider(self, spider):
        print('爬虫开始执行')
        self.conn = taos.connect(host='127.0.0.1', database='db_quant_copy')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        if isinstance(item, FundspiderItem):
            self._process_fund(item)
            pass
        elif isinstance(item, FundNetValueItem):
            self._process_fund_net_value(item)
            pass
        return item

    '''
    Save to db
    '''
    import taos
    import pandas as pd
    @defer.inlineCallbacks
    def _save_data_to_Db(self, sql, cursor, values, commitDirectly):
        values_str = ' '.join(str(e) for e in values)
        if (values_str):
            finalSql = sql + values_str
            logging.info(f'execute sql--> {finalSql}')
            out = defer.Deferred()
            reactor.callInThread(self._insert, finalSql, out)
            yield out
            defer.returnValue(finalSql)
            # try:
            #     self.cursor.execute(finalSql)
            #     if (commitDirectly):
            #         self.conn.commit()
            # except Exception as err:
            #     print(err)
            #     logging.error(f'exception: {finalSql}')

    def _insert(self, finalSql, out):
        try:
            self.cursor.execute(finalSql)
            reactor.callFromThread(out.callback, finalSql)
        except Exception as err:
            print(err)

    '''
    处理基金数据
    '''
    def _process_fund(self, item):
        exists = self._check_if_data_exist(item['fund_symbol'], self.type_fund_insert)
        if(exists):
            print('数据已经存在，不重复插入')
        else:
            self._save_to_cache(str(item['fund_symbol']), self.type_fund_insert)
            value = f"('{datetime.datetime.now()}', '{item['fund_symbol']}', '{item['name']}')"
            self.fund_data.append(value)
            if (len(self.fund_data) >= self.batch_size):
                self._save_data_to_Db(self.insert_fund_sql_prefix, self.cursor, self.fund_data, True)
                self.fund_data.clear()

    '''
    处理资金净值数据
    '''
    def _process_fund_net_value(self, item):
        exists = self._check_if_data_exist(str(item['fund_symbol'] + item['fund_date']), self.type_fund_net_value_insert)
        if(exists):
            print('数据已经存在，不重复插入')
        else:
            self._save_to_cache(str(item['fund_symbol'] + item['fund_date']), self.type_fund_net_value_insert)

            fundDate = datetime.datetime.strptime(item['fund_date'], '%Y-%m-%d')
            value = f"('{datetime.datetime.now()}', '{item['fund_symbol']}', '{fundDate}', '{item['fund_net_value']}', '{item['fund_net_value']}', '{item['redemption_status']}', '{item['subscription_status']}')"
            self.fund_net_value_data.append(value)
            if (len(self.fund_net_value_data) >= self.batch_size):
<<<<<<< HEAD
                self._save_data_to_Db(self.insert_fund_net_value_sql_prefix, self.cursor, self.fund_net_value_data, True)
                self.fund_net_value_data.clear()
=======
                self._save_data_to_Db(self.insert_fund_net_value_sql_prefix, self.cursor, self.fund_net_value_data)
                self.fund_net_value_data.clear()

>>>>>>> ff99678ad66ebd0fcc71951c8ed939a17f729e06

    # TODO: Save to redis
    def _save_to_cache(self, c_key, c_type):
<<<<<<< HEAD
        pass
        # value =  f"('{datetime.datetime.now()}', '{c_key}', '{c_type}')"
        # if (not self._check_if_data_exist(c_key, c_type)):
        #     self.fund_cache_data.append(value)
        #     if (len(self.fund_cache_data) >= self.batch_size):
        #         self._save_data_to_Db(self.insert_cache_prefix, self.cursor, self.fund_cache_data, False)
        #         self.fund_cache_data.clear()
=======
        value =  f"('{datetime.datetime.now()}', '{c_key}', '{c_type}')"
        if (not self._check_if_data_exist(c_key, c_type)):
            self.fund_cache_data.append(value)
            if (len(self.fund_cache_data) >= self.batch_size):
                self._save_data_to_Db(self.insert_cache_prefix, self.cursor, self.fund_cache_data)
                self.fund_cache_data.clear()
>>>>>>> ff99678ad66ebd0fcc71951c8ed939a17f729e06

    ## TODO: Check in redis
    def _check_if_data_exist(self, c_key, c_type):
        return False
        # sql = f'select count(*) from t_cache where c_key = "{c_key}" and c_type = "{c_type}"'
        # result = False
        # try:
        #     self.cursor.execute(sql)
        #     for c in self.cursor:
        #         result = c[0] > 0
        #         break
        #     # logging.error(f'the check data exist sql: {sql}')
        #     # logging.error(f'the check result is:{result}')
        #     return result
        # except Exception  as e:
        #     print('exception at check data if exists:' + str(e))
        #     return False

    def close_spider(self, spider):
        print('爬虫结束')
<<<<<<< HEAD
        self._save_data_to_Db(self.insert_fund_sql_prefix, self.cursor, self.fund_data, False)
        self.fund_data.clear()
        self._save_data_to_Db(self.insert_fund_net_value_sql_prefix, self.cursor, self.fund_net_value_data, False)
        self.fund_net_value_data.clear()
        self._save_data_to_Db(self.insert_cache_prefix, self.cursor, self.fund_cache_data, True)
        self.fund_cache_data.clear()
    
        try: 
            self.conn.close()
        except Exception as e:
            pass
=======
        self._save_data_to_Db(self.insert_fund_sql_prefix, self.cursor, self.fund_data)
        self.fund_data.clear()
        self._save_data_to_Db(self.insert_fund_net_value_sql_prefix, self.cursor, self.fund_net_value_data)
        self.fund_net_value_data.clear()
        self._save_data_to_Db(self.insert_cache_prefix, self.cursor, self.fund_cache_data)
        self.fund_cache_data.clear()

        self.cursor.close()
        self.conn.close()
>>>>>>> ff99678ad66ebd0fcc71951c8ed939a17f729e06

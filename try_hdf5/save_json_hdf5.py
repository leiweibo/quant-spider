import numpy as np
import h5py
import json

def save_data():
    '''
    组合列表数据
    '''
    cubeList = [
        {
            "user":{
                "id":2818639099,
                "screen_name":"盛世有我88",
                "photo_domain":"http://xavatar.imedao.com/",
                "profile_image_url":"community/default/avatar.png,community/default/avatar.png!180x180.png,community/default/avatar.png!50x50.png,community/default/avatar.png!30x30.png"
            },
            "rate":1.1162,
            "symbol":"SP1008125",
            "name":"盛世有我88的实盘"
        },
        {
            "user":{
                "id":4669951570,
                "screen_name":"TotemlessOne",
                "photo_domain":"http://xavatar.imedao.com/",
                "profile_image_url":"community/20151/1424586996452-1424586996593.jpeg,community/20151/1424586996452-1424586996593.jpeg!180x180.png,community/20151/1424586996452-1424586996593.jpeg!50x50.png,community/20151/1424586996452-1424586996593.jpeg!30x30.png"
            },
            "rate":0.7667,
            "symbol":"SP1036843",
            "name":"Totemless_的实盘"
        }
    ]

    cubeList2 = [
        {
            "user":{
                "id":2818639099,
                "screen_name":"盛世有我88_2",
                "photo_domain":"http://xavatar.imedao.com/",
                "profile_image_url":"community/default/avatar.png,community/default/avatar.png!180x180.png,community/default/avatar.png!50x50.png,community/default/avatar.png!30x30.png"
            },
            "rate":1.1162,
            "symbol":"SP1008125",
            "name":"盛世有我88的实盘_2"
        },
        {
            "user":{
                "id":4669951570,
                "screen_name":"TotemlessOne_2",
                "photo_domain":"http://xavatar.imedao.com/",
                "profile_image_url":"community/20151/1424586996452-1424586996593.jpeg,community/20151/1424586996452-1424586996593.jpeg!180x180.png,community/20151/1424586996452-1424586996593.jpeg!50x50.png,community/20151/1424586996452-1424586996593.jpeg!30x30.png"
            },
            "rate":0.7667,
            "symbol":"SP1036843",
            "name":"Totemless_的实盘_2"
        }
    ]

    '''
    调仓记录
    '''
    rebalanceHistoryList = [
                {
                        "id":231641361,
                        "rebalancing_id":62458118,
                        "stock_id":1027181,
                        "stock_name":"新晨科技",
                        "stock_symbol":"SZ300542",
                        "volume":0.0,
                        "price":17.12,
                        "net_value":0.0,
                        "weight":0.0,
                        "target_weight":0.0,
                        "prev_weight":100.0,
                        "prev_target_weight":100.0,
                        "prev_weight_adjusted":100.0,
                        "prev_volume":18.45269224,
                        "prev_price":18.01,
                        "prev_net_value":332.33298724,
                        "proactive":True,
                        "created_at":1572573178032,
                        "updated_at":1572573178032,
                        "target_volume":0.0,
                        "prev_target_volume":18.45269224
                },
                {"id":62407048,"status":"success","cube_id":10289,"prev_bebalancing_id":62407001,"category":"user_rebalancing","exe_strategy":"intraday_all","created_at":1572486748216,"updated_at":1572486748216,"cash_value":1.7E-7,"cash":0.0,"error_code":None,"error_message":None,"error_status":None,"holdings":None,"rebalancing_histories":[{"id":231637756,"rebalancing_id":62407048,"stock_id":1002092,"stock_name":"海联金汇","stock_symbol":"SZ002537","volume":0.0,"price":10.11,"net_value":0.0,"weight":0.0,"target_weight":0.0,"prev_weight":1.0,"prev_target_weight":1.0,"prev_weight_adjusted":1.0,"prev_volume":0.32807457,"prev_price":10.13,"prev_net_value":3.32339539,"proactive":True,"created_at":1572486748216,"updated_at":1572486748216,"target_volume":0.0,"prev_target_volume":0.32807457},{"id":231637757,"rebalancing_id":62407048,"stock_id":1027181,"stock_name":"新晨科技","stock_symbol":"SZ300542","volume":18.45269224,"price":18.01,"net_value":332.333,"weight":100.0,"target_weight":100.0,"prev_weight":None,"prev_target_weight":None,"prev_weight_adjusted":None,"prev_volume":None,"prev_price":None,"prev_net_value":None,"proactive":True,"created_at":1572486748216,"updated_at":1572486748216,"target_volume":18.45269224,"prev_target_volume":None}],"comment":"","diff":0.0,"new_buy_count":0}
            ]
    '''
    收益记录
    '''
    profitList = [
        {
            "time":1542729600000,
            "date":"2018-11-21",
            "value":0.7573,
            "percent":2.49
        },
        {
            "time":1542816000000,
            "date":"2018-11-22",
            "value":0.7554,
            "percent":2.23
        },
        {
            "time":1542902400000,
            "date":"2018-11-23",
            "value":0.7342,
            "percent":-0.65
        },
        {
            "time":1543161600000,
            "date":"2018-11-26",
            "value":0.7267,
            "percent":-1.66
        },
        {
            "time":1543248000000,
            "date":"2018-11-27",
            "value":0.73,
            "percent":-1.21
        }
    ]

    with h5py.File('cubeList.h5', 'a') as f:
        if not 'ZH1307218' in f:
            grp = f.create_group('ZH1307218')

        metaData = None
        if 'ZH1307218/cubeList' in f:
            metaData = json.loads(f['ZH1307218/cubeList'][()])
            print('load meta data')
        else:
            f['ZH1307218/cubeList'] = json.dumps(cubeList)
            print('no meta data to load.')
            metaData = cubeList
        
        if metaData:
            f['ZH1307218/cubeList'][()] = json.dumps(metaData + cubeList2)
            print('meta data is not none.')
        else:
            f['ZH1307218/cubeList'][()] = json.dumps(cubeList2)
            print('meta data is none.')

        print(f['ZH1307218/cubeList'][()])
        f.close()
        
if __name__ == '__main__':
    print("Try to save json data into hdf5.")
    save_data()
import numpy as np
import h5py
import json
import pandas as pd

def save_data_via_pandas():

    '''
    组合列表数据
    '''
    cubeList = [
        {
            "user":2818639099,
            "rate":1.162,
            "symbol":"SP1008125",
            "name":"盛世有我88的实盘_"
        },
        {
            "user":4669951570,
            "rate":0.7667,
            "symbol":"SP1036843",
            "name":"Totemless_的实盘_"
        }
    ]

    cubeList2 = [
        {
            "user":2818639099,
            "rate":1.1162,
            "symbol":"SP1008125",
            "name":"盛世有我88的实盘_2"
        },
        {
            "user":4669951570,
            "rate":0.7667,
            "symbol":"SP1036843",
            "name":"Totemless_的实盘_2"
        }
    ]
    for i in range(0, 10):
        dfItem = pd.DataFrame.from_records(cubeList)
        dfItem.to_hdf('pd_json_data.h5', format='table', key = 'cube_list', mode='a', append=True, min_itemsize={'name' : 30})
        dfItem = pd.DataFrame.from_records(cubeList2)
        dfItem.to_hdf('pd_json_data.h5', format='table', key = 'cube_list', mode='a', append=True, min_itemsize={'name' : 30})
    
    print('Fetch type:  ---->')
    print(pd.read_hdf('pd_json_data.h5', key = 'cube_list')) # type: dateframe
    print('Query data:  ---->')
    print(pd.read_hdf('pd_json_data.h5', key = 'cube_list').query('user == 4669951570')) # type: dateframe

    # store = pd.HDFStore('pd_json_data.h5', mode = 'w')
    # dfItem = pd.DataFrame.from_records(cubeList)
    # 注意，这里, min_itemsize={'name' : 30}如果不加的化，当数组前面数据的长度小于后面数据长度的时候，就回出现
    # Trying to store a string with len [25] in [name] column but
    # this column has a limit of [24]!
    # store.append(key = 'cubeList', value = dfItem, format='table', data_columns = True, min_itemsize={'name' : 30})
    # dfItem = pd.DataFrame.from_records(cubeList2)
    # store.append(key = 'cubeList', value = dfItem, format='table', data_columns = True, min_itemsize={'name' : 30})
    # print(store['cubeList']) # type: dateframe


if __name__ == '__main__':
    save_data_via_pandas()

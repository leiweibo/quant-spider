import numpy as np
import h5py
import json
import pandas as pd
class Hdf5Utils():
    def save_data_via_pandas(self, h5Name, key, dataList, exclude = None, fillna = False):
        # 需要把Null的数据设置为0.0 否则会出现append的时候，类型不匹配的问题
        if fillna:
            profiltListItem = pd.DataFrame.from_records(dataList, exclude = exclude, coerce_float = True).fillna(0.0)
        else:
            profiltListItem = pd.DataFrame.from_records(dataList, exclude = exclude, coerce_float = True)
        profiltListItem.to_hdf(h5Name, format='table', key = key, mode='a', append=True, complevel = 9)
        
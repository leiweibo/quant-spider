import numpy as np
import h5py
import json
import pandas as pd
class Hdf5Utils():
    def save_data_via_pandas(self, h5Name, key, dataList):
        print('h5Name:' + h5Name + ", key:" + key)
        profiltListItem = pd.DataFrame.from_records(dataList)
        profiltListItem.to_hdf(h5Name, format='table', key = key, mode='a', append=True, complevel = 9)
        
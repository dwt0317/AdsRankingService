from constants import *
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import utils
from scipy import sparse


class Preprocessor:
    def __init__(self):
        self._params = {}
        self._rows = 0
        self._cols = 0
        self.init_params()

    def init_params(self):
        self._params = {
            'userID_size': 2,
            'adID_size': 2,
            'position_size': 2,
        }

    # merge click data and impression data
    def get_train_data(self):
        click_header = ['time', 'userID', 'ip', 'impressionID', 'adID', 'position', 'url']
        click_data = utils.read(click_path, click_header)
        impression_header = ['time', 'userID', 'ip', 'searchID', 'impressionID', 'adID', 'position']
        impression_data = utils.read(impression_path, impression_header)
        click_list = set(click_data['impressionID'].values)
        impression_list = impression_data['impressionID'].values
        train_y = [0] * len(impression_list)
        i = 0
        for impressionID in impression_list:
            if impressionID in click_list:
                train_y[i] = 1
            i += 1
        clean_df = impression_data.drop(['time', 'impressionID', 'ip', 'searchID'], axis=1)
        del impression_data
        clean_array = clean_df.values.tolist()
        del clean_df
        self._rows = len(clean_array)
        self._cols = self._params['userID_size'] + self._params['adID_size'] + self._params['position_size']
        return clean_array, train_y

    # build train_x in lil format
    def build_lil_train(self):
        clean_array, train_y = self.get_train_data()

        train_x = sparse.lil_matrix((self._rows, self._cols), dtype=float)
        for i in xrange(self._rows):
            offset = 0
            idx = utils.hash_id(clean_array[i][0], self._params['userID_size'])
            # idx = self._userID_dict.setdefault(clean_array[i][0], 0)
            train_x[i, offset+idx] = 1
            offset += self._params['userID_size']

            # idx = self._adID_dict.setdefault(clean_array[i][1], 0)
            idx = utils.hash_id(clean_array[i][0], self._params['adID_size'])
            train_x[i, offset + idx] = 1
            offset += self._params['adID_size']

            # idx = self._position_dict.setdefault(clean_array[i][2], 0)
            idx = utils.hash_id(clean_array[i][0], self._params['position_size'])
            train_x[i, offset + idx] = 1
            offset += self._params['position_size']
        print "Loading data finished."
        return train_x, train_y

    # build train_x for deep model
    def build_deep_train(self):
        clean_array, train_y = self.get_train_data()


    # transform ad query to train_x format
    def transform_x(self, ad_query):
        userID, adID, position = ad_query.split('&')
        x = sparse.lil_matrix((self._rows, self._cols), dtype=float)
        offset = 0
        idx = utils.hash_id(userID, self._params['userID_size'])
        # idx = self._userID_dict.setdefault(clean_array[i][0], 0)
        x[0, offset + idx] = 1
        offset += self._params['userID_size']

        # idx = self._adID_dict.setdefault(clean_array[i][1], 0)
        idx = utils.hash_id(adID, self._params['adID_size'])
        x[0, offset + idx] = 1
        offset += self._params['adID_size']

        # idx = self._position_dict.setdefault(clean_array[i][2], 0)
        idx = utils.hash_id(position, self._params['position_size'])
        x[0, offset + idx] = 1
        offset += self._params['position_size']
        return x
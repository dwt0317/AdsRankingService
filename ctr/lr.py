
from constants import *
import pandas as pd
from sklearn.linear_model import LogisticRegression
import numpy as np
import utils
from scipy import sparse
import time


class LR:
    def __init__(self):
        self._userID_dict = dict()
        self._adID_dict = dict()
        self._position_dict = dict()
        self._rows = 0
        self._cols = 0
        self._model = LogisticRegression(max_iter=20)
        # self.train()

    def train(self):
        print "Training model starts: "
        train_x, train_y = self.get_train_data()
        self._model.fit(train_x, train_y)
        print "Training model finished."

    def predict(self, x):
        pred = self._model.predict_proba(x)[:, 1]
        print "ctr: " + str(pred[0])
        return float(pred[0])

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

        self._userID_dict = utils.list2dict(clean_df['userID'].unique())
        self._adID_dict = utils.list2dict(clean_df['adID'].unique())
        self._position_dict = utils.list2dict(clean_df['position'].unique())
        clean_array = clean_df.values.tolist()
        # print clean_df
        self._rows = len(clean_df)
        self._cols = len(self._userID_dict) + len(self._adID_dict) + len(self._position_dict) + 3
        del clean_df

        train_x = sparse.lil_matrix((self._rows, self._cols), dtype=float)

        # print clean_array
        for i in xrange(self._rows):
            offset = 0
            idx = self._userID_dict.setdefault(clean_array[i][0], 0)
            train_x[i, offset+idx] = 1
            offset += len(self._userID_dict) + 1

            idx = self._adID_dict.setdefault(clean_array[i][1], 0)
            train_x[i, offset + idx] = 1
            offset += len(self._adID_dict) + 1

            idx = self._position_dict.setdefault(clean_array[i][2], 0)
            train_x[i, offset + idx] = 1
            offset += len(self._position_dict) + 1

        # print train_x
        # s1 = pd.Series(label_list)
        # print impression_data
        # labeled_data = pd.concat([s1, impression_data], axis=1, ignore_index=True)
        # print labeled_data
        return train_x, train_y

    # transform ad query to train_x format
    def transform_x(self, ad_query):
        userID, adID, position = ad_query.split('&')
        x = sparse.lil_matrix((self._rows, self._cols), dtype=float)
        offset = 0
        idx = self._userID_dict.get(userID, 0)
        x[0, offset+idx] = 1
        offset += len(self._userID_dict) + 1

        idx = self._adID_dict.get(adID, 0)
        x[0, offset+idx] = 1
        offset += len(self._adID_dict) + 1

        idx = self._position_dict.get(position, 0)
        x[0, offset+idx] = 1
        return x


if __name__ == '__main__':
    lr = LR()
    print lr.predict(np.asarray([1, 0, 1, 0, 0, 0, 1, 3, 0]))

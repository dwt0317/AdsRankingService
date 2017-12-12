

from sklearn.linear_model import LogisticRegression
import numpy as np
import time
from preprocessor import Preprocessor


class LR:
    """ Training a logistic regression model and then used for prediction. """

    def __init__(self):
        self._rows = 0
        self._cols = 0
        self._params = {}
        self._model = LogisticRegression(max_iter=20)
        self._preprocessor = Preprocessor()
        self.init_params()
        # self.train()

    def init_params(self):
        self._params = {
            'userID_size': 2,
            'adID_size': 2,
            'position_size': 2,
        }

    def train(self):
        print "Training model starts: "
        train_x, train_y = self._preprocessor.build_lil_train()
        if train_x.shape[0] == 0 or len(train_y) == 0:
            print "No sample is available."
        else:
            self._model.fit(train_x, train_y)
            print "Training model finished."

    def predict(self, x):
        pred = self._model.predict_proba(x)[:, 1]
        print "ctr: " + str(pred[0])
        return float(pred[0])

    def preprocessor(self):
        return self._preprocessor

if __name__ == '__main__':
    lr = LR()
    lr.train()
    print lr.predict(np.asarray([1, 0, 1, 0, 0, 1]))

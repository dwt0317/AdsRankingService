from constants import *
import pandas as pd


class DeepModel:
    """ Training a DeepFM model and then used for prediction. """
    def __init__(self):
        self._rows = 0
        self._cols = 0
        self._params = {}
        self.init_params()
        # self.train()

    def init_params(self):
        self._params = {
            'userID_size': 2,
            'adID_size': 2,
            'position_size': 2,
        }


from constants import *
import pandas as pd

from preprocessor import Preprocessor


class DeepModel:
    """ Training a DeepFM model and then used for prediction. """
    def __init__(self):
        self._preprocessor = Preprocessor()
        # self.train()


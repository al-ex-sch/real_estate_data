import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RatioTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column1, column2, new_column_name, replace_inf_with=0, replace_nan_with=0):
        self.column1 = column1
        self.column2 = column2
        self.new_column_name = new_column_name
        self.replace_inf_with = replace_inf_with
        self.replace_nan_with = replace_nan_with

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.new_column_name] = X[self.column1] / X[self.column2]

        X[self.new_column_name].replace([np.inf, -np.inf], self.replace_inf_with, inplace=True)
        X[self.new_column_name].fillna(self.replace_nan_with, inplace=True)

        return X

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ImageColTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, column_name, new_column_name=None):
        self.column_name = column_name
        self.new_column_name = new_column_name

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.column_name] = np.where(X[self.column_name].isna(), 0, 1)

        if self.new_column_name is not None:
            X.rename(columns={self.column_name: self.new_column_name}, inplace=True)

        return X

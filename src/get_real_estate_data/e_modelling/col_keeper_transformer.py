from sklearn.base import BaseEstimator, TransformerMixin


class ColumnKeeper(BaseEstimator, TransformerMixin):
    def __init__(self, columns_to_keep):
        self.columns_to_keep = columns_to_keep

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        return X[self.columns_to_keep]

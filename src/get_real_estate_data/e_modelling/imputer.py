from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.impute import SimpleImputer


class Imputer(BaseEstimator, TransformerMixin):
    def __init__(self, input_df, columns_to_impute, strategy='constant', fill_value=0):
        self.input_df = input_df
        self.columns_to_impute = columns_to_impute
        self.strategy = strategy
        self.fill_value = fill_value
        self.imputer = SimpleImputer(strategy=self.strategy, fill_value=self.fill_value)

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X[self.columns_to_impute] = self.imputer.fit_transform(X[self.columns_to_impute])
        self.input_df[self.columns_to_impute] = self.imputer.transform(self.input_df[self.columns_to_impute])
        return X

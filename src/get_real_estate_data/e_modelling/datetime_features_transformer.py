import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class DateTimeFeaturesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, datetime_column, extract_month=True, extract_year=True, extract_quarter=True):
        self.datetime_column = datetime_column
        self.extract_month = extract_month
        self.extract_year = extract_year
        self.extract_quarter = extract_quarter

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        datetime_series = pd.to_datetime(X[self.datetime_column])

        if self.extract_month:
            X[f'{self.datetime_column}_month'] = datetime_series.dt.month

        if self.extract_year:
            X[f'{self.datetime_column}_year'] = datetime_series.dt.year

        if self.extract_quarter:
            X[f'{self.datetime_column}_quarter'] = datetime_series.dt.quarter

        return X

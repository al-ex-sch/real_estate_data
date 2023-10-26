import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class CountPerCategory(BaseEstimator, TransformerMixin):
    def __init__(self, input_df, categories, new_column_name, subset_condition=None):
        self.grouped_input_ = None
        self.input_df = input_df.copy()
        self.categories = categories
        self.new_column_name = new_column_name
        self.subset_condition = subset_condition

    def fit(self, X, y=None):
        if self.subset_condition:
            self.input_df = self.input_df.query(self.subset_condition)
        self.grouped_input_ = self.input_df.groupby(self.categories, observed=False) \
            .size().reset_index(name='count')
        self.grouped_input_.columns = self.categories + [self.new_column_name]
        return self

    def transform(self, X):
        X = pd.merge(X, self.grouped_input_, on=self.categories, how='left')
        X[self.new_column_name] = X[self.new_column_name].fillna(0)
        return X


class CountPerCategoryOld(BaseEstimator, TransformerMixin):
    def __init__(self, input_df, categories, new_column_name):
        self.grouped_input_ = None
        self.input_df = input_df.copy()
        self.categories = categories
        self.new_column_name = new_column_name

    def fit(self, X, y=None):
        self.grouped_input_ = self.input_df.groupby(self.categories, observed=False) \
            .size().reset_index(name='count')
        self.grouped_input_.columns = self.categories + [self.new_column_name]
        return self

    def transform(self, X):
        X = pd.merge(X, self.grouped_input_, on=self.categories, how='left')
        X[self.new_column_name] = X[self.new_column_name].fillna(0)
        return X

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class AverageMetricPerCategory(BaseEstimator, TransformerMixin):
    def __init__(self, input_df, metric, categories, new_column_name, subset_condition=None):
        self.grouped_input_ = None
        self.input_df = input_df.copy()
        self.metric = metric
        self.categories = categories
        self.new_column_name = new_column_name
        self.subset_condition = subset_condition

    def fit(self, X, y=None):
        if self.subset_condition:
            self.input_df = self.input_df.query(self.subset_condition)
        self.grouped_input_ = self.input_df.groupby(self.categories, observed=False) \
            .agg({self.metric: 'mean'}).reset_index()
        self.grouped_input_.columns = self.categories + [self.new_column_name]
        return self

    def impute_missing_values(self, X):
        missing_rows = X[X[self.new_column_name].isna()].index
        for index in missing_rows:
            category1_val = X.loc[index, self.categories[0]]
            category2_val = X.loc[index, self.categories[1]]
            avg_category1 = self.input_df.loc[self.input_df[self.categories[0]] == category1_val][self.metric].mean()
            avg_category2 = self.input_df.loc[self.input_df[self.categories[1]] == category2_val][self.metric].mean()
            if np.isnan(avg_category2):
                avg_category2 = avg_category1
            imputed_value = (avg_category1 + avg_category2) / 2
            X.loc[index, self.new_column_name] = imputed_value

    def transform(self, X):
        X = pd.merge(X, self.grouped_input_, on=self.categories, how='left')
        self.impute_missing_values(X)
        return X


class AverageMetricPerCategoryOld(BaseEstimator, TransformerMixin):
    def __init__(self, input_df, metric, categories, new_column_name):
        self.grouped_input_ = None
        self.input_df = input_df
        self.metric = metric
        self.categories = categories
        self.new_column_name = new_column_name

    def fit(self, X, y=None):
        self.grouped_input_ = self.input_df.groupby(self.categories, observed=False) \
            .agg({self.metric: 'mean'}).reset_index()
        self.grouped_input_.columns = self.categories + [self.new_column_name]
        return self

    def impute_missing_values(self, X):
        missing_rows = X[X[self.new_column_name].isna()].index
        for index in missing_rows:
            category1_val = X.loc[index, self.categories[0]]
            category2_val = X.loc[index, self.categories[1]]
            avg_category1 = self.input_df.loc[self.input_df[self.categories[0]] == category1_val][self.metric].mean()
            avg_category2 = self.input_df.loc[self.input_df[self.categories[1]] == category2_val][self.metric].mean()
            imputed_value = (avg_category1 + avg_category2) / 2
            X.loc[index, self.new_column_name] = imputed_value

    def transform(self, X):
        X = pd.merge(X, self.grouped_input_, on=self.categories, how='left')
        self.impute_missing_values(X)
        return X

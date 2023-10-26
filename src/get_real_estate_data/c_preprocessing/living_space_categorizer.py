import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class LivingSpaceCategorizer(BaseEstimator, TransformerMixin):
    def __init__(self, living_space_dict, selected_key):
        self.bins = living_space_dict[selected_key]['bins']
        self.labels = living_space_dict[selected_key]['labels']

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X['living_space_range'] = pd.cut(
            X['living_space'], bins=self.bins, labels=self.labels, right=False, include_lowest=True
        )
        return X

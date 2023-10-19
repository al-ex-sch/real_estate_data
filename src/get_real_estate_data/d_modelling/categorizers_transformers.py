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


class RoomCategorizer(BaseEstimator, TransformerMixin):
    def __init__(self, upper_limit):
        self.upper_limit = upper_limit

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        def room_range(rooms):
            if rooms >= self.upper_limit:
                return f"{self.upper_limit}+"
            else:
                lower_limit = int(rooms)
                upper_limit_range = lower_limit + 0.5
                return f"{lower_limit}-{upper_limit_range}"

        X['room_range'] = X['rooms'].apply(room_range)
        return X

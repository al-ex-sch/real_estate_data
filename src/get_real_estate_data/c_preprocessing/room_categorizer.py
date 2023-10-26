from sklearn.base import BaseEstimator, TransformerMixin


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

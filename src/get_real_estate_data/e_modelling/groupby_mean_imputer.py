from sklearn.base import BaseEstimator, TransformerMixin


class GroupbyMeanImputer(BaseEstimator, TransformerMixin):
    def __init__(self, groupby_col, impute_cols):
        self.groupby_col = groupby_col
        self.impute_cols = impute_cols
        self.means_ = None

    def fit(self, X, y=None):
        self.means_ = X.groupby(self.groupby_col)[self.impute_cols].mean()
        return self

    def transform(self, X, y=None):
        X_copy = X.copy()
        for col in self.impute_cols:
            col_mean = X_copy.groupby(self.groupby_col)[col].transform(lambda x: x.mean())
            X_copy[col] = X_copy[col].fillna(col_mean)
        return X_copy

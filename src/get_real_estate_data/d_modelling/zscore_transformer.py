from sklearn.base import BaseEstimator, TransformerMixin


# TODO: aby fungoval na zaklade input_df, ne ty current df (test set)
class ZScoreByCategoryTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, metric_column, category_column):
        self.std_by_category_ = None
        self.mean_by_category_ = None
        self.metric_column = metric_column
        self.category_column = category_column

    def fit(self, X, y=None):
        self.mean_by_category_ = X.groupby(self.category_column)[self.metric_column].mean()
        self.std_by_category_ = X.groupby(self.category_column)[self.metric_column].std()
        return self

    def transform(self, X):
        def calculate_zscore(row):
            category = row[self.category_column]
            value = row[self.metric_column]
            zscore = (value - self.mean_by_category_[category]) / self.std_by_category_[category]
            return zscore

        X_transformed = X.copy()
        col_name = f'{self.metric_column}_zscore_by_{self.category_column}'
        X_transformed[col_name] = X_transformed.apply(calculate_zscore, axis=1)
        return X_transformed


# usage inside pipeline:
# ('zscore_sqm_per_canton', ZScoreByCategoryTransformer(metric_column='living_space', category_column='canton')),

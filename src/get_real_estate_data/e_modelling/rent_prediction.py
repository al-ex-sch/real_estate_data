import warnings

import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb

from src.get_real_estate_data.e_modelling.metrics import Metrics
from src.get_real_estate_data.e_modelling.ml_flow_logger import log_model
from src.get_real_estate_data.e_modelling.pipeline_sklearn import PipelineSklearn

warnings.simplefilter(action='ignore', category=FutureWarning)


class RentPrediction:
    def __init__(self, training_cols):
        self.training_cols = training_cols
        self.train_set = None
        self.model = None

    @staticmethod
    def _split_rent_df(df):
        df = df.rename(columns={'price': 'rent', 'price_sqm': 'rent_sqm'})
        X = df.drop(columns=['rent'])
        y = df['rent']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=22)
        train_combined = pd.concat([X_train, y_train], axis=1)
        test_combined = pd.concat([X_test, y_test], axis=1)
        y_train = y_train.reset_index(drop=True)
        y_test = y_test.reset_index(drop=True)
        return df, X_train, X_test, y_train, y_test, train_combined, test_combined

    def _apply_pipeline(self, train_combined, test_combined, df_apt_buy):
        pipe = PipelineSklearn()
        pipeline = pipe.get_pipeline(
            df_apt_buy=df_apt_buy,
            rent_train_X_y=train_combined,
            training_cols=self.training_cols
        )
        X_train_trans = pipeline.fit_transform(train_combined)
        X_test_trans = pipeline.fit_transform(test_combined)

        return X_train_trans, X_test_trans

    def _train_models(self, X_train_trans, y_train, X_test_trans, y_test, log_model_bool, model_name):
        xgb_regressor = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=20,
            random_state=22,
        )
        xgb_metrics = Metrics(
            model=xgb_regressor, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
        )
        xgb_metrics.report()

        if log_model_bool:
            log_model(
                xgb_metrics, model_name, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
            )

        self.model = xgb_regressor
        return xgb_regressor

    @staticmethod
    def _calculate_metrics(df_apt_buy):
        df_apt_buy['annual_rent'] = df_apt_buy['rent_prediction'] * 12
        df_apt_buy['expenses'] = df_apt_buy['annual_rent'] * 0.02  # maintenance, repairs, taxes, insurance
        df_apt_buy['net_profit'] = df_apt_buy['annual_rent'] - df_apt_buy['expenses']
        df_apt_buy['rental_yield'] = (df_apt_buy['net_profit'] / df_apt_buy['price']) * 100
        df_apt_buy['payback_period'] = df_apt_buy['price'] / df_apt_buy['net_profit']
        df_apt_buy = df_apt_buy.sort_values('rental_yield', ascending=False)
        return df_apt_buy

    def _get_apt_buy_df_with_preds(self, model, df_apt_buy_orig, df_apt_rent):
        df_apt_buy = df_apt_buy_orig.copy()
        rent_and_buy_pipe = PipelineSklearn()
        pipeline = rent_and_buy_pipe.get_pipeline(
            df_apt_buy=df_apt_buy,
            rent_train_X_y=df_apt_rent,
            training_cols=self.training_cols,
        )
        # TODO: we will predict on current stock, not full history
        X_apt_buy = pipeline.fit_transform(df_apt_buy)
        y_pred = model.predict(X_apt_buy)
        df_apt_buy['rent_prediction'] = y_pred
        df_apt_buy = self._calculate_metrics(df_apt_buy=df_apt_buy)
        return df_apt_buy

    def run(self, df_apt_buy, df_apt_rent, log_model_bool=False, model_name='model'):
        df_apt_rent, X_train, X_test, y_train, y_test, train_combined, test_combined = self._split_rent_df(df_apt_rent)
        X_train_trans, X_test_trans = self._apply_pipeline(
            train_combined=train_combined, test_combined=test_combined, df_apt_buy=df_apt_buy
        )
        self.train_set = X_train_trans
        model = self._train_models(
            X_train_trans=X_train_trans,
            y_train=y_train,
            X_test_trans=X_test_trans,
            y_test=y_test,
            log_model_bool=log_model_bool,
            model_name=model_name,
        )

        df_buy_with_preds = self._get_apt_buy_df_with_preds(
            model=model, df_apt_buy_orig=df_apt_buy, df_apt_rent=df_apt_rent,
        )

        return df_buy_with_preds

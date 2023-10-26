##
import warnings

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor, VotingRegressor
import xgboost as xgb

from src.get_real_estate_data.e_modelling.metrics import Metrics
from src.get_real_estate_data.e_modelling.ml_flow_logger import log_model
from src.get_real_estate_data.e_modelling.pipeline_sklearn import PipelineSklearn

warnings.simplefilter(action='ignore', category=FutureWarning)


class RentPrediction:
    def __init__(self, training_cols):
        self.training_cols = training_cols
        self.train_set = None

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
        """
        pipeline_sk = PipelineSklearn()
        pipeline = pipeline_sk.get_pipeline(
            df_apt_buy=df_apt_buy,
            rent_train_X_y=train_combined,
            training_cols=self.training_cols,
        )
        """
        X_train_trans = pipeline.fit_transform(train_combined)
        X_test_trans = pipeline.fit_transform(test_combined)

        return X_train_trans, X_test_trans

    @staticmethod
    def _train_models(X_train_trans, y_train, X_test_trans, y_test, log_model_bool, model_name):
        # TODO: simplify, or move to other class
        gb_regressor = GradientBoostingRegressor(n_estimators=100, random_state=22)
        gb_metrics = Metrics(
            model=gb_regressor, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
        )
        gb_metrics.report()

        xgb_regressor = xgb.XGBRegressor(
            objective='reg:squarederror',
            n_estimators=20
        )
        xgb_metrics = Metrics(
            model=xgb_regressor, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
        )
        xgb_metrics.report()

        # TODO: is it fitted when we return it?
        ensemble_model = VotingRegressor(
            estimators=[
                ('xgb', xgb_regressor),
                ('gb', gb_regressor)
            ],
            weights=[0.5, 0.5]
        )
        ensemble_metrics = Metrics(
            model=ensemble_model, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
        )
        ensemble_metrics.report()

        if log_model_bool:
            log_model(
                ensemble_model, model_name, X_train=X_train_trans, y_train=y_train, X_test=X_test_trans, y_test=y_test,
            )
        return ensemble_model

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
            training_cols=self.training_cols
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


apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/full_history_apt_buy_cat.csv'
)
apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/full_history_apt_rent_cat.csv'
)

train_cols = [
    'rooms',
    'living_space',
    'sqm_per_room',
    'page',
    'has_image',
    'date_month',
    'date_year',
    'date_quarter',
    'latitude',
    'longitude',

    'avg_price_sqm_by_canton_room_range',
    'avg_price_sqm_by_canton_living_space_range',
    # 'avg_price_stock_sqm_by_canton_room_range',
    # 'avg_price_stock_sqm_by_canton_living_space_range',
    # 'avg_price_sold_sqm_by_canton_room_range',
    # 'avg_price_sold_sqm_by_canton_living_space_range',

    'count_buy_by_canton_room_range',
    'count_buy_by_canton_living_space_range',
    # 'count_sold_buy_by_canton_room_range',
    # 'count_sold_buy_by_canton_living_space_range',
    # 'count_new_buy_by_canton_room_range',
    # 'count_new_buy_by_canton_living_space_range',
    # 'count_stock_buy_by_canton_room_range',
    # 'count_stock_buy_by_canton_living_space_range',

    'stockturn_buy_by_canton_room_range',
    'stockturn_buy_by_canton_living_space_range',
    'share_new_props_buy_by_canton_room_range',
    'share_new_props_buy_by_canton_living_space_range',

    'avg_net_drops_buy_by_canton_room_range',
    'avg_net_drops_buy_by_canton_living_space_range',
    'avg_net_increases_buy_by_canton_room_range',  # got worse
    'avg_net_increases_buy_by_canton_living_space_range',  # got worse
    'avg_sold_dis_buy_by_canton_room_range',
    'avg_sold_dis_buy_by_canton_living_space_range',
    'avg_stock_dis_buy_by_canton_room_range',
    'avg_stock_dis_buy_by_canton_living_space_range',

    'pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_room_range',
    'pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_living_space_range',



    'avg_rent_sqm_by_canton_room_range',
    'avg_rent_sqm_by_canton_living_space_range',
    # 'avg_rent_stock_sqm_by_canton_room_range',
    # 'avg_rent_stock_sqm_by_canton_living_space_range',
    # 'avg_rent_sold_sqm_by_canton_room_range',
    # 'avg_rent_sold_sqm_by_canton_living_space_range',

    'count_rent_by_canton_room_range',
    'count_rent_by_canton_living_space_range',
    # 'count_sold_rent_by_canton_room_range',
    # 'count_sold_rent_by_canton_living_space_range',
    # 'count_new_rent_by_canton_room_range',
    # 'count_new_rent_by_canton_living_space_range',
    # 'count_stock_rent_by_canton_room_range',
    # 'count_stock_rent_by_canton_living_space_range',

    'stockturn_rent_by_canton_room_range',
    'stockturn_rent_by_canton_living_space_range',
    'share_new_props_rent_by_canton_room_range',
    'share_new_props_rent_by_canton_living_space_range',

    'avg_net_drops_rent_by_canton_room_range',
    'avg_net_drops_rent_by_canton_living_space_range',
    'avg_net_increases_rent_by_canton_room_range',
    'avg_net_increases_rent_by_canton_living_space_range',
    'avg_sold_dis_rent_by_canton_room_range',
    'avg_sold_dis_rent_by_canton_living_space_range',
    'avg_stock_dis_rent_by_canton_room_range',
    'avg_stock_dis_rent_by_canton_living_space_range',

    'ratio_count_stock_rent_vs_buy_by_canton_room_range',
    'ratio_count_new_rent_vs_buy_by_canton_room_range',
    'ratio_count_sold_rent_vs_buy_by_canton_room_range',

    'share_rent_sqm_vs_price_sqm_by_canton_room_range',
    'share_rent_sqm_vs_price_sqm_by_canton_living_space_range',

    'pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_room_range',
    'pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_living_space_range',
]

# dis_sold, last_price (sold price), count sold will make sense once we have more data

rent_prediction = RentPrediction(training_cols=train_cols)
df_buy_pred = rent_prediction.run(df_apt_buy=apt_buy, df_apt_rent=apt_rent)


# TODO: make plots - distribution - profitability by canton, living space range etc.

##

tst = rent_prediction.train_set.copy()

##
import warnings
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import xgboost as xgb


from src.get_real_estate_data.a_helper.config import living_space_ranges
from src.get_real_estate_data.d_modelling.avg_metric_transformer import AverageMetricPerCategory, ColumnKeeper, \
    CountPerCategory
from src.get_real_estate_data.d_modelling.categorizers_transformers import LivingSpaceCategorizer, RoomCategorizer
from src.get_real_estate_data.d_modelling.metrics import Metrics
from src.get_real_estate_data.d_modelling.ml_flow_logger import log_model

warnings.simplefilter(action='ignore', category=FutureWarning)

df_apt_buy = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv', index_col=0)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_rent_new.csv', index_col=0
)


df_apt_rent = df_apt_rent.rename(columns={'price': 'rent', 'price_sqm': 'rent_sqm'})  # TODO: move to preprocessing


def categorize_df():
    dataframes = [df_apt_buy, df_apt_rent]
    upper_limits = [6, 6]
    living_space_keys = ['apartment_buy', 'apartment_rent']
    transformed_dataframes = []

    for df, upper_limit, living_space_key in zip(dataframes, upper_limits, living_space_keys):
        pipeline_cat = Pipeline([
            ('room_categorizer', RoomCategorizer(upper_limit=upper_limit)),
            ('living_space_categorizer',
             LivingSpaceCategorizer(living_space_dict=living_space_ranges, selected_key=living_space_key)),
        ])
        transformed_df = pipeline_cat.fit_transform(df)
        transformed_dataframes.append(transformed_df)

    return transformed_dataframes


df_apt_buy_tr, df_apt_rent_tr = categorize_df()


def split_df(df):
    X = df.drop(columns=['rent'])
    y = df['rent']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.15, random_state=22)
    train_combined = pd.concat([X_train, y_train], axis=1)
    test_combined = pd.concat([X_test, y_test], axis=1)
    y_train = y_train.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    return X_train, X_test, y_train, y_test, train_combined, test_combined


X_train, X_test, y_train, y_test, train_combined, test_combined = split_df(df=df_apt_rent_tr)

training_cols = [
    'rooms', 'living_space', 'sqm_per_room',

    'avg_price_sqm_by_canton_room_range',
    'avg_price_sqm_by_canton_living_space_range',

    'avg_rent_sqm_by_canton_room_range',
    'avg_rent_sqm_by_canton_living_space_range',


    'count_buy_by_canton_room_range',
    'count_buy_by_canton_living_space_range',

    'count_rent_by_canton_room_range',
    'count_rent_by_canton_living_space_range',
]

# transforming rent data

pipeline = Pipeline([
    ('count_buy_by_canton_room_range',
     CountPerCategory(input_df=df_apt_buy_tr, categories=['canton', 'room_range'],
                      new_column_name='count_buy_by_canton_room_range')),
    ('count_buy_by_canton_living_space_range',
     CountPerCategory(input_df=df_apt_buy_tr, categories=['canton', 'living_space_range'],
                      new_column_name='count_buy_by_canton_living_space_range')),

    ('avg_price_sqm_by_canton_room_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price_sqm', categories=['canton', 'room_range'],
                              new_column_name='avg_price_sqm_by_canton_room_range')),
    ('avg_price_sqm_by_canton_living_space_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price_sqm', categories=['canton', 'living_space_range'],
                              new_column_name='avg_price_sqm_by_canton_living_space_range')),

    ('avg_rent_sqm_by_canton_room_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent_sqm', categories=['canton', 'room_range'],
                              new_column_name='avg_rent_sqm_by_canton_room_range')),
    ('avg_rent_sqm_by_canton_living_space_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent_sqm', categories=['canton', 'living_space_range'],
                              new_column_name='avg_rent_sqm_by_canton_living_space_range')),

    ('count_rent_by_canton_room_range',
     CountPerCategory(input_df=train_combined, categories=['canton', 'room_range'],
                      new_column_name='count_rent_by_canton_room_range')),
    ('count_rent_by_canton_living_space_range',
     CountPerCategory(input_df=train_combined, categories=['canton', 'living_space_range'],
                      new_column_name='count_rent_by_canton_living_space_range')),

    # target encoded categorical cols
    ('avg_rent_by_canton',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['canton'],
                              new_column_name='avg_rent_by_canton')),
    ('avg_rent_by_room_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['room_range'],
                              new_column_name='avg_rent_by_room_range')),
    ('avg_rent_by_living_space_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['living_space_range'],
                              new_column_name='avg_rent_by_living_space_range')),

    ('column_keeper', ColumnKeeper(columns_to_keep=training_cols)),
])

X_train_trans = pipeline.fit_transform(train_combined)
X_test_trans = pipeline.fit_transform(test_combined)

##

from sklearn.ensemble import GradientBoostingRegressor

# Train a Gradient Boosting model
gb_regressor = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_metrics = Metrics(gb_regressor, X_train_trans, y_train, X_test_trans, y_test)
gb_metrics.report()

# Train an XGBoost model
xgb_regressor = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=20
)
xgb_metrics = Metrics(xgb_regressor, X_train_trans, y_train, X_test_trans, y_test)
xgb_metrics.report()

##

from sklearn.ensemble import VotingRegressor

# Create an ensemble model
ensemble_model = VotingRegressor(
    estimators=[
        ('xgb', xgb_regressor),
        ('gb', gb_regressor)
    ],
    weights=[0.5, 0.5]  # Optional: Specify weights for the base models
)

# Train the ensemble model and calculate its metrics
ensemble_metrics = Metrics(ensemble_model, X_train_trans, y_train, X_test_trans, y_test)
ensemble_metrics.report()


##

log_model(gb_regressor, "GradientBoostingRegressor", X_train_trans, y_train, X_test_trans, y_test)

##
log_model(xgb_regressor, "XGBRegressor", X_train_trans, y_train, X_test_trans, y_test)


log_model(ensemble_model, "VotingRegressor", X_train_trans, y_train, X_test_trans, y_test)

##
# transforming buy data

pipeline_buy = Pipeline([
    # BUY
    ('count_buy_by_canton_room_range',
     CountPerCategory(input_df=df_apt_buy_tr, categories=['canton', 'room_range'],
                      new_column_name='count_buy_by_canton_room_range')),
    ('count_buy_by_canton_living_space_range',
     CountPerCategory(input_df=df_apt_buy_tr, categories=['canton', 'living_space_range'],
                      new_column_name='count_buy_by_canton_living_space_range')),

    ('avg_price_sqm_by_canton_room_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price_sqm', categories=['canton', 'room_range'],
                              new_column_name='avg_price_sqm_by_canton_room_range')),
    ('avg_price_sqm_by_canton_living_space_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price_sqm', categories=['canton', 'living_space_range'],
                              new_column_name='avg_price_sqm_by_canton_living_space_range')),

    # RENT
    ('count_rent_by_canton_room_range',
     CountPerCategory(input_df=df_apt_rent_tr, categories=['canton', 'room_range'],
                      new_column_name='count_rent_by_canton_room_range')),
    ('count_rent_by_canton_living_space_range',
     CountPerCategory(input_df=df_apt_rent_tr, categories=['canton', 'living_space_range'],
                      new_column_name='count_rent_by_canton_living_space_range')),

    ('avg_rent_sqm_by_canton_room_range',
     AverageMetricPerCategory(input_df=df_apt_rent_tr, metric='rent_sqm', categories=['canton', 'room_range'],
                              new_column_name='avg_rent_sqm_by_canton_room_range')),
    ('avg_rent_sqm_by_canton_living_space_range',
     AverageMetricPerCategory(input_df=df_apt_rent_tr, metric='rent_sqm', categories=['canton', 'living_space_range'],
                              new_column_name='avg_rent_sqm_by_canton_living_space_range')),

    ('avg_rent_by_canton',
     AverageMetricPerCategory(input_df=df_apt_rent_tr, metric='rent', categories=['canton'],
                              new_column_name='avg_rent_by_canton')),
    ('avg_rent_by_room_range',
     AverageMetricPerCategory(input_df=df_apt_rent_tr, metric='rent', categories=['room_range'],
                              new_column_name='avg_rent_by_room_range')),
    ('avg_rent_by_living_space_range',
     AverageMetricPerCategory(input_df=df_apt_rent_tr, metric='rent', categories=['living_space_range'],
                              new_column_name='avg_rent_by_living_space_range')),

    ('column_keeper', ColumnKeeper(columns_to_keep=training_cols)),
])

X_apt_buy = pipeline_buy.fit_transform(df_apt_buy_tr)

##

y_pred = ensemble_model.predict(X_apt_buy)

##

df_apt_buy_tr['prediction'] = y_pred

##


df_apt_buy_tr['annual_rent'] = df_apt_buy_tr['prediction'] * 12
df_apt_buy_tr['expenses'] = df_apt_buy_tr['annual_rent'] * 0.02  # maintenance, repairs, taxes, insurance
df_apt_buy_tr['net_profit'] = df_apt_buy_tr['annual_rent'] - df_apt_buy_tr['expenses']
df_apt_buy_tr['rental_yield'] = (df_apt_buy_tr['net_profit'] / df_apt_buy_tr['price']) * 100
df_apt_buy_tr['roi'] = (df_apt_buy_tr['net_profit'] / df_apt_buy_tr['price']) * 100
df_apt_buy_tr['payback_period'] = df_apt_buy_tr['price'] / df_apt_buy_tr['net_profit']

##

df_apt_buy_tr = df_apt_buy_tr.sort_values('rental_yield', ascending=False)

##

df_apt_buy_tr['link'].head()

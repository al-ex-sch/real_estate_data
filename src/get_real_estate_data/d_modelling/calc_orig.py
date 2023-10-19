##
import warnings
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import xgboost as xgb

from src.get_real_estate_data.a_helper.config import living_space_ranges
from src.get_real_estate_data.d_modelling.avg_metric_transformer import AverageMetricPerCategory, ColumnKeeper
from src.get_real_estate_data.d_modelling.categorizers_transformers import LivingSpaceCategorizer, RoomCategorizer
from src.get_real_estate_data.d_modelling.metrics import Metrics

warnings.simplefilter(action='ignore', category=FutureWarning)

df_apt_buy = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv', index_col=0)
df_house_buy = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_house_buy_new.csv', index_col=0)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_rent_new.csv', index_col=0
)
df_house_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_house_rent_new.csv', index_col=0
)


df_apt_rent = df_apt_rent.rename(columns={'price': 'rent'})  # TODO: move to preprocessing
df_house_rent = df_house_rent.rename(columns={'price': 'rent'})


# TODO: check dict with bounds train_transformed['living_space_range'].value_counts()

def categorize_df():
    dataframes = [df_apt_buy, df_house_buy, df_apt_rent, df_house_rent]
    upper_limits = [6, 6, 6, 6]
    living_space_keys = ['apartment_buy', 'house_buy', 'apartment_rent', 'house_rent']
    transformed_dataframes = []

    for df, upper_limit, living_space_key in zip(dataframes, upper_limits, living_space_keys):
        pipeline_cat = Pipeline([
            ('room_categorizer', RoomCategorizer(upper_limit=upper_limit)),  # TODO: adjust (houses)
            ('living_space_categorizer',
             LivingSpaceCategorizer(living_space_dict=living_space_ranges, selected_key=living_space_key)),  # TODO: adjust
        ])
        transformed_df = pipeline_cat.fit_transform(df)
        transformed_dataframes.append(transformed_df)

    return transformed_dataframes


df_apt_buy_tr, df_house_buy_tr, df_apt_rent_tr, df_house_rent_tr = categorize_df()


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
    # 'canton', 'room_range', 'living_space_range', CATEGORICAL
    'avg_price_by_canton_room_range', 'avg_price_by_canton_living_space_range',
    'avg_rent_by_canton_room_range', 'avg_rent_by_canton_living_space_range',
    'avg_rent_by_canton',
]

# TODO: add feature avg price_sqm by canton and living_space_range/room_range
# TODO: or divide avg_price_by_canton_living_space_range by living_space to get price_sqm


pipeline = Pipeline([
    ('average_price_per_canton_room_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price', categories=['canton', 'room_range'])),
    ('average_price_per_canton_living_space_range',
     AverageMetricPerCategory(input_df=df_apt_buy_tr, metric='price', categories=['canton', 'living_space_range'])),
    ('average_rent_per_canton_room_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['canton', 'room_range'])),
    ('average_rent_per_canton_living_space_range',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['canton', 'living_space_range'])),
    ('average_rent_per_canton',
     AverageMetricPerCategory(input_df=train_combined, metric='rent', categories=['canton'])),
    ('column_keeper', ColumnKeeper(columns_to_keep=training_cols)),
])

X_train_trans = pipeline.fit_transform(train_combined)
X_test_trans = pipeline.fit_transform(test_combined)

xgb_regressor = xgb.XGBRegressor(
    objective='reg:squarederror',
    # learning_rate=0.001,
    n_estimators=100,
    # max_depth=6,
    # min_child_weight=1,
    # gamma=0,
    # subsample=1,
    # colsample_bytree=1,
    # reg_alpha=0,
    # reg_lambda=1
)


##


import matplotlib.pyplot as plt


xgb_regressor.fit(X_train_trans, y_train)

# Plot feature importance
xgb.plot_importance(xgb_regressor, max_num_features=10, importance_type='gain', xlabel='Gain')
plt.title('Feature Importance (Gain)')
plt.show()

xgb.plot_importance(xgb_regressor, max_num_features=10, importance_type='weight', xlabel='Weight')
plt.title('Feature Importance (Weight)')
plt.show()

##

from sklearn.model_selection import RandomizedSearchCV
import numpy as np

param_dist = {
    'n_estimators': np.arange(100, 1000, 50),
    'learning_rate': np.logspace(-3, 0, 10),
    'max_depth': np.arange(1, 11, 1),
    'colsample_bytree': np.arange(0.1, 1.1, 0.1),
    'subsample': np.arange(0.1, 1.1, 0.1),
    'min_child_weight': np.arange(1, 11, 1),
    'gamma': np.logspace(-3, 0, 10),
    'reg_alpha': np.logspace(-3, 0, 10),
    'reg_lambda': np.logspace(-3, 0, 10)
}


n_iter_search = 100  # Number of random combinations to try
random_search = RandomizedSearchCV(
    xgb_regressor,
    param_distributions=param_dist,
    n_iter=n_iter_search,
    cv=5,
    scoring='neg_mean_squared_error',
    n_jobs=-1,
    verbose=2,
    random_state=42
)
random_search.fit(X_train_trans, y_train)
best_params = random_search.best_params_
print(f"Best hyperparameters: {best_params}")

best_xgb_regressor = xgb.XGBRegressor(objective='reg:squarederror', **best_params)

# Recalculate metrics with the tuned model
metrics_tuned = Metrics(best_xgb_regressor, X_train_trans, y_train, X_test_trans, y_test)
metrics_tuned.report()

##

metrics = Metrics(xgb_regressor, X_train_trans, y_train, X_test_trans, y_test)
metrics.report()


##


metrics.plot_residuals()
metrics.plot_true_vs_predicted()

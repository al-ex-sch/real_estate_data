##
import pandas as pd

from scripts.z_training_cols import train_cols
from src.get_real_estate_data.e_modelling.rent_prediction import RentPrediction


apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_buy/'
    '2023-10-21_apartments_buy_full_history_step3.csv'
)
apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_rent/'
    '2023-10-21_apartments_rent_full_history_step3.csv'
)


rent_prediction = RentPrediction(training_cols=train_cols)
df_buy_pred = rent_prediction.run(df_apt_buy=apt_buy, df_apt_rent=apt_rent)


# TODO: make plots - distribution - profitability by canton, living space range etc.

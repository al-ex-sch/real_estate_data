##
import pandas as pd

from src.get_real_estate_data.e_modelling.rent_prediction import RentPrediction, train_cols


apt_rent = pd.read_csv(
    '/data/data_step_3/apartment_rent/2023-10-21_apartments_rent_full_history_step3.csv'
)

apt_buy = pd.read_csv(
    '/data/data_step_3/apartment_buy/2023-10-21_apartments_buy_full_history_step3.csv'
)


embeddings = pd.read_csv('/embeddings.csv')


# combined_apt_buy = pd.concat([apt_buy, apt_buy_enc], axis=1)
combined_apt_rent = pd.concat([apt_rent, embeddings], axis=1)


cols = embeddings.columns.tolist()

train_cols2 = train_cols + cols

##
rent_prediction = RentPrediction(training_cols=train_cols2)
df_buy_pred = rent_prediction.run(df_apt_buy=apt_buy, df_apt_rent=combined_apt_rent)


##


def check_duplicate_columns(df):
    duplicate_columns = df.columns[df.columns.duplicated()]
    if len(duplicate_columns) > 0:
        print(f"Duplicate columns found: {', '.join(duplicate_columns)}")
        return True
    else:
        print("No duplicate columns found.")
        return False


check_duplicate_columns(combined_apt_rent)

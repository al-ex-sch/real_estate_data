##
import pandas as pd

from src.get_real_estate_data.e_modelling.rent_prediction import RentPrediction, train_cols


apt_buy = pd.read_csv(
    '/buy_less_words.csv'
)
apt_rent = pd.read_csv(
    '/rent_less_words.csv'
)

apt_buy_enc = pd.read_csv(
    '/apt_buy_encoded.csv'
)
apt_rent_enc = pd.read_csv(
    '/apt_rent_encoded.csv'
)


# train_cols2 = apt_buy_enc.drop('price', axis=1).columns

apt_buy_enc = apt_buy_enc.drop(['canton', 'new', 'address', 'link'], axis=1)
apt_rent_enc = apt_rent_enc.drop(['canton', 'new', 'address', 'link'], axis=1)

combined_apt_buy = pd.concat([apt_buy, apt_buy_enc], axis=1)
combined_apt_rent = pd.concat([apt_rent, apt_rent_enc], axis=1)


cols = apt_buy_enc.columns.tolist()

train_cols2 = train_cols + cols

##
rent_prediction = RentPrediction(training_cols=train_cols2)
df_buy_pred = rent_prediction.run(df_apt_buy=combined_apt_buy, df_apt_rent=combined_apt_rent)


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

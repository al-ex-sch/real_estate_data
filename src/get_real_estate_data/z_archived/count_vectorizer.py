##
import pandas as pd

from src.get_real_estate_data.e_modelling.rent_prediction import RentPrediction

##
apt_buy = pd.read_csv(
    '/buy_less_words.csv'
)
apt_rent = pd.read_csv(
    '/rent_less_words.csv'
)
words = pd.read_excel(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/words.xlsx'
)

##


def one_hot_encode(df, words):
    one_hot_encoded = pd.DataFrame(index=df.index)

    for word in words["index"]:
        one_hot_encoded[word] = df["text_translated_2"].apply(lambda x: 1 if word in x else 0)

    return one_hot_encoded


apt_buy_encoded = one_hot_encode(apt_buy, words)
apt_rent_encoded = one_hot_encode(apt_rent, words)



##

apt_buy_encoded.to_csv('apt_buy_encoded.csv')
apt_rent_encoded.to_csv('apt_rent_encoded.csv')



##

apt_buy_enc = pd.read_csv(
    '/apt_buy_encoded.csv'
)
apt_rent_enc = pd.read_csv(
    '/apt_rent_encoded.csv'
)

##


apt_buy_enc['price'] = apt_buy_enc['price']
apt_rent_enc['price'] = apt_rent_enc['price']

##


train_cols = apt_buy_enc.columns

rent_prediction = RentPrediction(training_cols=train_cols)
df_buy_pred = rent_prediction.run(df_apt_buy=apt_buy_enc, df_apt_rent=apt_rent_enc)

##

xgb_model = rent_prediction.model

##
importances = xgb_model.feature_importances_
importances_df = pd.DataFrame({'feature': train_cols, 'importance': importances})
importances_df = importances_df.sort_values('importance', ascending=False)

##

importances_df = importances_df[importances_df['importance'] > 0]

##

importances_df.to_csv('importances_df.csv')

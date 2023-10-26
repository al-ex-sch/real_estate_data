##
import pandas as pd

from src.get_real_estate_data.c_preprocessing.text_translator import TextTranslator

df_apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_buy/'
    '2023-10-14_apartments_buy_full_history_step3.csv', index_col=0,
)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_rent/'
    '2023-10-14_apartments_rent_full_history_step3.csv', index_col=0,
)

##

translator = TextTranslator(df=df_apt_buy)
df_apt_buy = translator.translate_column()
df_apt_buy.to_csv('df_apt_buy_full_translated.csv')


translator = TextTranslator(df=df_apt_rent)
df_apt_rent = translator.translate_column()
df_apt_rent.to_csv('df_apt_rent_full_reverse.csv')


##


def split_dfs(df):
    df_sold = df[df['sold'] == 1]
    df_current_stock = df[df['sold'] != 1]
    return df_sold, df_current_stock


sold_buy, stock_buy = split_dfs(df=df_apt_buy)
sold_buy.to_csv('sold_buy.csv')
stock_buy.to_csv('stock_buy.csv')


sold_rent, stock_rent = split_dfs(df=df_apt_rent)
sold_rent.to_csv('sold_rent.csv')
stock_rent.to_csv('stock_rent.csv')

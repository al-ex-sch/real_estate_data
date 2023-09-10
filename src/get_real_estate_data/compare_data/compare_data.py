##
import numpy as np
import pandas as pd
import datetime

pd.options.mode.chained_assignment = None

path = '../../../data/urls_2023-09-09_old.csv'
df = pd.read_csv(path, index_col=False)


df = df.drop('scrape_date', axis=1)

today_date = pd.Timestamp(datetime.date.today())

df['first_date_on_stock'] = '2023-09-08'
df['first price'] = df['price']

yesterday = df[0:5].copy()
today = df[2:7].copy()
today.loc[2, 'price'] = 7777777
today.loc[3, 'price'] = 11


##


def merge_dataframes(yesterday, today):
    merged = pd.merge(yesterday, today, on='property_id', how='outer', suffixes=('_yesterday', '_today'))
    return merged


def remove_duplicate_columns(df):
    for col in df.columns:
        if col.endswith('_yesterday'):
            original_col = col[:-10]
            df[original_col] = df[col]
            df.drop([col, original_col + '_today'], axis=1, inplace=True)
    return df


def find_stock_properties(merged):
    stock = merged[
        (merged['property_id'].isin(yesterday['property_id'])) & (merged['property_id'].isin(today['property_id']))]

    price_changed = stock[stock['price_yesterday'] != stock['price_today']].copy()
    if not price_changed.empty:
        price_changed['price_yesterday'] = price_changed['price_today']

    stock_combined = pd.concat([stock, price_changed], ignore_index=True)
    return remove_duplicate_columns(stock_combined)


def find_new_properties(yesterday, today):
    new_properties = today[~today['property_id'].isin(yesterday['property_id'])]
    return remove_duplicate_columns(new_properties)


def find_sold_properties(yesterday, today):
    sold_properties = yesterday[~yesterday['property_id'].isin(today['property_id'])]
    return remove_duplicate_columns(sold_properties)


def add_stock_columns(stock_properties):
    stock_properties['stock'] = 1
    stock_properties['sold'] = 0
    stock_properties['new'] = 0
    stock_properties['stock_date'] = today_date
    stock_properties['last_date_on_stock'] = np.nan
    stock_properties['last_price'] = np.nan
    stock_properties['dis_sold'] = np.nan
    stock_properties['first_date_on_stock'] = pd.to_datetime(stock_properties['first_date_on_stock'])
    stock_properties['dis_stock'] = (today_date - stock_properties['first_date_on_stock']).dt.days
    return stock_properties


def add_new_columns(new_properties):
    new_properties['stock'] = 0
    new_properties['sold'] = 0
    new_properties['new'] = 1
    new_properties['first_date_on_stock'] = today_date
    new_properties['stock_date'] = today_date
    new_properties['first_price'] = new_properties['price']
    new_properties['last_date_on_stock'] = np.nan
    new_properties['last_price'] = np.nan
    new_properties['dis_sold'] = np.nan
    new_properties['first_date_on_stock'] = pd.to_datetime(new_properties['first_date_on_stock'])
    new_properties['dis_stock'] = (today_date - new_properties['first_date_on_stock']).dt.days
    return new_properties


def add_sold_columns(sold_properties):
    sold_properties['stock'] = 0
    sold_properties['sold'] = 1
    sold_properties['new'] = 0
    sold_properties['stock_date'] = np.nan
    sold_properties['last_date_on_stock'] = today_date
    sold_properties['last_price'] = sold_properties['price']
    sold_properties['first_date_on_stock'] = pd.to_datetime(sold_properties['first_date_on_stock'])
    sold_properties['dis_sold'] = (sold_properties['last_date_on_stock'] - sold_properties['first_date_on_stock']).dt.days
    sold_properties['dis_stock'] = np.nan
    return sold_properties


merged = pd.merge(yesterday, today, on='property_id', suffixes=('_yesterday', '_today'))

stock_properties = find_stock_properties(merged)
new_properties = find_new_properties(yesterday, today)
sold_properties = find_sold_properties(yesterday, today)

stock_properties = add_stock_columns(stock_properties)
new_properties = add_new_columns(new_properties)
sold_properties = add_sold_columns(sold_properties)

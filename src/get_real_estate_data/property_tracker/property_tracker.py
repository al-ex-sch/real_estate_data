##
from typing import Tuple

import pandas as pd
import datetime


class PropertyTracker:
    def __init__(self):
        self.today_date = pd.Timestamp(datetime.date.today())

    @staticmethod
    def _merge_dataframes(yesterday: pd.DataFrame, today: pd.DataFrame) -> pd.DataFrame:
        for df in [yesterday, today]:
            df['property_id'] = df['property_id'].astype(str)
        return pd.merge(yesterday, today, on='property_id', how='outer', suffixes=('_yesterday', '_today'))

    @staticmethod
    def _remove_duplicate_columns(df):
        for col in df.columns:
            if col.endswith('_yesterday'):
                original_col = col[:-10]
                df[original_col] = df[col]
                df = df.drop([col, original_col + '_today'], axis=1)
        return df

    def _find_stock_properties(
            self, merged: pd.DataFrame, yesterday: pd.DataFrame, today: pd.DataFrame,
    ) -> pd.DataFrame:
        stock = merged[
            (merged['property_id'].isin(yesterday['property_id'])) & (merged['property_id'].isin(today['property_id']))
        ]

        prefixes = ['today', 'yesterday']
        for prefix in prefixes:
            stock[f'price_{prefix}'] = pd.to_numeric(stock[f'price_{prefix}'], errors='coerce')

        price_changed = stock[stock['price_yesterday'] != stock['price_today']].copy()
        print(f'Price changed: {price_changed}')

        if not price_changed.empty:
            price_changed['price_yesterday'] = price_changed['price_today']

            stock_combined = pd.concat([stock, price_changed], ignore_index=True)
            stock_combined = self._add_columns(properties=stock_combined, stock=1)

            stock_combined['price_diff'] = stock_combined['price_today'] - stock_combined['price_yesterday']
            stock_combined.loc[stock_combined['price_diff'] < 0, 'drops'] = abs(stock_combined['price_diff'])
            stock_combined.loc[stock_combined['price_diff'] > 0, 'increases'] = stock_combined['price_diff']
            stock_combined = stock_combined.drop('price_diff', axis=1)
        else:
            stock_combined = stock

        stock_combined = self._remove_duplicate_columns(stock_combined)
        return stock_combined

    def _find_new_properties(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> pd.DataFrame:
        new_properties = today[~today['property_id'].isin(yesterday['property_id'])]
        new_properties = self._remove_duplicate_columns(new_properties)
        new_properties = self._add_columns(properties=new_properties, new=1)
        return new_properties

    def _find_sold_properties(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> pd.DataFrame:
        sold_properties = yesterday[~yesterday['property_id'].isin(today['property_id'])]
        sold_properties = self._remove_duplicate_columns(sold_properties)
        sold_properties = self._add_columns(properties=sold_properties, sold=1)
        return sold_properties

    def _add_columns(self, properties: pd.DataFrame, stock: int = 0, sold: int = 0, new: int = 0) -> pd.DataFrame:
        properties['stock'] = stock
        properties['sold'] = sold
        properties['new'] = new

        properties['drops'] = 0
        properties['increases'] = 0

        if stock:
            properties['stock_date'] = pd.to_datetime(self.today_date)
            properties['last_date_on_stock'] = None
            properties['last_price'] = None
            properties['dis_sold'] = None
            properties['first_date_on_stock'] = pd.to_datetime(properties['first_date_on_stock'])
            properties['dis_stock'] = (self.today_date - properties['first_date_on_stock']).dt.days
        elif new:
            properties['first_date_on_stock'] = pd.to_datetime(self.today_date)
            properties['stock_date'] = pd.to_datetime(self.today_date)
            properties['first_price'] = properties['price']
            properties['last_date_on_stock'] = None
            properties['last_price'] = None
            properties['dis_sold'] = None
            properties['dis_stock'] = (pd.to_datetime(self.today_date) - properties['first_date_on_stock']).dt.days

        else:  # sold
            properties['stock_date'] = pd.to_datetime(self.today_date)
            properties['last_date_on_stock'] = pd.to_datetime(self.today_date)
            properties['last_price'] = properties['price']
            properties['first_date_on_stock'] = pd.to_datetime(properties['first_date_on_stock'])
            properties['dis_sold'] = (properties['last_date_on_stock'] - properties['first_date_on_stock']).dt.days
            properties['dis_stock'] = None

        return properties

    def perform_property_tracking(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> Tuple:
        df_merged = self._merge_dataframes(yesterday=yesterday, today=today)
        stock_df = self._find_stock_properties(merged=df_merged, yesterday=yesterday, today=today)
        new_df = self._find_new_properties(yesterday=yesterday, today=today)
        sold_df = self._find_sold_properties(yesterday=yesterday, today=today)
        return stock_df, new_df, sold_df

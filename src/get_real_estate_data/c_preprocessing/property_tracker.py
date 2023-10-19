##
import re
from typing import Tuple
import pandas as pd


class PropertyTracker:
    def __init__(self, file_name: str):
        date_str = re.search(r'\d{4}-\d{2}-\d{2}', file_name).group(0)
        self.today_date = pd.Timestamp(date_str)

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
            ].copy()

        prefixes = ['today', 'yesterday']
        for prefix in prefixes:
            stock[f'price_{prefix}'] = pd.to_numeric(stock[f'price_{prefix}'], errors='coerce')

        price_changed = stock[stock['price_yesterday'] != stock['price_today']].copy()

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
        stock_combined = self._cast_datatypes(df=stock_combined)
        return stock_combined

    def _find_new_properties(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> pd.DataFrame:
        new_properties = today[~today['property_id'].isin(yesterday['property_id'])]
        new_properties = self._remove_duplicate_columns(new_properties)
        new_properties = self._add_columns(properties=new_properties, new=1)
        new_properties = self._cast_datatypes(df=new_properties)
        return new_properties

    def _find_sold_properties(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> pd.DataFrame:
        sold_properties = yesterday[~yesterday['property_id'].isin(today['property_id'])]
        sold_properties = self._remove_duplicate_columns(sold_properties)
        sold_properties = self._add_columns(properties=sold_properties, sold=1)
        sold_properties = self._cast_datatypes(df=sold_properties)
        return sold_properties

    @staticmethod
    def _cast_datatypes(df):  # TODO: do for all columns, replace int64 with int32 and lower
        cols = ['first_price', 'price', 'page']
        for col in cols:
            df[col] = df[col].astype('int64')

        df = df.reset_index(drop=True)
        return df

    def _add_columns(self, properties: pd.DataFrame, stock: int = 0, sold: int = 0, new: int = 0) -> pd.DataFrame:
        properties = properties.copy()
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

    @staticmethod
    def _handle_drops_and_increases(df: pd.DataFrame) -> pd.DataFrame:
        if 'sum_drops' not in df.columns:
            df['sum_drops'] = 0
        if 'sum_increases' not in df.columns:
            df['sum_increases'] = 0

        duplicates = df[df.duplicated('property_id', keep=False)]

        for prop_id in duplicates['property_id'].unique():
            duplicate_rows = duplicates[duplicates['property_id'] == prop_id]

            sum_drops = duplicate_rows.iloc[0]['drops'] + duplicate_rows.iloc[0]['sum_drops']
            sum_increases = duplicate_rows.iloc[0]['increases'] + duplicate_rows.iloc[0]['sum_increases']

            df.loc[df['property_id'] == prop_id, 'sum_drops'] = sum_drops
            df.loc[df['property_id'] == prop_id, 'sum_increases'] = sum_increases

            df.loc[df['property_id'] == prop_id, 'drops'] = duplicate_rows['drops'].values[0]
            df.loc[df['property_id'] == prop_id, 'increases'] = duplicate_rows['increases'].values[0]

        df['net_drops'] = df['sum_drops'] - df['sum_increases']
        df['net_increases'] = 0
        df.loc[df['net_drops'] < 0, 'net_increases'] = abs(df['net_drops'])
        df.loc[df['net_drops'] < 0, 'net_drops'] = 0

        df = df.drop_duplicates('property_id', keep='last')

        return df

    def perform_property_tracking(self, yesterday: pd.DataFrame, today: pd.DataFrame) -> Tuple:
        df_merged = self._merge_dataframes(yesterday=yesterday, today=today)
        stock_df = self._find_stock_properties(merged=df_merged, yesterday=yesterday, today=today)
        new_df = self._find_new_properties(yesterday=yesterday, today=today)
        sold_df = self._find_sold_properties(yesterday=yesterday, today=today)

        stock_df, new_df, sold_df = [self._handle_drops_and_increases(df) for df in [stock_df, new_df, sold_df]]
        return stock_df, new_df, sold_df

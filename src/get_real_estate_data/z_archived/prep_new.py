##
import os

import pandas as pd
from dotenv import load_dotenv

from src.get_real_estate_data.a_helper.config import bounds_outliers, cantons
from src.get_real_estate_data.c_preprocessing.geo_coder import GeoCoder
from src.get_real_estate_data.c_preprocessing.plotter_utils import plot_distribution, plot_all_cantons
from src.get_real_estate_data.c_preprocessing.room_imputer import RoomsImputer

load_dotenv()
geo_api = os.getenv("geo_api")

##

df_apt_buy = pd.read_csv('/2023-10-07_apartments_buy_step1.csv')
df_apt_rent = pd.read_csv(
    '/2023-10-07_apartments_rent_step1.csv'
)


# TODO: check whether all cols have correct data types
class DataCleaner:

    def __init__(self, buy_or_rent, property_type, bounds):
        self.bounds = bounds
        self.current_bounds = self.bounds[f'{property_type}_{buy_or_rent}']
        self.removed = None

    def get_current_bounds(self, key):
        return self.current_bounds[key]

    @staticmethod
    def _calc_cols(df):
        df['price_sqm'] = df['price'] / df['living_space']
        df['sqm_per_room'] = df['living_space'] / df['rooms']
        return df

    @staticmethod
    def _perform_imputing(df):
        rooms_imputer = RoomsImputer(df=df)
        df, imputed_indices = rooms_imputer.impute_rooms(df=df)
        imputed_rows = df.loc[imputed_indices].reset_index(drop=True)
        return df, imputed_rows

    @staticmethod
    def _remove_nans_living_space(df_orig):
        df = df_orig.copy()
        nans = df[df['living_space'].isna()].copy()
        df = df.drop(nans.index).reset_index(drop=True)
        return df, nans

    @staticmethod
    def _handle_outliers(df_orig, column_name, lower_bound, upper_bound):
        df = df_orig.copy()
        outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)].copy()
        df = df.drop(outliers.index).reset_index(drop=True)
        return df, outliers

    @staticmethod
    def _remove_duplicates(df_orig, column_name='property_id'):
        df = df_orig.copy()
        duplicates = df[df.duplicated(subset=column_name, keep='first')]
        df = df.drop(duplicates.index).reset_index(drop=True)
        return df, duplicates

    @staticmethod
    def _remove_rows_with_keywords(df, column, keywords):
        mask = df[column].str.contains('|'.join(keywords), case=False, na=False)
        clean_df = df.loc[~mask]
        removed_rows = df.loc[mask]
        return clean_df, removed_rows

    def perform_data_cleaning(self, df):
        df, nans = self._remove_nans_living_space(df)
        df, imputed_rows = self._perform_imputing(df=df)
        df = self._calc_cols(df=df)

        df, outliers0 = self._handle_outliers(df, 'living_space', *self.get_current_bounds('living_space'))
        df, outliers1 = self._handle_outliers(df, 'sqm_per_room', *self.get_current_bounds('sqm_per_room'))
        df, outliers2 = self._handle_outliers(df, 'price_sqm', *self.get_current_bounds('price_sqm'))
        df, outliers3 = self._handle_outliers(df, 'price', *self.get_current_bounds('price'))
        df, duplicates = self._remove_duplicates(df, column_name='property_id')

        to_remove = [
            'WG Zimmer', 'WG-Zimmer', 'WG-Haus', 'zimmer zu vermieten',
            'room for rent', 'room to rent', 'shared room', 'shared apartment', 'house share', 'flat share',
            'chambre à louer', 'chambre en colocation', 'appartement partagé',
            'stanza in affitto', 'camera in affitto', 'appartamento condiviso',
            'gemeinschaftswohnung', 'mitbewohner', 'mitbewohnerin', 'zimmer in wohngemeinschaft'
        ]
        df, keywords_removed = self._remove_rows_with_keywords(df=df, column='text', keywords=to_remove)
        self.removed = nans, outliers0, outliers1, outliers2, outliers3, duplicates, imputed_rows, keywords_removed
        return df

    @staticmethod
    def perform_geocoding(df):
        geo = GeoCoder(user_agent=geo_api)
        df_processed = geo.process_data(df=df)
        return df_processed

##


def clean_and_export_dataframes(
        df_apt_buy, df_apt_rent, bounds_outliers, export_to_csv=True
):
    def clean_and_save_data(data_cleaner, df, output_filename, export):
        df = data_cleaner.perform_data_cleaning(df=df)
        cleaned_df = data_cleaner.perform_geocoding(df=df)
        if export:
            cleaned_df.to_csv(output_filename)
        return cleaned_df

    data_cleaners = {
        "df_apt_buy_new.csv": DataCleaner(buy_or_rent='buy', property_type='apartment', bounds=bounds_outliers),
        "df_apt_rent_new.csv": DataCleaner(buy_or_rent='rent', property_type='apartment', bounds=bounds_outliers),
    }

    dataframes = {
        "df_apt_buy_new.csv": df_apt_buy,
        "df_apt_rent_new.csv": df_apt_rent,
    }

    cleaned_dataframes = {}

    for output_filename, data_cleaner in data_cleaners.items():
        cleaned_df = clean_and_save_data(
            data_cleaner=data_cleaner,
            df=dataframes[output_filename],
            output_filename=output_filename,
            export=export_to_csv,
        )
        cleaned_dataframes[output_filename] = cleaned_df

    return cleaned_dataframes


cleaned_dfs = clean_and_export_dataframes(
    df_apt_buy, df_apt_rent, bounds_outliers, export_to_csv=True,
)

##

df_apt_buy = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv')
df_apt_rent = pd.read_csv(
    '/2023-10-07_apartments_rent_step1.csv'
)

##

plot_distribution(df_apt_buy, 'price')

##

plot_all_cantons(df=df_apt_buy, cantons=cantons, metric='price')

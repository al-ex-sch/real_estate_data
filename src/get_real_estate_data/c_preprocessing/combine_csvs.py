import os

import pandas as pd
import re


class CombineCSVs:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.property_type = None
        self.buy_or_rent = None

    def _process_csvs(self):
        all_files = [f for f in os.listdir(self.folder_path) if f.endswith('.csv')]
        folder_name = os.path.basename(self.folder_path)
        date, property_type, buy_or_rent = folder_name.split('_')
        self.property_type = property_type
        self.buy_or_rent = buy_or_rent
        combined_df = pd.DataFrame()

        for file in all_files:
            file_path = os.path.join(self.folder_path, file)
            canton = re.search("canton-canton-([a-zA-Z]+)", file).group(1)
            df = pd.read_csv(file_path)
            df['date'] = date
            df['property_type'] = property_type
            df['buy_or_rent'] = buy_or_rent
            df['canton'] = canton
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        return combined_df

    @staticmethod
    def _move_m2_to_living_space(df_orig):
        """
        This function takes a DataFrame and moves the "m²" values from the 'rooms'
        column to the 'living_space' column, converting them to numeric values.

        :param df_orig: Original DataFrame
        :return: Modified DataFrame
        """
        df = df_orig.copy()
        df['temp_living_space'] = df['rooms'].apply(
            lambda x: float(str(x).replace('m²', '').replace(',', '')) if 'm²' in str(x) else None
        )
        df['living_space'] = df['living_space'].apply(
            lambda x: float(str(x).replace('m²', '').replace(',', '')) if 'm²' in str(x) else x
        )
        df['living_space'] = df['temp_living_space'].combine_first(df['living_space'])
        df['rooms'] = df['rooms'].apply(lambda x: None if 'm²' in str(x) else x).astype(float)
        df = df.drop('temp_living_space', axis=1)
        df['living_space'] = df['living_space'].apply(lambda x: str(x).rstrip('²') if '²' in str(x) else x)
        df['living_space'] = pd.to_numeric(df['living_space'], errors='coerce', downcast='integer')
        return df

    def _adjust_price_column(self, df_orig):
        """
        This function takes a DataFrame and extracts the numeric value from the price
        column, which is in the format "1000.– / month" or a plain number like "1000",
        and converts it to integers. It also creates a new column 'frequency' to store
        the value after the slash, if present.

        :param df_orig: Original DataFrame
        :return: Modified DataFrame
        """
        df = df_orig.copy()

        if self.buy_or_rent == 'rent':
            df['frequency'] = df['price'].apply(
                lambda x: x.split(' / ')[1].strip() if isinstance(x, str) and ' / ' in x else None
            )
            df['frequency'] = df['frequency'].fillna('month')
            df = df[df['frequency'] == 'month']

        df['price'] = df['price'].apply(
            lambda x: int(float(x.split(' / ')[0].strip('.– '))) if isinstance(x, str) and ' / ' in x else x
        )
        df['price'] = pd.to_numeric(df['price'], errors='coerce', downcast='integer')
        df = df.dropna(subset=['price']).reset_index(drop=True)
        return df

    def combine_and_preprocess_csvs(self):
        df = self._process_csvs()
        df = self._move_m2_to_living_space(df)
        df = self._adjust_price_column(df_orig=df)
        return df

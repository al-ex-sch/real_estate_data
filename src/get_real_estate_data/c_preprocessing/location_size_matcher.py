import re

import pandas as pd
import numpy as np


class LocationSizeMatcher:
    def __init__(self, cities_df):
        self.cities_df = cities_df
        self.location_size_dict = None

    def _assign_location_size(self):
        self.cities_df['location_size'] = np.where(
            self.cities_df['population'] > 50000, 'big_city',
            np.where(
                self.cities_df['population'] > 25000, 'mid_city',
                np.where(self.cities_df['population'] > 10000, 'town', 'village')
            )
        )

    def _create_location_size_dict(self):
        location_size_dict = {}
        for index, row in self.cities_df.iterrows():
            location_size_dict[row['city']] = row['location_size']
        return location_size_dict

    def _get_location_size(self, address):
        address = re.sub(r'\s*/\s*Bienne', '', address)
        match = re.search(r'\d+\s+([\w\s\.-]+)$', address)
        if match:
            location = match.group(1).strip()
            return self.location_size_dict.get(location, None)
        return None

    @staticmethod
    def _one_hot_encode_location_size(df):
        one_hot = pd.get_dummies(df['location_size'], prefix='location_size')
        df = pd.concat([df, one_hot], axis=1)
        return df

    def match_location_size(self, df):
        self._assign_location_size()
        self.location_size_dict = self._create_location_size_dict()
        df['location_size'] = df['address'].apply(self._get_location_size)
        df['location_size'] = df['location_size'].fillna('village')
        df = self._one_hot_encode_location_size(df=df)
        return df

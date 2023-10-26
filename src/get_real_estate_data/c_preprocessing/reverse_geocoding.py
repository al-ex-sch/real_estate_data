import pandas as pd
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable


class LocationInfo:
    def __init__(self, df, lat_col, lon_col, sleep_time=10):
        self.df = df.copy()
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.geolocator = Nominatim(user_agent="fiksiedfhsi")
        self.sleep_time = sleep_time

    def get_address_components(self, lat, lon, max_retries=2):
        if pd.isna(lat) or pd.isna(lon):
            return {}

        retries = 0
        while retries < max_retries:
            try:
                location = self.geolocator.reverse(f"{lat}, {lon}")
                address = location.raw["address"]
                return address
            except (GeocoderTimedOut, GeocoderUnavailable):
                retries += 1
                time.sleep(self.sleep_time)

        return {}

    @staticmethod
    def apply_location_decision(row):
        if row.get("hamlet") or row.get("village"):
            return "village"
        elif row.get("town"):
            return "town"
        elif row.get("city"):
            return "city"
        else:
            return None

    def apply_location_info(self):
        original_columns = list(self.df.columns)
        for loc_type in ["village", "town", "city"]:
            self.df[loc_type] = None

        for row_number, row in self.df.iterrows():
            print(f"Processing row {row_number}")
            address_components = self.get_address_components(row[self.lat_col], row[self.lon_col])

            loc_decision = self.apply_location_decision(address_components)

            for loc_type in ["village", "town", "city"]:
                self.df.at[row_number, loc_type] = int(loc_decision == loc_type)

            self.df.to_csv('temp_df.csv', index=False)

        desired_columns = original_columns + ["village", "town", "city"]
        result_df = self.df[desired_columns]

        return result_df

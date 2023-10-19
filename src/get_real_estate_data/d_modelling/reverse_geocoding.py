##
import pandas as pd
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut


df_apt_buy = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_buy_new.csv', index_col=0,
)
df_apt_rent = pd.read_csv(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/df_apt_rent_new.csv', index_col=0,
)


class LocationInfo:
    def __init__(self, df, lat_col, lon_col, max_retries=3, sleep_time=1):
        self.df = df.copy()
        self.lat_col = lat_col
        self.lon_col = lon_col
        self.geolocator = Nominatim(user_agent="myGeocoder3")
        self.max_retries = max_retries
        self.sleep_time = sleep_time

    def get_address_components(self, lat, lon):
        if pd.isna(lat) or pd.isna(lon):
            return {}

        retries = 0
        while retries < self.max_retries:
            try:
                location = self.geolocator.reverse(f"{lat}, {lon}")
                address = location.raw["address"]
                return address
            except GeocoderTimedOut:
                retries += 1
                time.sleep(self.sleep_time)

        return {}

    @staticmethod
    def apply_location_decision(row):
        if row["hamlet"] or row["village"]:
            return "village"
        elif row["town"]:
            return "town"
        elif row["city"]:
            return "city"
        else:
            return None

    def apply_location_info(self):
        def get_address_components_with_row_number(row, row_number):
            print(f"Processing row {row_number}")
            return self.get_address_components(row[self.lat_col], row[self.lon_col])

        self.df["address_components"] = self.df.apply(
            lambda row: get_address_components_with_row_number(row, row.name), axis=1
        )

        self.df.to_csv('temp_df.csv')

        address_keys = set()
        for address in self.df["address_components"]:
            address_keys.update(address.keys())

        for key in address_keys:
            self.df[key] = self.df["address_components"].apply(lambda address: address.get(key, None))

        self.df["location_decision"] = self.df.apply(self.apply_location_decision, axis=1)

        for loc_type in ["village", "town", "city"]:
            self.df[loc_type] = (self.df["location_decision"] == loc_type).astype(int)

        original_columns = list(self.df.columns)
        desired_columns = original_columns + ["village", "town", "city"]
        result_df = self.df[desired_columns]

        return result_df


##
location_b = LocationInfo(df_apt_buy, "latitude", "longitude")
df_with_location_b = location_b.apply_location_info()
df_with_location_b.to_csv('df_apt_buy_new2.csv')

##

location_r = LocationInfo(df_apt_rent, "latitude", "longitude")
df_with_location_r = location_r.apply_location_info()
df_with_location_r.to_csv('df_apt_rent_new2.csv')

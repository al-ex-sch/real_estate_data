##
import os

import pandas as pd
from dotenv import load_dotenv
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
from geopy.geocoders import Nominatim

load_dotenv()
geo_api = os.getenv("geo_api")


class GeoCoder:
    def __init__(self, user_agent: str = geo_api):
        """
        A class to handle geocoding tasks using Nominatim.

        :param user_agent: The user agent for Nominatim geocoding service.
        """
        self.geolocator = Nominatim(user_agent=user_agent)

    def _lat_long(self, row: pd.Series) -> pd.Series:
        """
        Add latitude and longitude to the given row using geocoding.

        :param row: A pandas Series containing an "address" key.
        :return: The updated Series with "latitude" and "longitude" keys.
        """
        try:
            loc = self.geolocator.geocode(row["address"])
            row["latitude"] = loc.latitude
            row["longitude"] = loc.longitude
        except (ValueError, AttributeError, GeocoderTimedOut, GeocoderUnavailable):
            pass
        return row

    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process a DataFrame to add latitude and longitude values for each row.

        :param df: A pandas DataFrame containing an "address" column.
        :return: The updated DataFrame with "latitude" and "longitude" columns.
        """
        return df.apply(self._lat_long, axis=1)

##
import os

import pandas as pd
from dotenv import load_dotenv

from src.get_real_estate_data.c_preprocessing.property_tracker import PropertyTracker
from src.get_real_estate_data.c_preprocessing.geo_coder import GeoCoder
from src.get_real_estate_data.c_preprocessing.text_translator import TextTranslator
from src.get_real_estate_data.d_nlp.location_size_matcher import LocationSizeMatcher

load_dotenv()
geo_api = os.getenv("geo_api")


class RunPropertyTracker:

    @staticmethod
    def _combine_dfs(df1, df2):
        df1 = df1[df2.columns]

        combined_rows = df2.values.tolist() + df1.values.tolist()
        combined_df = pd.DataFrame(combined_rows, columns=df2.columns)
        return combined_df

    @staticmethod
    def _combine_sold_dfs(sold_df, first_run, file_path):
        if first_run:
            return sold_df

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        existing_df = pd.read_csv(file_path, usecols=lambda column: column != 'Unnamed: 0')
        combined_df = pd.concat([existing_df, sold_df], axis=0, ignore_index=True)
        return combined_df

    @staticmethod
    def _cast_datatypes(df):
        data_types = {
            'sold': 'Int8',
            'stock': 'Int8',
            'new': 'Int8',
            'page': 'Int8',
            'dis_sold': 'Int16',
            'dis_stock': 'Int16',
            'rooms': 'float16',
            'living_space': 'float16',
            'price_sqm': 'float16',
            'sqm_per_room': 'float16',
            'price': 'Int32',
            'first_price': 'Int32',
            'drops': 'Int32',
            'increases': 'Int32',
            'last_price': 'Int32',
            'sum_drops': 'Int32',
            'sum_increases': 'Int32',
            'net_drops': 'Int32',
            'net_increases': 'Int32',
        }

        for col, dtype in data_types.items():
            df[col] = pd.to_numeric(df[col], errors='coerce').astype(dtype)

        date_cols = [
            'first_date_on_stock',
            'stock_date',
            'last_date_on_stock',
            'date',
        ]

        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')

        df = df.reset_index(drop=True)
        return df

    @staticmethod
    def _save_to_csv(current_properties, sold_df, full_history_df, today_df_path, output_dir):
        if output_dir is None:
            raise ValueError("output_directory must be specified")

        file_prefix = os.path.basename(today_df_path).split('_step')[0]
        current_properties_file = os.path.join(output_dir, f'{file_prefix}_current_stock_step3.csv')
        sold_history_file = os.path.join(output_dir, f'{file_prefix}_sold_history_step3.csv')
        full_history_file = os.path.join(output_dir, f'{file_prefix}_full_history_step3.csv')

        current_properties.to_csv(current_properties_file, index=False)
        sold_df.to_csv(sold_history_file, index=False)
        full_history_df.to_csv(full_history_file, index=False)

    @staticmethod
    def _perform_geocoding(df):
        geo = GeoCoder(user_agent=geo_api)
        df_processed = geo.process_data(df=df)
        return df_processed

    @staticmethod
    def _get_location_size(df):
        matcher = LocationSizeMatcher(cities_df=cities)
        df = matcher.match_location_size(df=df)
        return df

    @staticmethod
    def _perform_translation(df):
        translator = TextTranslator(df)
        df = translator.translate_column()
        return df

    def track_properties(self, today_file, yesterday_file, sold_file_path, output_dir, first_run=False):
        today_df = pd.read_csv(today_file)
        yesterday_df = pd.read_csv(yesterday_file, usecols=lambda column: column != 'Unnamed: 0')

        if first_run:
            yesterday_df['first_date_on_stock'] = yesterday_df['date']
            yesterday_df['first_price'] = yesterday_df['price']

        property_tracker = PropertyTracker(file_name=today_file)
        stock_df, new_df, sold_df = property_tracker.perform_property_tracking(yesterday=yesterday_df, today=today_df)

        if not first_run:
            # only on the new listings
            new_df = self._perform_geocoding(df=new_df)
            new_df = self._get_location_size(df=new_df)
            new_df = self._perform_translation(df=new_df)

        current_properties = self._combine_dfs(df1=new_df, df2=stock_df)
        sold_history_df = self._combine_sold_dfs(sold_df=sold_df, first_run=first_run, file_path=sold_file_path)
        full_history_df = self._combine_dfs(df1=sold_history_df, df2=current_properties)
        current_properties, full_history_df, sold_history_df = [
            self._cast_datatypes(df) for df in [current_properties, full_history_df, sold_history_df]
        ]

        # TODO: make sure full history does not have duplicates

        self._save_to_csv(
            current_properties=current_properties, 
            sold_df=sold_history_df,
            full_history_df=full_history_df,
            today_df_path=today_file,
            output_dir=output_dir,
        )

        return current_properties, sold_df, full_history_df


date_today = '2023-10-21'
date_yesterday = '2023-10-14'

paths = {
    'buy': {
        'today': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_2/apartment_buy/'
                 f'{date_today}_apartments_buy_step2.csv',
        'yesterday': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_buy/'
                     f'{date_yesterday}_apartments_buy_current_stock_step3.csv',
        'sold': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_buy/'
                f'{date_yesterday}_apartments_buy_sold_history_step3.csv',
        'output': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_buy',
    },
    'rent': {
        'today': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_2/apartment_rent/'
                 f'{date_today}_apartments_rent_step2.csv',
        'yesterday': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_rent/'
                     f'{date_yesterday}_apartments_rent_current_stock_step3.csv',
        'sold': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_rent/'
                f'{date_yesterday}_apartments_rent_sold_history_step3.csv',
        'output': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_3/apartment_rent',
    }
}

cities = pd.read_excel(
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/dimensions/cities_ch.xlsx'
)  # TODO: make parameter - input in the class

# choose between: buy, rent
prop_type = 'rent'

prop_track = RunPropertyTracker()
current_stock, sold_history, full_history = prop_track.track_properties(
    today_file=paths[prop_type]['today'],
    yesterday_file=paths[prop_type]['yesterday'],
    sold_file_path=paths[prop_type]['sold'],
    output_dir=paths[prop_type]['output'],
    first_run=False,
)

# TODO: properties that were falsely "sold" (taken from the market) in past
#  and now are newly listed on the market will not have the same id - think about removing duplicates in full history
#  based on unique key made of features (address, canton, living space, rooms)

##
import os

import pandas as pd

from src.get_real_estate_data.c_preprocessing.property_tracker import PropertyTracker


class RunPropertyTracker:

    @staticmethod
    def _combine_current_dfs(new_df, stock_df):
        new_df = new_df[stock_df.columns]

        for col in stock_df.columns:
            new_df[col] = new_df[col].astype(stock_df[col].dtypes)

        combined_rows = stock_df.values.tolist() + new_df.values.tolist()
        combined_df = pd.DataFrame(combined_rows, columns=stock_df.columns)
        return combined_df

    @staticmethod
    def _combine_sold_dfs(sold_df, first_run, file_path):
        if first_run:
            return sold_df

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        existing_df = pd.read_csv(file_path)
        combined_df = pd.concat([existing_df, sold_df], axis=0, ignore_index=True)
        return combined_df

    def track_properties(self, today_file, yesterday_file, sold_file_path, first_run=False):
        today_df = pd.read_csv(today_file)
        yesterday_df = pd.read_csv(yesterday_file)

        if first_run:
            yesterday_df['first_date_on_stock'] = yesterday_df['date']
            yesterday_df['first_price'] = yesterday_df['price']

        property_tracker = PropertyTracker(file_name=today_file)

        stock_df, new_df, sold_df = property_tracker.perform_property_tracking(yesterday=yesterday_df, today=today_df)
        current_properties = self._combine_current_dfs(new_df=new_df, stock_df=stock_df)
        sold_df = self._combine_sold_dfs(sold_df=sold_df, first_run=first_run, file_path=sold_file_path)
        return current_properties, sold_df


today_path = 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-14_apartments_buy_step2.csv'
yest_path = 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-07_apartments_buy_step2.csv'
sold_path = ''


prop_track = RunPropertyTracker()
current_stock, sold_history = prop_track.track_properties(
    today_file=today_path, yesterday_file=yest_path, sold_file_path=sold_path, first_run=True,
)

# TODO: add save to csv to certain directory method

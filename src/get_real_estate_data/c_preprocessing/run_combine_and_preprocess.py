##
import os
from pathlib import Path

from src.get_real_estate_data.a_helper.config import bounds_outliers
from src.get_real_estate_data.c_preprocessing.combine_csvs import CombineCSVs
from src.get_real_estate_data.c_preprocessing.data_cleaner import DataCleaner


class CombineAndPreprocess:
    def __init__(self, paths):
        self.paths = paths

    @staticmethod
    def _process_csvs(path):
        combiner = CombineCSVs(path)
        result = combiner.combine_and_preprocess_csvs()
        return result

    @staticmethod
    def _preprocessing(df, buy_or_rent):
        data_cleaner = DataCleaner(buy_or_rent=buy_or_rent, property_type='apartment', bounds=bounds_outliers)
        df = data_cleaner.perform_data_cleaning(df=df)
        # df = data_cleaner.perform_geocoding(df=df)
        return df

    @staticmethod
    def _create_output_dir(output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    @staticmethod
    def _get_output_path(output_dir, folder_name, file_suffix):
        file_name = folder_name + file_suffix
        output_path = os.path.join(output_dir, file_name)
        return output_path

    def process_and_save(self, output_dir):
        self._create_output_dir(output_dir)

        for path in self.paths:
            print(f"Processing path: {path}")

            if not os.path.exists(path):
                print(f"Path does not exist: {path}")
                continue

            combined_df = self._process_csvs(path)
            folder_name = Path(path).name

            output_path_step1 = self._get_output_path(output_dir, folder_name, '_step1.csv')
            print(f"Saving to: {output_path_step1}")
            combined_df.to_csv(output_path_step1, index=False)

            preprocessed_df = self._preprocessing(combined_df, buy_or_rent="buy" if "buy" in path else "rent")
            output_path_step2 = self._get_output_path(output_dir, folder_name, '_step2.csv')
            print(f"Saving to: {output_path_step2}")
            preprocessed_df.to_csv(output_path_step2, index=False)


paths_list = [
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-14_apartments_buy',
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-14_apartments_rent',
]

dir_out = 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate'

comb_prep = CombineAndPreprocess(paths=paths_list)
comb_prep.process_and_save(output_dir=dir_out)

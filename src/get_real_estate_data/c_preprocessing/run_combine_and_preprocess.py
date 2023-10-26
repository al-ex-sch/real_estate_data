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

    def process_and_save(self):
        for buy_or_rent, buy_or_rent_paths in self.paths.items():
            print(f"Processing {buy_or_rent} data")

            raw_data_path = buy_or_rent_paths['raw_data']
            if not os.path.exists(raw_data_path):
                print(f"Path does not exist: {raw_data_path}")
                continue

            combined_df = self._process_csvs(raw_data_path)
            folder_name = Path(raw_data_path).name

            output_dir_step1 = buy_or_rent_paths['output_step_1']
            self._create_output_dir(output_dir_step1)
            output_path_step1 = self._get_output_path(output_dir_step1, folder_name, '_step1.csv')
            print(f"Saving to: {output_path_step1}")
            combined_df.to_csv(output_path_step1, index=False)

            preprocessed_df = self._preprocessing(combined_df, buy_or_rent=buy_or_rent)
            output_dir_step2 = buy_or_rent_paths['output_step_2']
            self._create_output_dir(output_dir_step2)
            output_path_step2 = self._get_output_path(output_dir_step2, folder_name, '_step2.csv')
            print(f"Saving to: {output_path_step2}")
            preprocessed_df.to_csv(output_path_step2, index=False)


date = '2023-10-21'

paths_dict = {
    'buy': {
        'raw_data': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/raw_data/{date}_apartments_buy',
        'output_step_1': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_1/apartment_buy',
        'output_step_2': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_2/apartment_buy',
    },
    'rent': {
        'raw_data': f'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/raw_data/{date}_apartments_rent',
        'output_step_1': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_1/apartment_rent',
        'output_step_2': 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/data/data_step_2/apartment_rent',
    }
}

comb_prep = CombineAndPreprocess(paths=paths_dict)
comb_prep.process_and_save()

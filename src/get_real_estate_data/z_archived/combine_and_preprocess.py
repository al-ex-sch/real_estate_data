##
import os

from src.get_real_estate_data.a_helper.config import bounds_outliers
from src.get_real_estate_data.c_preprocessing.combine_csvs import CombineCSVs
from src.get_real_estate_data.z_archived.prep_new import DataCleaner


class CombineAndPreprocess:
    def __init__(self, paths):
        self.paths = paths
        self.results = []
        self.folder_names = []

    @staticmethod
    def _process_csvs(path):
        combiner = CombineCSVs(path)
        result = combiner.combine_and_preprocess_csvs()
        return result

    def _save_to_csv(self, index, suffix, output_dir=None, folder_name=None):
        if not folder_name:
            folder_name = os.path.basename(self.paths[index])
        csv_name = f"{folder_name}{suffix}.csv"
        if not output_dir:
            output_dir = os.path.dirname(self.paths[index])  # Use the parent directory as the default output directory
        csv_name = os.path.join(output_dir, csv_name)
        self.results[index].to_csv(csv_name, index=False)
        return folder_name

    def get_combined_csvs(self, output_dir=None):
        """
        step 1
        :param output_dir:
        :return:
        """
        for index, path in enumerate(self.paths):
            result = self._process_csvs(path)
            self.results.append(result)
            folder_name = self._save_to_csv(index=index, suffix='_step1', output_dir=output_dir)
            self.folder_names.append(folder_name)

    @staticmethod
    def _preprocessing(df, buy_or_rent):
        data_cleaner = DataCleaner(buy_or_rent=buy_or_rent, property_type='apartment', bounds=bounds_outliers)
        df = data_cleaner.perform_data_cleaning(df=df)
        df = data_cleaner.perform_geocoding(df=df)
        return df

    def save_preprocessed_dataframes(self, output_dir=None):
        """
        step 2
        :param output_dir:
        :return:
        """
        for index, (df, fold) in enumerate(zip(self.results, self.folder_names)):
            buy_or_rent = 'buy' if 'buy' in fold else 'rent'
            preprocessed_df = self._preprocessing(df=df, buy_or_rent=buy_or_rent)
            self.results[index] = preprocessed_df
            self._save_to_csv(index=index, suffix='_step2', output_dir=output_dir, folder_name=fold)


paths_list = [
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-07_apartments_buy',
    'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/2023-10-07_apartments_rent',
]

output_dir = '/'

comb_prep = CombineAndPreprocess(paths=paths_list)
comb_prep.get_combined_csvs(output_dir=output_dir)

##

comb_prep.save_preprocessed_dataframes()

##

# TODO: how to incorporate current stock and full history (and save to db)
# full data from step 1 will be in csvs (with outliers), clean data from step 2 to db
# result_yes['first_date_on_stock'] = result_yes['date']
# property_tracker = PropertyTracker()
# stock_df, new_df, sold_df = property_tracker.perform_property_tracking(yesterday=result_yes, today=result_today)

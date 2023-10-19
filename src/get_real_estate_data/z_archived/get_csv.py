import os
import pandas as pd


class CSVProcessor:
    def __init__(self, input_folder, output_file, property_type):
        self.input_folder = input_folder
        self.output_file = output_file
        self.property_type = property_type

    @staticmethod
    def extract_canton_from_filename(filename):
        canton = filename.split("_")[0].split("-")[1]
        return canton

    def process_files(self):
        all_files = os.listdir(self.input_folder)
        combined_df = pd.DataFrame()

        for file in all_files:
            if file.endswith(".csv"):
                file_path = os.path.join(self.input_folder, file)
                df = pd.read_csv(file_path)

                canton = self.extract_canton_from_filename(file)
                df['canton'] = canton
                df['property_type'] = self.property_type

                combined_df = combined_df.append(df, ignore_index=True)

        combined_df.to_csv(self.output_file, index=False)


folder_path = '/data/apartments'
output_file_name = 'combined_data.csv'
property_type_name = 'buy_apartment'

csv_processor = CSVProcessor(folder_path, output_file_name, property_type_name)
csv_processor.process_files()

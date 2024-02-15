##
from src.get_real_estate_data.c_preprocessing.combine_and_preprocess import CombineAndPreprocess

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

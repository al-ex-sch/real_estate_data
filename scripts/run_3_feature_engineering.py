##
import pandas as pd

from src.get_real_estate_data.c_preprocessing.run_property_tracker import FeatureEngineering

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
)

# choose between: buy, rent
prop_type = 'rent'

prop_track = FeatureEngineering()
current_stock, sold_history, full_history = prop_track.track_properties(
    today_file=paths[prop_type]['today'],
    yesterday_file=paths[prop_type]['yesterday'],
    sold_file_path=paths[prop_type]['sold'],
    output_dir=paths[prop_type]['output'],
    first_run=False,
    cities=cities,
)

# TODO: properties that were falsely "sold" (taken from the market) in past
#  and now are newly listed on the market will not have the same id - think about removing duplicates in full history
#  based on unique key made of features (address, canton, living space, rooms)

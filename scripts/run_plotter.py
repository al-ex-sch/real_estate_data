##
import pandas as pd

from src.get_real_estate_data.a_helper.config import cantons
from src.get_real_estate_data.c_preprocessing.plotter_utils import plot_distribution, plot_all_cantons

df = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/old_data/df_apt_buy_new.csv')

# choose between: rooms, price_sqm, living_space, price
col_name = 'rooms'

# choose between: single, cantons
plot_type = 'single'

if plot_type == 'single':
    plot_distribution(df, col_name)
else:
    plot_all_cantons(df=df, cantons=cantons, metric=col_name)

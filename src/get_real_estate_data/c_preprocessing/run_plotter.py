##
import pandas as pd

from src.get_real_estate_data.a_helper.config import cantons
from src.get_real_estate_data.c_preprocessing.plotter_utils import plot_distribution, plot_all_cantons

df = pd.read_csv('C:/Users/alexandra.sulcova/PycharmProjects/real_estate/old_data/df_apt_buy_new.csv')

##

to_plot = ['price', 'price_sqm', 'living_space', 'rooms']

plot_distribution(df, 'rooms')


##

plot_all_cantons(df=df, cantons=cantons, metric='price')

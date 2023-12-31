from sklearn.pipeline import Pipeline

from src.get_real_estate_data.e_modelling.groupby_mean_imputer import GroupbyMeanImputer
from src.get_real_estate_data.e_modelling.image_col_transformer import ImageColTransformer
from src.get_real_estate_data.e_modelling.avg_metric_transformer import AverageMetricPerCategory
from src.get_real_estate_data.e_modelling.col_keeper_transformer import ColumnKeeper
from src.get_real_estate_data.e_modelling.count_transformer import CountPerCategory
from src.get_real_estate_data.e_modelling.datetime_features_transformer import DateTimeFeaturesTransformer
from src.get_real_estate_data.e_modelling.imputer import Imputer
from src.get_real_estate_data.e_modelling.pct_diff_transformer import PctDiffTransformer
from src.get_real_estate_data.e_modelling.ratio_transformer import RatioTransformer


class PipelineSklearn:

    @staticmethod
    def get_pipeline(df_apt_buy, rent_train_X_y, training_cols):

        return Pipeline([
            ('impute_df_apt_buy', Imputer(input_df=df_apt_buy, columns_to_impute=['net_drops', 'net_increases'])),
            ('impute_rent_train_X_y',
             Imputer(input_df=rent_train_X_y, columns_to_impute=['net_drops', 'net_increases'])),

            # FEATURES ON BUY DF

            # count listings
            ('count_buy_by_canton_room_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'room_range'],
                              new_column_name='count_buy_by_canton_room_range')),
            ('count_buy_by_canton_living_space_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'living_space_range'],
                              new_column_name='count_buy_by_canton_living_space_range')),

            # avg price
            ('avg_price_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_price_sqm_by_canton_room_range')),
            ('avg_price_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_price_sqm_by_canton_living_space_range')),
            ('avg_price_stock_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_price_stock_sqm_by_canton_room_range',
                                      subset_condition='sold == 0')),
            ('avg_price_stock_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_price_stock_sqm_by_canton_living_space_range',
                                      subset_condition='sold == 0')),
            ('avg_price_sold_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_price_sold_sqm_by_canton_room_range',
                                      subset_condition='sold == 1')),
            ('avg_price_sold_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='price_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_price_sold_sqm_by_canton_living_space_range',
                                      subset_condition='sold == 1')),

            # avg drops and increases
            ('avg_net_drops_buy_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='net_drops',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_net_drops_buy_by_canton_room_range')),
            ('avg_net_drops_buy_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='net_drops',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_net_drops_buy_by_canton_living_space_range')),
            ('avg_net_increases_buy_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='net_increases',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_net_increases_buy_by_canton_room_range')),
            ('avg_net_increases_buy_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='net_increases',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_net_increases_buy_by_canton_living_space_range')),

            # avg sold dis
            ('avg_sold_dis_buy_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='dis_sold', categories=['canton', 'room_range'],
                                      new_column_name='avg_sold_dis_buy_by_canton_room_range',
                                      subset_condition='sold == 1')),
            ('avg_sold_dis_buy_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='dis_sold',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_sold_dis_buy_by_canton_living_space_range',
                                      subset_condition='sold == 1')),
            ('avg_stock_dis_buy_by_canton_room_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='dis_stock', categories=['canton', 'room_range'],
                                      new_column_name='avg_stock_dis_buy_by_canton_room_range',
                                      subset_condition='sold == 0')),
            ('avg_stock_dis_buy_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=df_apt_buy, metric='dis_stock',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_stock_dis_buy_by_canton_living_space_range',
                                      subset_condition='sold == 0')),

            # count new, sold, stock
            ('count_sold_buy_by_canton_room_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'room_range'],
                              new_column_name='count_sold_buy_by_canton_room_range',
                              subset_condition='sold == 1')),
            ('count_sold_buy_by_canton_living_space_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'living_space_range'],
                              new_column_name='count_sold_buy_by_canton_living_space_range',
                              subset_condition='sold == 1')),
            ('count_new_buy_by_canton_room_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'room_range'],
                              new_column_name='count_new_buy_by_canton_room_range',
                              subset_condition='new == 1')),
            ('count_new_buy_by_canton_living_space_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'living_space_range'],
                              new_column_name='count_new_buy_by_canton_living_space_range',
                              subset_condition='new == 1')),
            ('count_stock_buy_by_canton_room_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'room_range'],
                              new_column_name='count_stock_buy_by_canton_room_range',
                              subset_condition='stock == 1')),
            ('count_stock_buy_by_canton_living_space_range',
             CountPerCategory(input_df=df_apt_buy, categories=['canton', 'living_space_range'],
                              new_column_name='count_stock_buy_by_canton_living_space_range',
                              subset_condition='stock == 1')),

            # stockturn
            ('stockturn_buy_by_canton_room_range',
             RatioTransformer(column1='count_sold_buy_by_canton_room_range',
                              column2='count_stock_buy_by_canton_room_range',
                              new_column_name='stockturn_buy_by_canton_room_range')),
            ('stockturn_buy_by_canton_living_space_range',
             RatioTransformer(column1='count_sold_buy_by_canton_living_space_range',
                              column2='count_stock_buy_by_canton_living_space_range',
                              new_column_name='stockturn_buy_by_canton_living_space_range')),
            ('share_new_props_buy_by_canton_room_range',
             RatioTransformer(column1='count_new_buy_by_canton_room_range',
                              column2='count_stock_buy_by_canton_room_range',
                              new_column_name='share_new_props_buy_by_canton_room_range')),
            ('share_new_props_buy_by_canton_living_space_range',
             RatioTransformer(column1='count_new_buy_by_canton_living_space_range',
                              column2='count_stock_buy_by_canton_living_space_range',
                              new_column_name='share_new_props_buy_by_canton_living_space_range')),

            # pct diff
            ('pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_room_range',
             PctDiffTransformer(column1="avg_price_sold_sqm_by_canton_room_range",
                                column2="avg_price_stock_sqm_by_canton_room_range",
                                new_column_name="pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_room_range")),
            ('pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_living_space_range',
             PctDiffTransformer(column1="avg_price_sold_sqm_by_canton_living_space_range",
                                column2="avg_price_stock_sqm_by_canton_living_space_range",
                                new_column_name="pct_diff_avg_buy_sold_vs_stock_sqm_by_canton_living_space_range")),


            # FEATURES ON RENT DF

            ('avg_rent_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm', categories=['canton', 'room_range'],
                                      new_column_name='avg_rent_sqm_by_canton_room_range')),
            ('avg_rent_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_rent_sqm_by_canton_living_space_range')),
            ('avg_rent_stock_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm', categories=['canton', 'room_range'],
                                      new_column_name='avg_rent_stock_sqm_by_canton_room_range',
                                      subset_condition='sold == 0')),
            ('avg_rent_stock_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_rent_stock_sqm_by_canton_living_space_range',
                                      subset_condition='sold == 0')),
            ('avg_rent_sold_sqm_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm', categories=['canton', 'room_range'],
                                      new_column_name='avg_rent_sold_sqm_by_canton_room_range',
                                      subset_condition='sold == 1')),
            ('avg_rent_sold_sqm_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent_sqm',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_rent_sold_sqm_by_canton_living_space_range',
                                      subset_condition='sold == 1')),


            ('count_rent_by_canton_room_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'room_range'],
                              new_column_name='count_rent_by_canton_room_range')),
            ('count_rent_by_canton_living_space_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'living_space_range'],
                              new_column_name='count_rent_by_canton_living_space_range')),

            ('avg_net_drops_rent_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='net_drops',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_net_drops_rent_by_canton_room_range')),
            ('avg_net_drops_rent_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='net_drops',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_net_drops_rent_by_canton_living_space_range')),
            ('avg_net_increases_rent_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='net_increases',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_net_increases_rent_by_canton_room_range')),
            ('avg_net_increases_rent_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='net_increases',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_net_increases_rent_by_canton_living_space_range')),
            ('avg_sold_dis_rent_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='dis_sold',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_sold_dis_rent_by_canton_room_range',
                                      subset_condition='sold == 1')),
            ('avg_sold_dis_rent_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='dis_sold',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_sold_dis_rent_by_canton_living_space_range',
                                      subset_condition='sold == 1')),
            ('avg_stock_dis_rent_by_canton_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='dis_stock',
                                      categories=['canton', 'room_range'],
                                      new_column_name='avg_stock_dis_rent_by_canton_room_range',
                                      subset_condition='sold == 0')),
            ('avg_stock_dis_rent_by_canton_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='dis_stock',
                                      categories=['canton', 'living_space_range'],
                                      new_column_name='avg_stock_dis_rent_by_canton_living_space_range',
                                      subset_condition='sold == 0')),

            # count new, sold, stock
            ('count_sold_rent_by_canton_room_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'room_range'],
                              new_column_name='count_sold_rent_by_canton_room_range',
                              subset_condition='sold == 1')),
            ('count_sold_rent_by_canton_living_space_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'living_space_range'],
                              new_column_name='count_sold_rent_by_canton_living_space_range',
                              subset_condition='sold == 1')),
            ('count_new_rent_by_canton_room_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'room_range'],
                              new_column_name='count_new_rent_by_canton_room_range',
                              subset_condition='new == 1')),
            ('count_new_rent_by_canton_living_space_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'living_space_range'],
                              new_column_name='count_new_rent_by_canton_living_space_range',
                              subset_condition='new == 1')),
            ('count_stock_rent_by_canton_room_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'room_range'],
                              new_column_name='count_stock_rent_by_canton_room_range',
                              subset_condition='stock == 1')),
            ('count_stock_rent_by_canton_living_space_range',
             CountPerCategory(input_df=rent_train_X_y, categories=['canton', 'living_space_range'],
                              new_column_name='count_stock_rent_by_canton_living_space_range',
                              subset_condition='stock == 1')),

            # stockturn
            ('stockturn_rent_by_canton_room_range',
             RatioTransformer(column1='count_sold_rent_by_canton_room_range',
                              column2='count_stock_rent_by_canton_room_range',
                              new_column_name='stockturn_rent_by_canton_room_range')),
            ('stockturn_rent_by_canton_living_space_range',
             RatioTransformer(column1='count_sold_rent_by_canton_living_space_range',
                              column2='count_stock_rent_by_canton_living_space_range',
                              new_column_name='stockturn_rent_by_canton_living_space_range')),
            ('share_new_props_rent_by_canton_room_range',
             RatioTransformer(column1='count_new_rent_by_canton_room_range',
                              column2='count_stock_rent_by_canton_room_range',
                              new_column_name='share_new_props_rent_by_canton_room_range')),
            ('share_new_props_rent_by_canton_living_space_range',
             RatioTransformer(column1='count_new_rent_by_canton_living_space_range',
                              column2='count_stock_rent_by_canton_living_space_range',
                              new_column_name='share_new_props_rent_by_canton_living_space_range')),

            # pct diff
            ('pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_room_range',
             PctDiffTransformer(column1="avg_rent_sold_sqm_by_canton_room_range",
                                column2="avg_rent_stock_sqm_by_canton_room_range",
                                new_column_name="pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_room_range")),
            ('pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_living_space_range',
             PctDiffTransformer(column1="avg_rent_sold_sqm_by_canton_living_space_range",
                                column2="avg_rent_stock_sqm_by_canton_living_space_range",
                                new_column_name="pct_diff_avg_rent_sold_vs_stock_sqm_by_canton_living_space_range")),


            # ratios rent vs buy
            ('ratio_count_stock_rent_vs_buy_by_canton_room_range',
             RatioTransformer(column1='count_stock_rent_by_canton_room_range',
                              column2='count_stock_buy_by_canton_room_range',
                              new_column_name='ratio_count_stock_rent_vs_buy_by_canton_room_range')),
            ('ratio_count_new_rent_vs_buy_by_canton_room_range',
             RatioTransformer(column1='count_new_rent_by_canton_room_range',
                              column2='count_new_buy_by_canton_room_range',
                              new_column_name='ratio_count_new_rent_vs_buy_by_canton_room_range')),
            ('ratio_count_sold_rent_vs_buy_by_canton_room_range',
             RatioTransformer(column1='count_sold_rent_by_canton_room_range',
                              column2='count_sold_buy_by_canton_room_range',
                              new_column_name='ratio_count_sold_rent_vs_buy_by_canton_room_range')),

            # ratios rent_sqm vs price_sqm
            ('share_rent_sqm_vs_price_sqm_by_canton_room_range',
             RatioTransformer(column1='avg_rent_sqm_by_canton_room_range',
                              column2='avg_price_sqm_by_canton_room_range',
                              new_column_name='share_rent_sqm_vs_price_sqm_by_canton_room_range')),
            ('share_rent_sqm_vs_price_sqm_by_canton_living_space_range',
             RatioTransformer(column1='avg_rent_sqm_by_canton_living_space_range',
                              column2='avg_price_sqm_by_canton_living_space_range',
                              new_column_name='share_rent_sqm_vs_price_sqm_by_canton_living_space_range')),


            # target encoded categorical cols
            ('avg_rent_by_canton',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent', categories=['canton'],
                                      new_column_name='avg_rent_by_canton')),
            ('avg_rent_by_room_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent', categories=['room_range'],
                                      new_column_name='avg_rent_by_room_range')),
            ('avg_rent_by_living_space_range',
             AverageMetricPerCategory(input_df=rent_train_X_y, metric='rent', categories=['living_space_range'],
                                      new_column_name='avg_rent_by_living_space_range')),

            ('has_image', ImageColTransformer(column_name="image_url", new_column_name="has_image")),
            ('datetime_features_extractor', DateTimeFeaturesTransformer(datetime_column="date")),
            ("groupby_mean_imputer", GroupbyMeanImputer(groupby_col='canton', impute_cols=['latitude', 'longitude'])),

            ('column_keeper', ColumnKeeper(columns_to_keep=training_cols)),
        ])

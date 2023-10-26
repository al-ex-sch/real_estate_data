from sklearn.pipeline import Pipeline

from src.get_real_estate_data.e_modelling.avg_metric_transformer import AverageMetricPerCategory
from src.get_real_estate_data.e_modelling.col_keeper_transformer import ColumnKeeper
from src.get_real_estate_data.e_modelling.count_transformer import CountPerCategory
from src.get_real_estate_data.e_modelling.imputer import Imputer
from src.get_real_estate_data.e_modelling.ratio_transformer import RatioTransformer


class PipelineSklearn:

    @staticmethod
    def generate_average_metric_steps(input_df, prefix, metrics):
        steps = []

        for metric in metrics:
            steps.extend([
                (f'{prefix}_{metric}_by_canton_room_range',
                 AverageMetricPerCategory(input_df=input_df, metric=metric, categories=['canton', 'room_range'],
                                          new_column_name=f'{prefix}_{metric}_by_canton_room_range')),
                (f'{prefix}_{metric}_by_canton_living_space_range',
                 AverageMetricPerCategory(input_df=input_df, metric=metric, categories=['canton', 'living_space_range'],
                                          new_column_name=f'{prefix}_{metric}_by_canton_living_space_range')),
            ])

        return steps

    @staticmethod
    def generate_count_steps(input_df, prefix, conditions):
        steps = []

        for condition in conditions:
            steps.extend([
                (f'count_{condition}_{prefix}_by_canton_room_range',
                 CountPerCategory(input_df=input_df, categories=['canton', 'room_range'],
                                  new_column_name=f'count_{condition}_{prefix}_by_canton_room_range',
                                  subset_condition=f'{condition} == 1')),
                (f'count_{condition}_{prefix}_by_canton_living_space_range',
                 CountPerCategory(input_df=input_df, categories=['canton', 'living_space_range'],
                                  new_column_name=f'count_{condition}_{prefix}_by_canton_living_space_range',
                                  subset_condition=f'{condition} == 1')),
            ])

        return steps

    @staticmethod
    def generate_ratio_transformer_steps(column1_prefix, column2_prefix, categories):
        steps = []

        for category in categories:
            steps.append((
                f'ratio_{column1_prefix}_vs_{column2_prefix}_by_canton_{category}_range',
                RatioTransformer(
                    column1=f'{column1_prefix}_by_canton_{category}_range',
                    column2=f'{column2_prefix}_by_canton_{category}_range',
                    new_column_name=f'ratio_{column1_prefix}_vs_{column2_prefix}_by_canton_{category}_range',
                )
            ))

        return steps

    def get_pipeline(self, df_apt_buy, rent_train_X_y, training_cols):
        buy_metrics = ['price_sqm', 'net_drops', 'net_increases', 'dis_sold', 'dis_stock']
        rent_metrics = ['rent_sqm', 'net_drops', 'net_increases', 'dis_sold', 'dis_stock']

        buy_average_metric_steps = self.generate_average_metric_steps(df_apt_buy, 'buy', buy_metrics)
        rent_average_metric_steps = self.generate_average_metric_steps(rent_train_X_y, 'rent', rent_metrics)

        buy_count_steps = self.generate_count_steps(df_apt_buy, 'buy', ['new', 'sold', 'stock'])
        rent_count_steps = self.generate_count_steps(rent_train_X_y, 'rent', ['new', 'sold', 'stock'])

        pipeline_steps = [
            ('impute_df_apt_buy', Imputer(input_df=df_apt_buy, columns_to_impute=['net_drops', 'net_increases'])),
            ('impute_rent_train_X_y',
             Imputer(input_df=rent_train_X_y, columns_to_impute=['net_drops', 'net_increases'])),
        ]

        pipeline_steps.extend(buy_average_metric_steps)
        pipeline_steps.extend(rent_average_metric_steps)
        pipeline_steps.extend(buy_count_steps)
        pipeline_steps.extend(rent_count_steps)

        ratio_transformer_steps = self.generate_ratio_transformer_steps('count_rent', 'count_buy',
                                                                        ['stock', 'new', 'sold'])
        pipeline_steps.extend(ratio_transformer_steps)

        pipeline_steps.append(('column_keeper', ColumnKeeper(columns_to_keep=training_cols)))

        return Pipeline(pipeline_steps)

from sklearn.pipeline import Pipeline

from src.get_real_estate_data.a_helper.config import living_space_ranges
from src.get_real_estate_data.c_preprocessing.living_space_categorizer import LivingSpaceCategorizer
from src.get_real_estate_data.c_preprocessing.room_categorizer import RoomCategorizer
from src.get_real_estate_data.c_preprocessing.room_imputer import RoomsImputer


class DataCleaner:

    def __init__(self, buy_or_rent, property_type, bounds):
        self.buy_or_rent = buy_or_rent
        self.bounds = bounds
        self.current_bounds = self.bounds[f'{property_type}_{buy_or_rent}']
        self.removed = None

    def get_current_bounds(self, key):
        return self.current_bounds[key]

    @staticmethod
    def _calc_cols(df):
        df['price_sqm'] = df['price'] / df['living_space']
        df['sqm_per_room'] = df['living_space'] / df['rooms']
        return df

    @staticmethod
    def _perform_imputing(df):
        rooms_imputer = RoomsImputer(df=df)
        df, imputed_indices = rooms_imputer.impute_rooms(df=df)
        imputed_rows = df.loc[imputed_indices].reset_index(drop=True)
        return df, imputed_rows

    @staticmethod
    def _remove_nans_living_space(df_orig):
        df = df_orig.copy()
        nans = df[df['living_space'].isna()].copy()
        df = df.drop(nans.index).reset_index(drop=True)
        return df, nans

    @staticmethod
    def _handle_outliers(df_orig, column_name, lower_bound, upper_bound):
        df = df_orig.copy()
        outliers = df[(df[column_name] < lower_bound) | (df[column_name] > upper_bound)].copy()
        df = df.drop(outliers.index).reset_index(drop=True)
        return df, outliers

    @staticmethod
    def _remove_duplicates(df_orig, column_name='property_id'):
        df = df_orig.copy()
        duplicates = df[df.duplicated(subset=column_name, keep='first')]
        df = df.drop(duplicates.index).reset_index(drop=True)
        return df, duplicates

    @staticmethod
    def _remove_rows_with_keywords(df, column, keywords):
        mask = df[column].str.contains('|'.join(keywords), case=False, na=False)
        clean_df = df.loc[~mask]
        removed_rows = df.loc[mask]
        return clean_df, removed_rows

    def _categorize_rooms_and_living_space(self, df):
        living_space_key = 'apartment_buy' if self.buy_or_rent == 'buy' else 'apartment_rent'

        pipeline_cat = Pipeline([
            ('room_categorizer', RoomCategorizer(upper_limit=6)),
            ('living_space_categorizer',
             LivingSpaceCategorizer(living_space_dict=living_space_ranges, selected_key=living_space_key)),
        ])
        transformed_df = pipeline_cat.fit_transform(df)
        return transformed_df

    def perform_data_cleaning(self, df):
        df, nans = self._remove_nans_living_space(df)
        df, imputed_rows = self._perform_imputing(df=df)
        df = self._calc_cols(df=df)

        df, outliers0 = self._handle_outliers(df, 'living_space', *self.get_current_bounds('living_space'))
        df, outliers1 = self._handle_outliers(df, 'sqm_per_room', *self.get_current_bounds('sqm_per_room'))
        df, outliers2 = self._handle_outliers(df, 'price_sqm', *self.get_current_bounds('price_sqm'))
        df, outliers3 = self._handle_outliers(df, 'price', *self.get_current_bounds('price'))
        df, duplicates = self._remove_duplicates(df, column_name='property_id')

        to_remove = [
            'WG Zimmer', 'WG-Zimmer', 'WG-Haus', 'zimmer zu vermieten',
            'room for rent', 'room to rent', 'shared room', 'shared apartment', 'house share', 'flat share',
            'chambre à louer', 'chambre en colocation', 'appartement partagé',
            'stanza in affitto', 'camera in affitto', 'appartamento condiviso',
            'gemeinschaftswohnung', 'mitbewohner', 'mitbewohnerin', 'zimmer in wohngemeinschaft'
        ]
        df, keywords_removed = self._remove_rows_with_keywords(df=df, column='text', keywords=to_remove)
        self.removed = nans, outliers0, outliers1, outliers2, outliers3, duplicates, imputed_rows, keywords_removed
        df = self._categorize_rooms_and_living_space(df=df)
        return df

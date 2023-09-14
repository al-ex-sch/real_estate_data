import pandas as pd


class SplitFeatures:
    """
    A class used to split and process features and main_info columns in a DataFrame.
    """

    @staticmethod
    def _process_features_furnishings(df: pd.DataFrame) -> pd.DataFrame:
        """
        Split and process the features_furnishings column into separate columns in the DataFrame.

        :param df: Input DataFrame with a features_furnishings column.
        :return: DataFrame with processed features_furnishings columns.
        """
        df['features_furnishings'] = df['features_furnishings'].apply(lambda x: x.split(', ') if pd.notna(x) else [])
        dummy_features = df['features_furnishings'].apply(pd.Series).stack().str.get_dummies().groupby(level=0).sum()
        df = pd.concat([df, dummy_features], axis=1)
        for col in dummy_features.columns:
            df[col] = df[col].astype(pd.Int64Dtype())
        return df

    @staticmethod
    def _process_main_info(df: pd.DataFrame) -> pd.DataFrame:
        """
        Split and process the main_info column into separate columns in the DataFrame.

        :param df: Input DataFrame with a main_info column.
        :return: DataFrame with processed main_info columns.
        """
        def process_row(row):
            attributes = row.split(', ')
            data = {key.strip(): value.strip() for key, value in (attribute.split(': ') for attribute in attributes)}
            return data

        main_info = pd.DataFrame(df['main_info'].apply(process_row).tolist())
        df = pd.concat([df, main_info], axis=1)
        return df

    @staticmethod
    def _rename_cols(df):
        """
        Rename DataFrame columns to a standardized format.

        :param df: Input DataFrame.
        :return: DataFrame with renamed columns.
        """
        df.columns = [
            col.lower().replace('.', '').replace(' / ', '_').replace('-', '_').replace(' ', '_') for col in df.columns
        ]
        return df

    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Process the input DataFrame, split and process features_furnishings and main_info columns.

        :param df: Input DataFrame with features_furnishings and main_info columns.
        :return: Processed DataFrame with separate columns for features_furnishings and main_info.
        """
        df = self._process_features_furnishings(df=df)
        df = self._process_main_info(df=df)
        df = self._rename_cols(df=df)
        return df

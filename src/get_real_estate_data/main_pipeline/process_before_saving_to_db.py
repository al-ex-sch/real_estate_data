from typing import Dict

import pandas as pd


class ProcessBeforeSavingToDb:
    @staticmethod
    def _add_missing_columns(df: pd.DataFrame, cols_n_datatypes: Dict[str, str]) -> pd.DataFrame:
        """
        Add missing columns to the DataFrame and fill them with None.

        :param df: The input DataFrame.
        :param cols_n_datatypes: The dictionary of columns and their respective data types.
        :return: The DataFrame with all columns from the cols_n_datatypes dictionary.
        """
        column_names = list(cols_n_datatypes.keys())
        df = df.reindex(columns=column_names, fill_value=None)
        return df

    @staticmethod
    def _enforce_data_types(df: pd.DataFrame, cols_n_datatypes: Dict[str, str]) -> pd.DataFrame:
        """
        Enforce the correct data types for the columns in the DataFrame.

        :param df: The input DataFrame.
        :return: The DataFrame with the enforced data types.
        """
        for col_name, datatype in cols_n_datatypes.items():
            if col_name in df.columns:
                if datatype.lower().startswith('varchar'):
                    df[col_name] = df[col_name].astype(str)
                elif 'int' in datatype.lower():
                    df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
                    df[col_name] = df[col_name].apply(lambda x: None if pd.isna(x) else int(x))
                elif 'boolean' in datatype.lower():
                    df[col_name] = df[col_name].astype(bool)
                elif 'date' in datatype.lower():
                    df[col_name] = pd.to_datetime(df[col_name], errors='coerce').dt.date
                    df[col_name] = df[col_name].apply(lambda x: None if pd.isna(x) else x)
                elif 'timestamp' in datatype.lower():
                    df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
                    df[col_name] = df[col_name].apply(lambda x: None if pd.isna(x) else x)
                elif 'float' in datatype.lower() or 'real' in datatype.lower():
                    df[col_name] = df[col_name].astype(float)
        return df

    def perform_preprocessing(self, df: pd.DataFrame, cols_n_datatypes: Dict) -> pd.DataFrame:
        df = self._add_missing_columns(df=df, cols_n_datatypes=cols_n_datatypes)
        df = self._enforce_data_types(df=df, cols_n_datatypes=cols_n_datatypes)
        return df

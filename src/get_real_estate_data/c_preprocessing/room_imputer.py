import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor


class RoomsImputer:
    def __init__(self, df):
        self.model = self._fit_living_space_to_rooms_model(df)

    @staticmethod
    def _fit_living_space_to_rooms_model(df):
        non_null_data = df.dropna(subset=['living_space', 'rooms'])
        X = non_null_data[['living_space']].to_numpy()
        y = non_null_data['rooms']

        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X, y)
        return model

    def _living_space_imputer(self, living_space):
        if np.isnan(living_space):
            return None

        rooms = self.model.predict([[living_space]])[0]
        return round(2 * rooms) / 2

    def impute_rooms(self, df):
        imputed_indices = []
        for index, row in df.iterrows():
            if pd.isna(row['rooms']):
                imputed_value = self._living_space_imputer(row['living_space'])
                df.at[index, 'rooms'] = imputed_value
                imputed_indices.append(index)
        return df, imputed_indices

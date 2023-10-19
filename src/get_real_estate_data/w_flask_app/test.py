##
import geopandas as gpd
import numpy as np
import pandas as pd


path_municipalities = '/src/get_real_estate_data/w_flask_app/gemeinden-geojson.geojson'
gdf_municipalities = gpd.read_file(path_municipalities)
df_municipalities = pd.DataFrame(gdf_municipalities)
random_floats_municipalities = np.random.uniform(200, 500, len(df_municipalities))
df_municipalities['avg_rent'] = random_floats_municipalities
# gdf_municipalities = gpd.GeoDataFrame(df_municipalities, geometry='geometry', crs="EPSG:4326")


path_cantons = '/src/get_real_estate_data/w_flask_app/canton_geojson.json'
gdf_cantons = gpd.read_file(path_cantons)
df_cantons = pd.DataFrame(gdf_cantons)
random_floats_cantons = np.random.uniform(200, 500, len(df_cantons))
df_cantons['avg_rent'] = random_floats_cantons
# gdf_cantons = gpd.GeoDataFrame(df_cantons, geometry='geometry', crs="EPSG:4326")


##
df_municipalities['avg_rent_m'] = df_municipalities['avg_rent']
df_municipalities['geometry_m'] = df_municipalities['geometry']
df_cantons['avg_rent_c'] = df_cantons['avg_rent']
df_cantons['geometry_c'] = df_cantons['geometry']

merged = df_municipalities.merge(df_cantons[['id', 'name', 'geometry_c', 'avg_rent_c']], how='left', left_on='kanton.KUERZEL', right_on='id')

##

merged.to_csv('cant_muni.csv')

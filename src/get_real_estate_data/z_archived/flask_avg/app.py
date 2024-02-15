from flask import Flask
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip

path = '/cant_muni.csv'
df = pd.read_csv(path)
gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")


def create_map(gdf):
    swiss_map = folium.Map(location=[46.8182, 8.2275], zoom_start=8)
    color_scale = folium.LinearColormap(['green', 'yellow', 'red'], vmin=gdf['avg_rent_m'].min(),
                                        vmax=gdf['avg_rent_m'].max())
    municipalities = folium.GeoJson(
        gdf,
        style_function=lambda feature: {
            'fillColor': color_scale(feature['properties']['avg_rent_m']),
            'fillOpacity': 0.7,
            'color': 'black',
            'weight': 1,
        },
        tooltip=GeoJsonTooltip(
            fields=['gemeinde.NAME', 'avg_rent_m'],
            aliases=['Municipality Name', 'Average Rent'],
            localize=True,
        ),
    )
    municipalities.add_to(swiss_map)
    color_scale.add_to(swiss_map)
    color_scale.caption = 'Average Rent'
    return swiss_map


app = Flask(__name__)


@app.route('/')
def index():
    swiss_map = create_map(gdf)
    return swiss_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)



"""
now what it does is that it plots a map with different shades for each municipality based on avg rent.  
  
here are the columns of the dataframe. 'gemeinde.BFS_NUMMER', 'gemeinde.NAME', 'kanton.KUERZEL', 'kanton.NAME',  
       'geometry', 'avg_rent', 'avg_rent_m', 'geometry_m', 'id', 'name',  
       'geometry_c', 'avg_rent_c'  
  
_c is for cantons and _m is for municipality.   
  
the problem is that the data is loading very slowly, since there are a lot of municipalities. what i want is to load the map with the shadings for cantons, and when i click a certain canton, it will zoom on the canton and then the shaded municipalities will appear for that canton.  
  
so that instead of loading municipalities for all cantons, we will load only municipalities of the canton the user will click on 
"""

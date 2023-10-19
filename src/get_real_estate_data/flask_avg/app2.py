import numpy as np
from flask import Flask, render_template
import pandas as pd
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from shapely.geometry import Polygon, MultiPolygon

path = 'C:/Users/alexandra.sulcova/PycharmProjects/real_estate/cant_muni.csv'
df = pd.read_csv(path)


def remove_z_coordinate(geometry):
    if isinstance(geometry, Polygon):
        return Polygon(geometry.exterior.coords[:-1])
    elif isinstance(geometry, MultiPolygon):
        polygons = [Polygon(p.exterior.coords[:-1]) for p in geometry]
        return MultiPolygon(polygons)


df['geometry'] = df['geometry'].apply(remove_z_coordinate)

gdf = gpd.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")

# Group the data by cantons
cantons_data = gdf.groupby('kanton.KUERZEL').agg(
    avg_rent_c=('avg_rent', 'mean'),
    geometry_c=('geometry', 'first'),
    name=('kanton.NAME', 'first')
).reset_index()

# Create a new GeoDataFrame from cantons_data
cantons_gdf = gpd.GeoDataFrame(cantons_data, geometry='geometry_c', crs="EPSG:4326")

# Calculate the centroid for each canton
cantons_gdf['centroid'] = cantons_gdf['geometry_c'].centroid


def create_map(gdf, cantons_data=None):
    swiss_map = folium.Map(location=[46.8182, 8.2275], zoom_start=8)

    if cantons_data is not None:
        # Add choropleth layer
        folium.Choropleth(
            geo_data=gdf,
            data=cantons_data,
            columns=['kanton.KUERZEL', 'avg_rent_c'],
            key_on='properties.kanton.KUERZEL',
            fill_color='YlOrRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Average Rent by Canton',
        ).add_to(swiss_map)

        # Add clickable markers for each canton
        for _, row in cantons_gdf.iterrows():
            if row['centroid'] is not None:
                marker = folium.Marker(
                    location=[row['centroid'].y, row['centroid'].x],
                    popup=f"{row['name']} ({row['kanton.KUERZEL']})",
                    icon=None
                )
                marker.add_child(folium.Popup(row['name']))
                marker.add_to(swiss_map)

                # Add a script to handle the click event and load the municipalities
        script = f"""  
            <script>  
                function onCantonClick(kanton) {{  
                    window.location.href = '/municipalities/' + kanton;  
                }}  
            </script>  
        """
        swiss_map.get_root().header.add_child(folium.Element(script))

    return swiss_map


app = Flask(__name__)


@app.route('/')
def index():
    swiss_map = create_map(gdf=None, cantons_data=cantons_gdf)
    return swiss_map._repr_html_()


@app.route('/municipalities/<kanton>')
def municipalities(kanton):
    # Filter the data for the given canton
    canton_gdf = gdf[gdf['kanton.KUERZEL'] == kanton]

    # Create a map with the municipalities of the canton
    canton_map = create_map(canton_gdf)
    return canton_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)

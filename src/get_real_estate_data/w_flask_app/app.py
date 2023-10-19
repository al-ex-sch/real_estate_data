from flask import Flask, render_template, request
import pandas as pd
import folium
import geopandas as gpd
from folium.plugins import MarkerCluster
import json

app = Flask(__name__)


def topojson_to_geojson(topojson_file):
    with open(topojson_file, 'r', encoding='utf-8') as file:
        topojson_data = json.load(file)
    return json.loads(gpd.read_file(json.dumps(topojson_data)).to_json())


custom_css = """    
<style>    
    .marker-cluster:hover,    
    .marker-cluster:hover div,    
    .marker-cluster:hover span {    
        background-color: transparent !important;    
        border-color: transparent !important;    
        color: transparent !important;    
    }    
</style>   
"""


@app.route("/", methods=["GET", "POST"])
def home():
    rent_apartment = pd.read_csv("C:/Users/alexandra.sulcova/PycharmProjects/real_estate/output.csv")
    rent_apartment = rent_apartment.dropna(subset='latitude')

    swiss_map = folium.Map(location=[46.8, 8.33], zoom_start=8)

    topojson_file = '/src/get_real_estate_data/w_flask_app/muni_topo.json'
    cantons_topojson_file = '/src/get_real_estate_data/w_flask_app/cantons_topo.json'

    municipalities_geojson = topojson_to_geojson(topojson_file)
    cantons_geojson = topojson_to_geojson(cantons_topojson_file)

    folium.GeoJson(
        data=municipalities_geojson,
        name='Municipalities',
        style_function=lambda x: {'color': 'grey', 'weight': 1, 'fillOpacity': 0},
        highlight_function=lambda x: {'weight': 2, 'fillOpacity': 0.1},
        smooth_factor=0.1,
    ).add_child(folium.GeoJsonTooltip(fields=['kanton.NAME'])).add_to(swiss_map)

    custom_marker_cluster = """    
    function(cluster) {    
        var childCount = cluster.getChildCount();    
        var color = 'black';    
        return L.divIcon({    
            html: '<div style="background-color:rgba(0, 0, 0, 0.5); color:white; border-radius:50%; width: 30px; height: 30px; line-height: 30px; text-align: center;"><span>' + childCount + '</span></div>',    
            className: 'marker-cluster'    
        });    
    }    
    """

    marker_cluster = MarkerCluster(icon_create_function=custom_marker_cluster).add_to(swiss_map)
    properties = rent_apartment
    markers = []  # Add this line
    for index, row in properties.iterrows():
        marker = folium.Marker(
            location=[row["latitude"], row["longitude"]],
            tooltip=f"{row['address']} - {row['price']} CHF",
            popup=f"<a href='{row['link']}' target='_blank'>View details</a>",
        )
        marker.add_to(marker_cluster)
        markers.append(marker)  # Add this line

    for feature in cantons_geojson['features']:
        canton_id = feature['properties']['id']
        canton_properties = rent_apartment[rent_apartment['canton'] == canton_id]

        feature['id'] = canton_id

        folium.GeoJson(
            data=feature,
            style_function=lambda x: {'color': 'black', 'weight': 1.5, 'fillOpacity': 0},
            highlight_function=lambda x: {'color': 'grey', 'weight': 1.5, 'fillColor': 'grey', 'fillOpacity': 0.5},
            smooth_factor=0.1,
            zoom_on_click=True,
        ).add_child(
            folium.GeoJsonTooltip(fields=['name'], style="font-family: Arial; color: black; font-size: 14px;")).add_to(
            swiss_map)

    swiss_map.get_root().header.add_child(folium.Element(custom_css))
    swiss_map.save("templates/map.html")

    swiss_map.get_root().header.add_child(folium.Element('<script>initMapListeners();</script>'))

    marker_coords = [[row["latitude"], row["longitude"]] for _, row in properties.iterrows()]
    return render_template("index.html", properties=properties, marker_coords=marker_coords)


if __name__ == "__main__":
    app.run(debug=True)

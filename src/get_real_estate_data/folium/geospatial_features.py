##
import pandas as pd
from geopy.geocoders import Nominatim

file_path = '/data/detail_listings_2023-09-10_all.csv'
data = pd.read_csv(file_path, index_col=False)
data = data[~data['address'].isna()]


geolocator = Nominatim(user_agent="pandasprechti@gmail.com")


def lat_long(row):
    try:
        loc = geolocator.geocode(row["address"])
        row["latitude"] = loc.latitude
        row["longitude"] = loc.longitude
    except:
        pass
    return row


data = data.apply(lat_long, axis=1)

# TODO: try out different geocoders, this one has a lot of nans


data = data[~(data['longitude'].isna())]
data = data[~(data['latitude'].isna())]

from flask import Flask, render_template
import folium

app = Flask(__name__)


@app.route('/')
def index():
    # Create a map with markers using Folium (use the previous examples)
    map = folium.Map(location=[37.421999, -122.084057], zoom_start=13)

    # Add markers and popups to the map, but also add a unique ID to each marker
    for i, (_, row) in enumerate(data.iterrows()):
        lat, long = row['latitude'], row['longitude']
        popup_content = f"Feature 1: {row['price']}<br>Feature 2: {row['advertiser']}<br>Feature 3: {row['address']}"
        popup = folium.Popup(popup_content, max_width=250, show=True)
        icon = folium.DivIcon(icon_size=(0, 0), icon_anchor=(0, 0), html=f'<div id="marker_{i}"></div>')
        marker = folium.Marker([lat, long], popup=popup, icon=icon)
        marker.add_to(map)

        # Render the map as an HTML string
    map_html = map._repr_html_()

    # Pass the map HTML and the property data to the template
    return render_template('index.html', map_html=map_html, properties=data, enumerate=enumerate)


if __name__ == '__main__':
    app.run(debug=True)

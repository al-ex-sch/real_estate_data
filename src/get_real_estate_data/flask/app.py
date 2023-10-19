from flask import Flask, render_template
import pandas as pd
import folium
from folium.plugins import MarkerCluster

df = pd.read_csv("C:/Users/alexandra.sulcova/PycharmProjects/real_estate/output.csv")
df = df.dropna(subset=['latitude'])

df_houses = pd.read_csv("C:/Users/alexandra.sulcova/PycharmProjects/real_estate/output_houses.csv")
df_houses = df_houses.dropna(subset=['latitude'])

app = Flask(__name__)


@app.route('/')
def index():
    m = folium.Map(location=[46.8182, 8.2275], zoom_start=8)

    marker_cluster = MarkerCluster().add_to(m)

    for idx, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=f"Price: {row['price']}<br>Rooms: {row['rooms']}<br>Living Space: {row['living_space']}",
            icon=None,
        ).add_to(marker_cluster)

    marker_coords = df[['latitude', 'longitude']].values.tolist()

    return render_template("map_template.html", map=m._repr_html_(), listings=df.to_dict(orient='records'),
                           marker_coords=marker_coords, house_listings=df_houses.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)

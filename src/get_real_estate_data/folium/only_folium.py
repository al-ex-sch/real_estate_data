import folium

# Create a map centered at the first pair of coordinates in your data
latitude, longitude = data_ll.loc[0, ['latitude', 'longitude']]
map = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add markers to the map using the latitude, longitude, and property features
for _, row in data_ll.iterrows():
    lat, long = row['latitude'], row['longitude']

    # Customize the popup content with your property features
    popup_content = f"Feature 1: {row['price']}<br>Feature 2: {row['address']}<br>Feature 3: {row['living_area']}"

    # Create a popup with the content, and set the options to show on hover
    popup = folium.Popup(popup_content, max_width=250, show=True)

    # Add the marker with the popup to the map
    folium.Marker([lat, long], popup=popup).add_to(map)

# Save the map as an HTML file
map.save("map.html")
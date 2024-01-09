import streamlit as st
import pandas as pd
import geopandas as gpd
import folium

# Load the data from the CSV file
file_path = 'path/to/your/file.csv'
data = pd.read_csv(file_path)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(data, geometry=gpd.GeoSeries.from_wkt(data['geo_shape_2d']))

# Create a map centered around Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Add all project polygons to the map using the same color (red)
for idx, row in gdf.iterrows():
    folium.GeoJson(row['geometry'], name=row['NAAMPROJECT'], style_function=lambda x: {'fillColor': 'red'}).add_to(m)

# Display the map using Streamlit
folium_static(m)

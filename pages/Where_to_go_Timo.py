import streamlit as st
import geopandas as gpd
import folium
from shapely.geometry import Polygon
import ast

# Read the dataset into a GeoDataFrame
# Replace 'path_to_your_file.csv' with the actual path to your dataset
data = gpd.read_file('./data/Timo_Where_to_go.csv')

# Convert the coordinates to Shapely Polygon geometries
data['geometry'] = data['geo_shape'].apply(lambda x: Polygon(ast.literal_eval(x)['coordinates'][0]))

# Create a GeoDataFrame with the geometry
gdf = gpd.GeoDataFrame(data, geometry='geometry')

# Create a folium map centered around Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Add GeoJSON layer to the map
folium.GeoJson(gdf).add_to(m)

# Streamlit app
st.title('Map of Eindhoven with Project Areas')

# Display the map in Streamlit using folium
st.markdown(m._repr_html_(), unsafe_allow_html=True)

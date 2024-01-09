import streamlit as st
import geopandas as gpd
import folium
import pandas as pd

# Assuming your data is in a variable called 'data'
# Load your data into a GeoDataFrame
gdf = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Create a unique list of project names
unique_projects = gdf['NAAMPROJECT'].unique()

# Let the user choose a project to display
selected_project = st.selectbox('Select a project', unique_projects)

# Filter the GeoDataFrame based on the selected project
selected_data = gdf[gdf['NAAMPROJECT'] == selected_project]

# Create a map centered around Eindhoven
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Add polygons to the map for the selected project
for idx, row in selected_data.iterrows():
    folium.GeoJson(row['geo_shape'], name=row['NAAMPROJECT']).add_to(m)

# Display the map using Streamlit
folium_static(m)

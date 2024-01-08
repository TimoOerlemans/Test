import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json

# Read the dataset
data = pd.read_csv('./data/Timo_Where_to_go.csv')

# Initialize the map
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Define a function to add polygons to the map based on filter
def add_polygons(df, selected_filter):
    filtered_data = df[df['PROJECTFASE'] == selected_filter]
    for index, row in filtered_data.iterrows():
        try:
            geo_shape = json.loads(row['geo_shape'])
            coordinates = geo_shape['coordinates']

            # Add polygon to the map
            folium.Polygon(
                locations=coordinates[0],
                color='red',  # Change color based on conditions
                fill=True,
                fill_color='red',  # Change color based on conditions
                fill_opacity=0.4,
                popup=row['NAAMPROJECT']
            ).add_to(m)
        except Exception as e:
            st.write(f"Error adding polygon for {row['NAAMPROJECT']}: {e}")

# Sidebar filter
selected_filter = st.sidebar.selectbox('Select Filter', data['PROJECTFASE'].unique())

# Add polygons to the map based on the selected filter
add_polygons(data, selected_filter)

# Display the map
st.header("Map of Eindhoven with Filters")
st.markdown("Interactive map showing different areas based on filters.")
folium_static(m)

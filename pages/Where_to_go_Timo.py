import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Show unique values of PRIJSKLASSE
unique_prices = data['PRIJSKLASSE'].unique()
price_checkboxes = {price: st.sidebar.checkbox(f"Toon '{price}' projects", value=True) for price in unique_prices}

# Show unique values of NAAMPROJECT
unique_projects = data['NAAMPROJECT'].unique()
project_checkboxes = {project: st.sidebar.checkbox(f"Toon '{project}' projects", value=True) for project in unique_projects}

# Show unique naamprojecten and their coordinates at the top
unique_projects = data[['NAAMPROJECT', 'geo_point_2d']].drop_duplicates()
project_list = st.empty()  # Placeholder to dynamically update the list

# Function to update the displayed projects based on checkboxes
def update_displayed_projects():
    filtered_data = data.copy()
    for project, checkbox in project_checkboxes.items():
        if not checkbox:
            filtered_data = filtered_data[filtered_data['NAAMPROJECT'] != project]

    for price, checkbox in price_checkboxes.items():
        if not checkbox:
            filtered_data = filtered_data[filtered_data['PRIJSKLASSE'] != price]
    return filtered_data

# Kaart van Eindhoven initialiseren
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Function to update the list of projects
def update_project_list():
    displayed_projects = update_displayed_projects()
    project_list.markdown("### Unieke Naamprojecten en Coördinaten")
    project_list.write(displayed_projects[['NAAMPROJECT', 'geo_point_2d']].drop_duplicates())

# Update displayed projects and list
update_project_list()

# Add markers for project locations
for index, row in data.iterrows():
    coordinates_str = row['geo_point_2d']

    # Convert the string representation to latitude and longitude
    try:
        # Assuming the coordinates are a list of [latitude, longitude]
        coordinates = [float(coord) for coord in coordinates_str.split(',')]
        latitude, longitude = coordinates[0], coordinates[1]
    except Exception as e:
        print(f"Error converting coordinates: {e}")
        continue

    # Add a marker for each project at its location if it's in the filtered data
    if row['PRIJSKLASSE'] in price_checkboxes and price_checkboxes[row['PRIJSKLASSE']] \
       and row['NAAMPROJECT'] in project_checkboxes and project_checkboxes[row['NAAMPROJECT']]:
        folium.Marker(
            location=[latitude, longitude],
            popup=row['NAAMPROJECT'],
            icon=folium.Icon(color='red', icon='circle')
        ).add_to(m)

# Weergeven van de kaart in Streamlit
st.header("Kaart van Eindhoven met rode punten voor elk project")
st.markdown("Elk punt vertegenwoordigt een naamproject in de dataset.")
folium_static(m)

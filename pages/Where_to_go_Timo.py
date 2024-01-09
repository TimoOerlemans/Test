import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Show unique naamprojecten and their coordinates at the top
unique_projects = data[['NAAMPROJECT', 'geo_point_2d']].drop_duplicates()
project_list = st.empty()  # Placeholder to dynamically update the list

# Function to update the displayed projects based on checkboxes
def update_displayed_projects():
    filtered_data = pd.DataFrame()
    if show_in_ontwikkeling and show_gereed:
        filtered_data = data  # Show all projects if both are selected
    elif show_in_ontwikkeling:
        filtered_data = data[data['PROJECTFASE'] == 'In ontwikkeling']
    elif show_gereed:
        filtered_data = data[data['PROJECTFASE'] == 'Gereed']
    return filtered_data

# Checkbox for 'In ontwikkeling' projects
show_in_ontwikkeling = st.sidebar.checkbox("Toon 'In Ontwikkeling' projecten")

# Checkbox for 'Gereed' projects
show_gereed = st.sidebar.checkbox("Toon 'Gereed' projecten")

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
    if row['PROJECTFASE'] == 'In ontwikkeling' and show_in_ontwikkeling:
        folium.Marker(
            location=[latitude, longitude],
            popup=row['NAAMPROJECT'],
            icon=folium.Icon(color='red', icon='circle')
        ).add_to(m)
    elif row['PROJECTFASE'] == 'Gereed' and show_gereed:
        folium.Marker(
            location=[latitude, longitude],
            popup=row['NAAMPROJECT'],
            icon=folium.Icon(color='red', icon='circle')
        ).add_to(m)

# Weergeven van de kaart in Streamlit
st.header("Kaart van Eindhoven met rode punten voor elk project")
st.markdown("Elk punt vertegenwoordigt een naamproject in de dataset.")
folium_static(m)

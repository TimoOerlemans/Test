import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Show unique naamprojecten and their coordinates at the top
unique_projects = data[['NAAMPROJECT', 'geo_point_2d']].drop_duplicates()

st.header("Unieke Naamprojecten en Coördinaten")
st.write(unique_projects)

# Checkbox to filter by projectfase
show_only_selected_phase = st.sidebar.checkbox("Toon alleen 'In Ontwikkeling' of 'Gereed' projecten")

# Kaart van Eindhoven initialiseren
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Filter based on checkbox selection
if show_only_selected_phase:
    filtered_data = data[data['PROJECTFASE'].isin(['In ontwikkeling', 'Gereed'])]
else:
    filtered_data = data

# Itereren over de dataset om gebieden toe te voegen als rode polygoon op de kaart
for index, row in filtered_data.iterrows():
    coordinates_str = row['geo_point_2d']

    # Convert the string representation to a list of coordinates
    try:
        # Assuming the coordinates are a list of [latitude, longitude]
        coordinates = [float(coord) for coord in coordinates_str.split(',')]
        coordinates = [(coordinates[1], coordinates[0])]  # Reformat to [latitude, longitude] pairs
    except Exception as e:
        print(f"Error converting coordinates: {e}")
        continue

    # Polygoon toevoegen aan de kaart als een rode zone met projectnaam als popup
    folium.Polygon(
        locations=coordinates,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.4,  # Reduced opacity for better visualization of overlapping areas
        popup=row['NAAMPROJECT']
    ).add_to(m)

# Weergeven van de kaart in Streamlit
st.header("Kaart van Eindhoven met rode gebieden voor elk project")
st.markdown("Elk gebied vertegenwoordigt een naamproject in de dataset.")
folium_static(m)

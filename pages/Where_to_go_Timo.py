import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Drop rows with NaN values in 'PRIJSKLASSE', 'PROJECTFASE', and 'WONINGTYPE' columns
columns_to_check = ['PRIJSKLASSE', 'PROJECTFASE', 'WONINGTYPE']
data = data.dropna(subset=columns_to_check)

# Generate unique values for filters
unique_prijsklasse = data['PRIJSKLASSE'].unique()
unique_projectfase = data['PROJECTFASE'].unique()
unique_woningtype = data['WONINGTYPE'].unique()

# Filter projects based on selected filters
selected_prijsklasse = st.multiselect('Selecteer prijsklasse', list(unique_prijsklasse))
selected_projectfase = st.multiselect('Selecteer projectfase', list(unique_projectfase))
selected_woningtype = st.multiselect('Selecteer woningtype', list(unique_woningtype))

# Filter the data based on selected filters
filtered_data = data.copy()
filtered_data = filtered_data[
    (filtered_data['PRIJSKLASSE'].isin(selected_prijsklasse)) &
    (filtered_data['PROJECTFASE'].isin(selected_projectfase)) &
    (filtered_data['WONINGTYPE'].isin(selected_woningtype))
]

# Create columns layout
col1, col2 = st.columns([1, 3])  # Adjust column ratios as needed

# Show filters in the first column
with col1:
    st.header('Filters')
    st.write("Filter by Prijsklasse")
    selected_prijsklasse = st.multiselect("Select Prijsklasse", list(unique_prijsklasse))

    st.write("Filter by Projectfase")
    selected_projectfase = st.multiselect("Select Projectfase", list(unique_projectfase))

    st.write("Filter by Woningtype")
    selected_woningtype = st.multiselect("Select Woningtype", list(unique_woningtype))

# Show the map and list in the second column
with col2:
    # Show the map with markers
    m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

    # Add markers for project locations based on filtered data
    for index, row in filtered_data.iterrows():
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
        folium.Marker(
            location=[latitude, longitude],
            popup=row['NAAMPROJECT'],
            icon=folium.Icon(color='lightred', icon='circle', prefix='fa', opacity=0.6, icon_size=(10, 10),
                             shadow=False)  # Set shadow to False
        ).add_to(m)

    st.header("Kaart van Eindhoven met rode gebieden voor elk project")
    st.markdown("Elk gebied vertegenwoordigt een naamproject in de dataset.")
    folium_static(m)

    # Show the list of filtered data
    st.header('Filtered Projectenlijst')
    st.dataframe(filtered_data)

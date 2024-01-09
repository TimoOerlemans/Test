import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Kaart van Eindhoven initialiseren
m = folium.Map(location=[51.4416, 5.4697], zoom_start=12)

# Voeg een selectiebox toe om projectfasen te filteren
selected_phase = st.sidebar.selectbox('Selecteer projectfase', data['PROJECTFASE'].unique())

# Filter de dataset op basis van geselecteerde fase
filtered_data = data[data['PROJECTFASE'] == selected_phase]

# Itereren over de dataset om gebieden toe te voegen als rode polygoon op de kaart
for index, row in data.iterrows():
    coordinates_str = row['geo_point_2d']

    # Try to convert the string representation to a list of coordinates
    try:
        coordinates = eval(coordinates_str)
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

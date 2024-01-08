import folium
import pandas as pd

# Assuming 'data' holds your complete dataset as a list of dictionaries

# Sample data (part of your dataset)
data = [
    {
        "NAAMPROJECT": "Van Hogendorplaan 1",
        "geometry": [[[5.508, 51.456], [5.508, 51.455], [5.508, 51.455], [5.508, 51.456]]],
        # Add other properties...
    },
    {
        "NAAMPROJECT": "Demer 47",
        "geometry": [[[5.477, 51.439], [5.477, 51.439], [5.477, 51.439], [5.477, 51.439]]],
        # Add other properties...
    },
    # Add more data...
]

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Create a folium map centered in Eindhoven
m = folium.Map(location=[51.44, 5.48], zoom_start=13)

# Add markers for each data point
for index, row in df.iterrows():
    folium.Polygon(
        locations=row['geometry'],
        popup=row['NAAMPROJECT'],
        color='red',  # Initial color
        fill=True,
        fill_color='red',  # Initial fill color
        fill_opacity=0.7,
    ).add_to(m)

# Display the map
m.save('map_with_filters.html')
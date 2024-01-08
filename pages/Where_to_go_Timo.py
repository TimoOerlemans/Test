import pandas as pd
import folium
from ast import literal_eval

# Load your dataset into a Pandas DataFrame
# Replace 'path_to_your_file' with the actual path to your dataset
data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Create a map centered around Eindhoven
eindhoven_map = folium.Map(location=[51.4416, 5.4697], zoom_start=13)

# Iterate through the dataset to add polygons for each area with its name
for index, row in data.iterrows():
    # Adjust these variables based on your dataset's column names
    project_name = row['NAAMPROJECT']
    coordinates = literal_eval(row['geo_shape'])['coordinates'][0]  # Extract coordinates
    coordinates = [[coord[1], coord[0]] for coord in coordinates]  # Reformat for folium

    # Create a polygon for each area
    folium.Polygon(locations=coordinates, color='red', popup=project_name).add_to(eindhoven_map)

# Display the map
eindhoven_map.save("eindhoven_areas_map.html")

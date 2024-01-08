import streamlit as st
import pandas as pd
import ast

# Assuming 'data' is your dataset containing the project information
# Replace 'path_to_your_file.csv' with the actual path to your dataset
data = pd.read_csv('path_to_your_file.csv')

# Extracting unique NAAMPROJECT values and their coordinates
unique_projects = data.groupby('NAAMPROJECT')['geo_shape'].apply(list).reset_index()

# Function to extract coordinates from the GeoJSON-like structure
def extract_coordinates(geo_shape):
    return ast.literal_eval(geo_shape[0])['coordinates'][0]

# Extracting coordinates from the GeoJSON-like structure
unique_projects['Coordinates'] = unique_projects['geo_shape'].apply(extract_coordinates)

# Displaying the table with NAAMPROJECT and Coordinates using st.table
st.table(unique_projects[['NAAMPROJECT', 'Coordinates']])

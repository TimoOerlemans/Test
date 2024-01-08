import streamlit as st
import pandas as pd

# Assuming 'data' is your dataset containing the project information
# Replace 'path_to_your_file.csv' with the actual path to your dataset
data = pd.read_csv('./data/Timo_Where_to_go.csv', sep=';')

# Show unique NAAMPROJECT values in a table
unique_projects = data['NAAMPROJECT'].unique()
unique_projects_df = pd.DataFrame({'Unique NAAMPROJECT': unique_projects})
st.write(unique_projects_df)
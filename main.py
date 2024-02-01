import streamlit as st
import numpy as np
import pandas as pd
import folium
from streamlit_folium import st_folium
import ast
import os
import streamlit_authenticator as stauth
from datetime import datetime


def writeToCat():
    with open("DataHolder/categories.csv", "w") as category_file:
        for category in categories:
            category_file.write(category + ",")


def writeToNames():
    with open("DataHolder/AquascopeDataFileNames.csv", "w") as station_file:
        for station in station_names:
            station_file.write(station + ",")

#Select which dataset to look at
dataFileNames = pd.read_csv('DataHolder/AquascopeDataFileNames.csv')
stationNames = pd.read_csv('DataHolder/testfile.csv')
categories = pd.read_csv('DataHolder/categories.csv')


#map
st.title("Water Clarity Program")
m = folium.Map(location=[51.538270867171455, -0.0160315323514259], zoom_start=12)

stationNames = stationNames.reset_index()

# Iterate through the DataFrame and add markers
for index, row in stationNames.iterrows():
    location = ast.literal_eval(row['Location'])
    popup_text = row['Description']
    tooltip_text = row['Station Code']

    folium.Marker(location, popup=popup_text, tooltip=tooltip_text).add_to(m)


st_data = st_folium(m, width=750) #End map making here

station_codes = stationNames['Station Code'].tolist()

selected_sation = st.selectbox('Select station', station_codes)
selected_categories = st.multiselect('Select categories', categories.columns)
print("Selected Station: ", selected_sation)
print("Selected Categories: ", selected_categories)

data_directory = "AquascopeData"
# Create empty lists to store categories and station names
categories = []
station_names = []

# Iterate through the files in the directory
for filename in os.listdir(data_directory): #Pseudocode
    if filename.endswith(".csv"):
        # Split the filename into [category] and [stationName].csv
        category, x = filename.split("_")
        station = filename


        # Append the category and station name to their respective lists
        if category not in categories:
            categories.append(category)


        if station not in station_names:
            station_names.append(station)

# Write the categories to a text file
writeToCat()


# Write the station names to a text file
writeToNames()


incremental = -1
all_relevant = []
col_names = ['dates']
for i in dataFileNames: #Iterating through every data file in the directory
    incremental += 1
    for j in range(len(selected_categories)): #For each selected caterogy
        startFrom = -1*len(selected_sation+".csv") #
        print("StartFrom: ", startFrom)
        endHere = len(str(dataFileNames.columns[incremental])) - len(selected_sation+"_.csv") #determine the station's location based on the naming conventions
        print("EndHere: ", endHere, " ", dataFileNames.columns[incremental])

        print("\n E1 ", str(dataFileNames.columns[incremental])[startFrom:-4], " =? ", selected_sation)
        print("E2", str(dataFileNames.columns[incremental])[:endHere], " =? ", selected_categories[j])

        if str(dataFileNames.columns[incremental])[startFrom:-4] == selected_sation and str(dataFileNames.columns[incremental])[:endHere] == selected_categories[j]:
            all_relevant.append(pd.read_csv('AquascopeData/' + str(dataFileNames.columns[incremental])))
            col_names.append(str(dataFileNames.columns[incremental])[:endHere])

for i in range(len(all_relevant)): #createa a single large dataframe
    all_relevant[i].columns = ['dates', col_names[i+1]]

try:
    final_df = all_relevant[0]

    for df in all_relevant[1:]:
        final_df = final_df.merge(df, on='dates', how='right')

    st.line_chart(final_df, x='dates', y=None)
    st.write(final_df) #create the chart using a single dataframe comprised of all others
except:
    pass #error handling



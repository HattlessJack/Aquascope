import streamlit as st
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import pandas as pd
import csv
import os
from datetime import datetime

def tryWriteStation():
        stationData = [StationName, StationPos, StationDesc]

        if newStationCheck == True:
            with open('DataHolder/testfile.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(stationData)
                file.close()
            with open("DataHolder/log.txt", "w") as file:
                file.write(str(datetime.now()) + ": " + str(name) + " added a new station named: " + str(StationName) + " at [" + str(StationPos) + "]")
                file.close()

def tryWriteData():  #Add the new data to the directiory if the file's name follows the naming convention
    if newDataCheck == True and Data.name[-1 * (len(DataStationName) + 4): -4] == DataStationName:

        file_path = os.path.join('AquascopeData', Data.name) #Create the file path

        with open(file_path, "wb") as f: #Add the given csv file to the directory
            f.write(Data.read())
            print("Uploaded!")

        with open("DataHolder/log.txt", "w") as file: #Make a reccord of this in the log
            file.write(str(datetime.now()) + " :" + str(name) + " entered a new csv file named: " + str(Data.name))
            file.close()

def createUser():
    if newUserCheck == True:
        one_pw = []
        one_pw.append(user_password)
        hashed_pw = stauth.Hasher(one_pw).generate()
        # Open a file with access mode 'a'
        file_object = open('DataHolder/users.txt', 'a')
        # Append data of that user at the end of file
        file_object.write(user_name + ", " + user_username + ", " + hashed_pw[0] + "\n")
        # Close the file
        file_object.close()

        with open("DataHolder/log.txt", "w") as file:
            file.write(str(datetime.now()) + " :" + str(name) + " created new user named: " + str(user_name) + "-" + str(user_username) + ". Is admin = " + str(isAdmin))
            file.close()

    if isAdmin == True:
        with open ('DataHolder/admins.txt', 'r') as file:
            contents = file.read()

        contents = contents.rstrip("\n")
        contents += "," + user_username

        with open("DataHolder/admins.txt", "w") as file:
            file.write(contents)

        print("DONNNNNNNE")

# open admins
admins = []
filename = "DataHolder/admins.txt"
with open(filename, "r") as file:
    line = file.readlines()

    for l in line:
        items = line[0].split(',')

    items[-1] = items[-1].rstrip('\n')

    admins = items

    print(admins)

# User authentication
users = []
filename = "DataHolder/users.txt"
with open(filename, "r") as file:
    lines = file.readlines()

    for l in lines:
        # split every line and every comma
        d = l.strip("\n").split(", ")

        #  append each user info (name, username, password) to users list
        users.append(d)

# create the credentials "dictionary" and add all usernames, names and passwords in three separate credentials
credentials = {"usernames": {}}
for u in users:
    credentials["usernames"][u[1]] = {}
    credentials["usernames"][u[1]]["name"] = u[0]
    credentials["usernames"][u[1]]["password"] = u[2]


authenticator = stauth.Authenticate(credentials,
                                    "Admin page", "KittyKittyCat", cookie_expiry_days=14)


name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status: #Make stuff happen here
    if username in admins:
        st.title(f"Welcome Esteemed {name} 👑")
        authenticator.logout("Logout", "sidebar")

        with st.expander("Enter New Data :bookmark_tabs:"): #Add new data to the program while pairing it up to a station
            stationNames = pd.read_csv('DataHolder/testfile.csv')
            DataStationName = st.selectbox("Enter Station Name:", stationNames['Station Code'])
            Data = st.file_uploader("Enter Data CSV file:", type=['.csv'], accept_multiple_files = False)
            newDataCheck = st.checkbox("I have verified that all the inputs are correct.", key = "newDataCheck")
            st.button("Submit", on_click=tryWriteData, key = "newDataSubmit")

        with st.expander("Enter New Station :factory:"):
            StationName = st.text_input("Enter Station Name:", key = "StationName")
            StationDesc = st.text_input("Enter Description of Station:", key = "StationDesc")
            StationPos = "[" + st.text_input("Enter Coordonates (North, East)", key = "StationPos") + "]"
            newStationCheck = st.checkbox("I have verified that all inputs are correct.")
            st.button("Submit", on_click=tryWriteStation)

        with st.expander("Enter New User :bust_in_silhouette:"): #Add a new user
            user_name = st.text_input("Enter user's name") #name
            user_username = st.text_input("Enter user's username") #username
            user_password = st.text_input("Enter user's password") #password
            isAdmin = st.checkbox("The user is an admin", key ="newUserAdminCheck") #Are they an admin Y/N?
            newUserCheck = st.checkbox("I have verified that all the inputs are correct.", key ="newUserCheck")
            st.button("Create user", on_click=createUser, key = "AdminButtonUserAdd")

        with open("DataHolder/log.txt", "r") as file:
            log_data = file.read()
            print("WEEEE: " + log_data)
            st.download_button(label="Download logs", data=log_data, file_name='AquascopeAppLogs.txt')

    else:
        dataDisabled = True

        st.title(f"Welcome {name}")
        authenticator.logout("Logout", "sidebar")


        with st.expander("Enter New Data :bookmark_tabs:"):
            stationNames = pd.read_csv('DataHolder/testfile.csv')
            DataStationName = st.selectbox("Enter Station Name:", stationNames['Station Code'])
            Data = st.file_uploader("Enter Data CSV file:", type=['.csv'], accept_multiple_files = False, help="CSV Format \n Title: \n (measured)_(stationName) \n Contents: \n (dateTime),(numericalValue)")
            newDataCheck = st.checkbox("I have verified that all the inputs are correct.", key = "newDataCheck")
            st.button("Submit", on_click=tryWriteData, key="newDataSubmit")


        with st.expander("Enter New Station :factory:"):
            StationName = st.text_input("Enter Station Name:", key = "StationName")
            StationDesc = st.text_input("Enter Description of Station:", key = "StationDesc")
            StationPos = "[" + st.text_input("Enter Coordonates (North, East)", key = "StationPos") + "]"
            newStationCheck = st.checkbox("I have verified that all e inputs are correct.")
            st.button("Submit", on_click=tryWriteStation)












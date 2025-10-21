import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets authentication
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open the sheet
sheet = client.open("App_Data").sheet1  # change name to your sheet name

# Streamlit app UI
st.title("Data Entry App (Online Excel)")
st.write("Enter your details below:")

name = st.text_input("Name")
age = st.number_input("Age", min_value=0, max_value=120)
department = st.text_input("Department")

if st.button("Submit"):
    sheet.append_row([name, age, department])
    st.success("✅ Data saved successfully to online Excel!")

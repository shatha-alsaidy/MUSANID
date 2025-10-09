import pandas as pd
import streamlit as st
from datetime import datetime

@st.cache_data
def load_patient_data():

    df = pd.read_csv("data/patients.csv")
    

    df["Date_of_Birth"] = pd.to_datetime(df["Date_of_Birth"], errors="coerce")
    today = pd.Timestamp.today()
    df["Age"] = df["Date_of_Birth"].apply(lambda dob: today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) if pd.notnull(dob) else None)
    df["Name"] = df["First_Name"].fillna("") + " " + df["Last_Name"].fillna("")

    
    return df

df= load_patient_data()
print(df.head())
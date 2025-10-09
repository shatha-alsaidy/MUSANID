import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import base64
from utils.data_loader import load_patient_data
import plotly.graph_objects as go
from utils.assessment_engine import AssessmentSession, disorders




############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Search Patient", layout="wide",initial_sidebar_state="collapsed")


#Delet the Page navigator

st.markdown("""
    <style>
  
    [data-testid="stSidebar"] {
        display: none;
    }
    [data-testid="stSidebarNav"] {
        display: none;
    }


    .block-container {
        padding-top: 1rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }

   
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }

  
    [data-testid="stHeader"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)




df = load_patient_data()

#search for patient 

st.markdown(
    """
    <style>
    .btn-container {
        display:flex;
        justify-content:center;  
        align-items:center;
        margin-top:60px;
        margin-bottom:40px;
    }
    .custom-btn {
        background-color:#1267b8;
        color:#ffffff !important;   
        font-weight:700;
        letter-spacing:1px;
        border:none;
        border-radius:40px;
        font-size:20px;
        padding:18px 70px;
        cursor:pointer;
        box-shadow:0 4px 8px rgba(18,103,184,0.3);
        text-decoration:none;
        transition: background-color 0.2s, transform 0.2s;
    }
    .custom-btn:hover {
        background-color:#0f5da5;
        color:#ffffff !important;  
        transform:translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True
)




st.markdown("<h2 style='text-align:center; color:#1267b8;'>ASSESSMENT</h2>", unsafe_allow_html=True)
st.write("")
st.write("")


df["File_Number"] = df["File_Number"].astype(str).str.strip()
file_number = st.text_input("", placeholder="Enter the file number", label_visibility="collapsed")

if file_number:
    p = df[df["File_Number"] == file_number.strip()]
    if not p.empty:
        row = p.iloc[0]

        st.session_state["patient_found"] = True
        st.session_state["patient_data"] = {
            "File_Number": str(row["File_Number"]),
            "First_Name": row["First_Name"],
            "Last_Name": row["Last_Name"],
            "Gender": row.get("Gender", "Unknown"),
            "Date_of_Birth": row.get("Date_of_Birth", None),
        }
        st.success(f"Patient found: {row['First_Name']} {row['Last_Name']}")
    else:
        st.session_state["patient_found"] = False
        st.error("Patient not found. Try again.")


if st.session_state.get("patient_found"):
    

    st.markdown("""
<style>
div[data-testid="stButton"] > button {
    background-color: #1267b8;
    color: white;
    font-weight: 700;
    font-size: 20px;
    letter-spacing: 1px;
    border: none;
    border-radius: 40px;
    padding: 18px 70px;
    box-shadow: 0 4px 8px rgba(18,103,184,0.3);
    cursor: pointer;
    transition: all 0.2s ease;
}
div[data-testid="stButton"] > button:hover {
    background-color: #0f5da5;
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns([1,1,2,1])  
    
    with col3:
        st.markdown("<div class='center-btn'>", unsafe_allow_html=True)
        clicked = st.button("START ASSESSMENT")
        st.markdown("</div>", unsafe_allow_html=True)

    if clicked:
        st.session_state["start_assessment"] = True
        st.switch_page("pages/Assessment_start.py")
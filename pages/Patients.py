import streamlit as st
import base64
from utils.data_loader import load_patient_data

############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Patients  Page", layout="wide",initial_sidebar_state="expanded")



# Delet the Page navigator
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)



#----------------- Sidebar -------------------
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    

image_path = "musanid 1.png"
image_base64 = get_base64_image(image_path)
with st.sidebar:
    
    #logo
    st.markdown(
        f"""
        <div style="text-align: center; margin-top: -140px;">
            <img src="data:image/png;base64,{image_base64}" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

    #Pages 
    st.page_link("pages/Home.py", label="Home", help="Go to Home")
    st.page_link("pages/Patients.py", label="Patients", help="Go to Patients")
    st.page_link("pages/Assessment.py", label="Assessment", help="Go to Patients")


   

   #LOG OUT 
    st.markdown(
        """
        <div style="position: relative; width: 100%; bottom: 0; margin-top: 450px;">
            <button style="
                background-color: #1267b8;  
                color: white;
                width: 100%;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            ">
                LOG OUT
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )
    ########### End of Fixed Page ############



#====================================== Home page Design =================================

df = load_patient_data()

#---------------------- HEADER ------------------ 
st.markdown("""
    <style>
    .block-container {
        padding-top: 0.35rem; 
    }
    </style>
""", unsafe_allow_html=True)

#Search 
col1, col2, col3 = st.columns([3, 1, 0.2])

with col1:
    st.text_input("", placeholder="Search here...")

with col2:
    st.write("") 
    st.write("")   
    st.markdown("<p style='text-align:right; font-weight:600;'>👤 Dr. Omar Ali</p>", unsafe_allow_html=True)

with col3:
    st.write("")
    st.write("")
    st.markdown("<p style='font-size:20px; text-align:right;'>⚙️</p>", unsafe_allow_html=True)



#----------------- Table design ---------------

df["Patient Name"] = df["First_Name"] + " " + df["Last_Name"]

display_df = df[[
    "File_Number", "Patient Name", "ID_Number", "Gender", 
    "Date_of_Birth", "Nationality"
]]

st.markdown("""
<style>
/* الحاوية العامة للجدول */
.full-width-table {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.12);
    padding: 25px;
    margin: 0 40px;          
    height: 700px;           
    overflow-y: auto;        
}


thead tr th {
    background-color: #1267b8 !important;
    color: white !important;
    font-weight: 600;
    text-align: center;
    font-size: 15px;
}


tbody tr td {
    text-align: center !important;
    padding: 12px 5px !important;
    color: #333;
    font-size: 14px;
}


tbody tr:nth-child(even) {
    background-color: #f8f8f8;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h5 style='font-weight:700; color:#2b2b2b; margin-bottom:10px;'>Patients List</h5>", unsafe_allow_html=True)


table_html = display_df.to_html(
    index=False,
    classes="dataframe-container",
    border=0,
    justify="center",

)

st.markdown(table_html, unsafe_allow_html=True)

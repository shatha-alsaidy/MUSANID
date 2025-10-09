import streamlit as st
import base64
from utils.data_loader import load_patient_data
import plotly.graph_objects as go


############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Assessment Page", layout="wide",initial_sidebar_state="expanded")


#Delet the Page navigator

st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none;}
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
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
        <div style="text-align:center; margin-top: -140px; margin-bottom: 30px;">
            <img src="data:image/png;base64,{image_base64}" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )


    #Pages 
    st.page_link("pages/Home.py", label="Home", help="Go to Home")
    st.page_link("pages/Patients.py", label="Patients", help="Go to Patients")
    st.page_link("pages/Assessment.py", label="Assessment", help="Go to Assessment")

   

    
    

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
    st.write()

with col2:
    st.write("") 
    st.write("")   
    st.markdown("<p style='text-align:right; font-weight:600;'>👤 Dr. Omar Ali</p>", unsafe_allow_html=True)

with col3:
    st.write("")
    st.write("")
    st.markdown("<p style='font-size:20px; text-align:right;'>⚙️</p>", unsafe_allow_html=True)

# ---------- BUTTON ----------
st.markdown(
    """
    <style>
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
        transition: background-color 0.2s;
    }
    .custom-btn:hover {
        background-color:#0f5da5;
        color:#ffffff !important;  
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="display:flex; justify-content:center; align-items:center; height:70vh;">
        <a href="/Assessment_SearchPatient" class="custom-btn">START ASSESSMENT</a>
    </div>
    """,
    unsafe_allow_html=True
)
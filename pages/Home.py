import streamlit as st
import base64
from utils.data_loader import load_patient_data
import plotly.graph_objects as go


############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Home Page", layout="wide",initial_sidebar_state="expanded")


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

# WELCOME 

st.markdown("""
    <div style="margin-top:-5px;">
        <p style="font-size:30px; font-weight:600; margin-bottom:-2px; color:#222;">
            Welcome Back, Dr. Omar Ali
        </p>
        <p style="font-size:15px; color:gray; margin-top:-2;">
            Today's Overview
        </p>
    </div>
""", unsafe_allow_html=True)

# ----------------- STAT CARDS -----------------

card_style = """
    background-color: white;
    border-radius: 15px;
    padding: 25px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    text-align: center;
    width: 100%;
"""

col1, col2, col3, col4 = st.columns(4)

appointments = 5
patients = df["File_Number"].nunique() 
critical_cases = len(df[df["Severity"] == "Severe"])
reminders = 7



with col1:
    st.markdown(
        f"""
        <div style="{card_style}">
            <p style="font-size:28px; font-weight:600; color:#2b2b2b; margin:0;">{appointments}</p>
            <p style="color:gray; margin-top:2px;">Appointments</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="{card_style}">
            <p style="font-size:28px; font-weight:600; color:#2b2b2b; margin:0;">{patients}</p>
            <p style="color:gray; margin-top:2px;">Patients</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="{card_style}">
            <p style="font-size:28px; font-weight:600; color:#2b2b2b; margin:0;">{critical_cases}</p>
            <p style="color:gray; margin-top:2px;">Critical Cases</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div style="{card_style}">
            <p style="font-size:28px; font-weight:600; color:#2b2b2b; margin:0;">{reminders}</p>
            <p style="color:gray; margin-top:2px;">Reminder</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.write("")



# ----------- LEFT SIDE: Disease Statistics ------------

total_patients = len(df)
disease_counts = df["Diagnosis"].value_counts()
disease_percent = (disease_counts / total_patients * 100).round(1)
diseases = ["Anxiety", "PTSD", "Depression", "Panic disorder"]
disease_percent = {d: disease_percent.get(d, 0) for d in diseases}


def get_color(percent):
    if percent < 20:
        return "#43a047"  
    elif percent < 50:
        return "#29b6f6"
    elif percent < 80:
        return "#fdd835" 
    else:
        return "#e53935"  
    

col_left, col_right = st.columns([2, 1.2])

with col_left:
    card = st.container()  

    with card:
        st.markdown(
        "<h4 class='stats-title'><span class='pill'>Disease</span> Statistics</h4>",
        unsafe_allow_html=True

    )
        top_row = st.columns(2)
        bottom_row = st.columns(2)
        rows = [top_row, bottom_row]
        diseases = list(disease_percent.items())

        for i, (disease, percent) in enumerate(diseases):
            color = get_color(percent)
            fig = go.Figure(go.Pie(
                values=[percent, 100 - percent],
                hole=0.7,
                marker_colors=[color, "#f5f5f5"],
                textinfo="none"
            ))
            fig.update_layout(
                showlegend=False,
                margin=dict(l=0, r=0, t=0, b=0),
                height=120,
                width=120,
                annotations=[dict(
                    text=f"{percent:.0f}%",
                    x=0.5, y=0.5,
                    font_size=16,
                    font_color="#2b2b2b",
                    showarrow=False
            )]
        )

            row = rows[i // 2]
            with row[i % 2]:
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
                st.markdown(
                    f"<p style='text-align:center; margin-top:-8px; font-weight:500; color:#2b2b2b;'>{disease}</p>",
                    unsafe_allow_html=True
                )
    

# Last Patient 
with col_right:
    last_patient = df.iloc[-1]
    st.markdown(f"""
        <div style="
            background-color:white;
            border-radius:20px;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
            padding:20px 25px;
            height:360px; 
            display:flex;
            flex-direction:column;
            justify-content:space-between;">
            <div>
                <h4 style="font-weight:800; color:#2b2b2b; margin-bottom:10px;">Last Patient</h4>
                <p style="font-size:17px; margin-bottom:5px;">👤 <b>{last_patient['File_Number']}</b></p>
                <p style="color:gray; margin-top:-8px;">{last_patient['First_Name']} {last_patient['Last_Name']}</p>
                <hr style="margin-top:10px; margin-bottom:10px;">
                <p style="font-size:15px; color:#555;">Diagnosis: <b>{last_patient['Diagnosis']}</b></p>
                <p style="font-size:15px; color:#555;">Severity: <b>{last_patient['Severity']}</b></p>
            </div>
            <div style="text-align:center;">
                <button style="
                    background-color:#1267b8;
                    color:white;
                    border:none;
                    border-radius:25px;
                    padding:10px 40px;
                    font-size:14px;
                    cursor:pointer;">
                    START ASSESSMENT
                </button>
            </div>
        </div>
    """, unsafe_allow_html=True)
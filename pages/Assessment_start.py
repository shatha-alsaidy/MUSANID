import sys, os
import streamlit as st
import base64
from utils.data_loader import load_patient_data
import plotly.graph_objects as go
from utils.assessment_engine import AssessmentSession, disorders
import pandas as pd
from datetime import date




############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Assessment Form page ", layout="wide",initial_sidebar_state="collapsed")


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


# know start Assisment
st.session_state["start_assessment"] = True

# Patient Data Setup 
patient_info = st.session_state.get("patient_data", None)

if patient_info and "processed" not in st.session_state:
    
    if "Name" not in patient_info:
        first = patient_info.get("First_Name", "")
        last = patient_info.get("Last_Name", "")
        patient_info["Name"] = f"{first} {last}".strip()

    dob = patient_info.get("Date_of_Birth", None)
    if dob:
        try:
            dob_dt = pd.to_datetime(dob)
            today = date.today()
            age = today.year - dob_dt.year - ((today.month, today.day) < (dob_dt.month, dob_dt.day))
            patient_info["Age"] = age
        except Exception:
            patient_info["Age"] = "Unknown"
    else:
        patient_info["Age"] = "Unknown"


    st.session_state["patient_data"] = patient_info
    st.session_state["processed"] = True  

# Extract values
if patient_info:
    patient_Name = patient_info.get("Name", "Unknown")
    patient_age = patient_info.get("Age", "Unknown")
    patient_sex = patient_info.get("Gender", "Unknown")


if st.session_state.get("start_assessment"):
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([0.2, 5, 0.2])
    with col1:
        back_btn = st.button("✖️", help="Back to Search Page")

    if back_btn:
        st.switch_page("pages/Assessment_SearchPatient.py")

    
    st.markdown("""
<style>

h4 {
    text-align:center;
    color:#1267b8 !important;
    font-weight:700;
    font-size:26px;
    margin-top:30px;
}


.question-text {
    text-align:center;
    color:#000;
    font-size:20px;
    font-weight:600;
    line-height:1.8;
    width:65%;
    margin:40px auto 20px auto; 
}


.stRadio [role=radiogroup] {
    display:flex;
    justify-content:center;   
    gap:30px;
    margin:0 auto;         
    width:fit-content;                 
}

.stRadio label {
    background-color:white;
    border-radius:15px;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
    padding:18px 25px;
    font-weight:500;
    color:#333;
    transition:all 0.2s ease;
    min-width:160px;           
    text-align:center;
}

.stRadio label:hover {
    color:#1267b8;
    transform:translateY(-3px);
    box-shadow:0 5px 12px rgba(18,103,184,0.25);
}


.stButton>button {
    
    background-color:#1267b8;
    color:white;
    border:none;
    border-radius:40px;
    padding:12px 45px;
    font-weight:600;
    font-size:16px;
    cursor:pointer;
    transition:0.3s;
    display:block;
    margin:20px auto 0 auto;  
}
.stButton>button:hover {
    background-color:#0e5da8;
}


.progress-container {
    width:60%;
    margin:40px auto 0 auto;
    height:8px;
    background-color:#eee;
    border-radius:10px;
}
.progress-bar {
    height:8px;
    background-color:#28a745;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)




    st.markdown("<h3 style='text-align:center; color:#1267b8;'>Assessment Questions</h3>", unsafe_allow_html=True)


   
    if "assessment_session" not in st.session_state:
        st.session_state.assessment_session = AssessmentSession(
            disorders_map=disorders,
            age=patient_age,
            sex=patient_sex,
            use_llm=True  # SOS , I should turn it into True when I run it on GPU
        )
    
    session = st.session_state.assessment_session
    question_data = session.get_next_question()

    if not question_data["done"]:
        st.markdown(
            f"<div class='question-text'>{question_data['question']}</div>",
            unsafe_allow_html=True
        )

        st.write("")
        st.write("")

        # Answers Mapping
        answer_map = {
            "Never": 0,
            "Occasionally": 1,
            "Sometimes": 2,
            "Often": 3,
            "All the time": 4
        }

        col1, col2, col3 = st.columns([0.5, 3, 0.5])
        with col2:
            user_answer = st.radio(
                "Select your answer:",
                list(answer_map.keys()),
                horizontal=True,
                label_visibility="collapsed"
                )

        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns([1, 2, 3, 1])
        with col3:
            next_clicked = st.button("Next ➜", use_container_width=False)

        if next_clicked:
            score = answer_map[user_answer]
            session.submit_answer(score)
            st.rerun()



###### get result ##########
    else:
        st.success("Assessment Complete!")
        results = session.get_results()
        df_results = pd.DataFrame(results).T

        if df_results.empty:
            st.warning("No results found.")
            st.stop()

        df_results.reset_index(inplace=True)
        df_results.rename(columns={"index": "Disorder"}, inplace=True)

        top_row = df_results.loc[df_results["normalized_pct"].idxmax()]
        top_disorder = top_row["Disorder"]
        severity = top_row["severity_label"]

        severity_color = {
            "Extreme": "#d9534f",
            "Severe": "#e67e22",
            "Moderate": "#f0ad4e",
            "Mild": "#5bc0de",
            "Normal": "#5cb85c"
        }.get(severity, "#333")

        st.session_state["diagnosis"] = top_disorder
        st.session_state["severity"] = severity

        st.markdown(f"""
        <div style="
            background-color:#ffffff;
            border:2px solid #1267b8;
            border-radius:20px;
            padding:40px 50px;
            width:70%;
            margin:50px auto;
            text-align:center;
            box-shadow:0 8px 20px rgba(0,0,0,0.1);
            font-family:'Tajawal',sans-serif;">
            <h3 style="color:#1267b8; font-size:28px;">Final Diagnosis</h3>
            <p style="font-size:22px; font-weight:600; color:#000;">
                The patient has 
                <b style="color:#1267b8;">{top_disorder}</b> 
                with 
                <b style="color:{severity_color};">{severity}</b> 
                severity.
            </p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            c1, c2 = st.columns([1, 1])
            with c1:
                if st.button("Back to Search"):
                    st.switch_page("pages/Assessment_SearchPatient.py")
            with c2:
                if st.button("Get Treatment Plan ➜"):
                    st.switch_page("pages/Treatment_Plan.py")





import streamlit as st
from utils.data_loader import load_patient_data
import plotly.graph_objects as go
from utils.assessment_engine import AssessmentSession, disorders
from utils.treatment_engine import generate_treatment_plan 
from utils.summary_engine import generate_summary
import pandas as pd 
from datetime import date
import re

############################# This part fixd in all pages #################

#----------------- Page Configration----------
st.set_page_config(page_title="Treatment Plan", layout="wide",initial_sidebar_state="collapsed")


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

patient_info = st.session_state.get("patient_data", None)
diagnosis = st.session_state.get("diagnosis", "Unknown")
severity = st.session_state.get("severity", "Unknown")

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



patient_name = patient_info.get("Name", "Unknown")
patient_age = patient_info.get("Age", "Unknown")
patient_Gender = patient_info.get("Gender", "Unknown")


st.markdown(f"""
    <div style="background-color:#f8f9fa; border-radius:15px; padding:25px 35px; 
                box-shadow:0 4px 15px rgba(0,0,0,0.05); margin-bottom:40px;">
        <h2 style="color:#1267b8; margin-bottom:20px;">Patient Overview</h2>
        <p style="font-size:18px; margin:5px 0;"><b>Name:</b> {patient_name}</p>
        <p style="font-size:18px; margin:5px 0;"><b>Age:</b> {patient_age}</p>
        <p style="font-size:18px; margin:5px 0;"><b>Diagnosis:</b> {diagnosis}</p>
        <p style="font-size:18px; margin:5px 0;"><b>Severity:</b> 
            <span style="color:#1267b8; font-weight:600;">{severity}</span>
        </p>
    </div>
""", unsafe_allow_html=True)



# ================== Treatment Plan =================

if st.button("Generate Treatment Plan"):
    try:
        plan = generate_treatment_plan(diagnosis, severity)

       
        clean_plan = re.sub(r'[*#\+\-]+', '', plan)
        clean_plan = re.sub(r'\n{2,}', '\n\n', clean_plan.strip())

        
        st.session_state["treatment_plan"] = clean_plan

    except Exception as e:
        st.error(f"Error generating treatment plan: {e}")


if "treatment_plan" in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; padding:20px 30px; border-radius:12px; border-left:6px solid #1267b8;">
            <h4 style="color:#1267b8;">Patient Summary</h4>
            <p style="font-size:17px; line-height:1.8; color:#333;">
                {st.session_state["treatment_plan"]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ================== Notes =================


st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("📝 Doctor Notes")

doctor_notes = st.text_area("Write your notes here...", height=200)


if st.button("Save Notes"):
    st.session_state["doctor_notes"] = doctor_notes 
    st.success("Notes saved successfully")


if doctor_notes:
    st.session_state["doctor_notes"] = doctor_notes


###==================== Summary =============

st.markdown("<hr>", unsafe_allow_html=True)
st.subheader("🧠 Start Summarization")

if st.button("Generate Patient Summary"):
    with st.spinner("Generating summary... please wait ⏳"):
        try:
            summary = generate_summary(
                name=patient_name,
                age=patient_age,
                sex=patient_Gender,
                diagnosis=diagnosis,
                severity=severity,
                treatment_plan=st.session_state["treatment_plan"],
                therapist_notes=doctor_notes
            )
            st.session_state["patient_summary"] = summary
            st.success("Summary generated successfully")
        except Exception as e:
            st.error(f"Error generating summary: {e}")


if "patient_summary" in st.session_state:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="background-color:#f9f9f9; padding:20px 30px; border-radius:12px; border-left:6px solid #1267b8;">
            <h4 style="color:#1267b8;">Patient Summary</h4>
            <p style="font-size:17px; line-height:1.8; color:#333;">
                {st.session_state["patient_summary"]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 💾 Save button
    save_btn = st.button("💾 Save in Patient File", use_container_width=False)

    if save_btn:
        st.success("Successfully saved to patient file!")


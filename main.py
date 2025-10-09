import streamlit as st
import base64

#----------------- Page Configration----------
st.set_page_config(page_title="Musanid", layout="wide", initial_sidebar_state="expanded")

#Delet the Page navigator
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
        <div style="text-align:center; margin-top: -140px; margin-bottom: 30px;">
            <img src="data:image/png;base64,{image_base64}" width="500">
        </div>
        """,
        unsafe_allow_html=True
    )

   
    #Pages
    st.page_link("pages/Home.py", label="Home ")
    st.page_link("pages/Patients.py", label="Patients ")
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


st.empty()


st.markdown(
    """
    <div style="text-align:center; margin-top:200px; color:gray; font-size:20px;">
        👋 Welcome to <b>Musanid</b><br>
        Please choose a page from the sidebar.
    </div>
    """,
    unsafe_allow_html=True
)

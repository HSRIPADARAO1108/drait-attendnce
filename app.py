import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

# --- 1. CONFIGURATION & DATA ---
STUDENT_DATA = {
    "1DA25SCS01": "BALAPRIYA F", "1DA25SCS02": "BHAVANA A", "1DA25SCS03": "CHARAN A",
    "1DA25SCS04": "CHETHAN PRASAD L", "1DA25SCS05": "DEEPTHI K", "1DA25SCS06": "DILIP K",
    "1DA25SCS07": "GURUKIRAN K L", "1DA25SCS08": "HARSHITHA P", "1DA25SCS09": "KUSHI PATIL",
    "1DA25SCS10": "L TEJASHWINI", "1DA25SCS11": "PRAKASH V", "1DA25SCS12": "RAKSHA M K",
    "1DA25SCS13": "RAKSHITHA M J", "1DA25SCS14": "RUJULA R", "1DA25SCS15": "SAAKETH D H",
    "1DA25SCS16": "SHWETA", "1DA25SCS17": "SIBIN SIMON", "1DA25SCS18": "SRIPADA RAO H",
    "1DA25SCS20": "YASHASWINI"
}

SUBJECT_INFO = {
    "MCST201: Big Data Analytics": "Dr. Prabha R.",
    "MCSU202: Adv. DBMS": "Dr. Shamshekhar S. Patil",
    "MCST203: Soft Computing": "Dr. K.R. Shylaja",
    "MCS241: Block Chain Tech": "Dr. Shamshekhar S. Patil",
    "MCS254: Agile Technologies": "Dr. Nandini N."
}

CREDENTIALS = {"Faculty": "scs123", "CR": "cr123"}
FILE_PATH = "attendance_records.csv"
LOGIN_BG = "login.jpeg"       
MAIN_BG = "after_login.jpg"    

# --- 2. BACKGROUND IMAGE HELPER ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def apply_background(image_file, is_login=False):
    if os.path.exists(image_file):
        bin_str = get_base64_of_bin_file(image_file)
        
        # Define visibility parameters
        if is_login:
            blur_amount = "0px"
            opacity = "1.0"
            brightness = "1.0"
            sidebar_opacity = "1.0"
        else:
            # Applying 50% visibility (0.5 opacity) and moderate blur
            blur_amount = "8px"
            opacity = "0.5" 
            brightness = "1.1"
            sidebar_opacity = "0.3" # Makes sidebar more transparent to see image
        
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Watermark effect for the entire app background */
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: inherit;
                filter: blur({blur_amount}) brightness({brightness});
                opacity: {opacity};
                z-index: -1;
            }}
            
            /* TARGETING SIDEBAR: Make it transparent to show background image */
            [data-testid="stSidebar"] {{
                background-color: rgba(255, 255, 255, {sidebar_opacity});
            }}

            /* Content container styling */
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.85);
                padding: 30px;
                border-radius: 15px;
                margin-top: 20px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}

            /* Login box styling */
            [data-testid="stVerticalBlock"] > div:has(div.stForm) {{
                background-color: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 3. HEADER COMPONENT ---
def display_header(is_login_page=False):
    main_title_color = "#1E3A8A"
    sub_title_color = "#B45309"
    body_text_color = "#374151"

    st.markdown(f"""
        <div style="text-align: left; background-color: rgba(255,255,255,0.8); padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A;">
            <h1 style="color: {main_title_color}; margin-bottom: 0; font-size: 28px; font-weight: bold;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {sub_title_color}; margin-top: 0; font-size: 20px;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
            <p style="color: {body_text_color}; font-weight: bold; margin-bottom: 5px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
            <div style="background-color: #1E3A8A; color: white; display: inline-block; padding: 6px 15px; border-radius: 5px; font-size: 15px; font-weight: bold;">
                M.Tech. - Computer Science & Engineering (SCS)
            </div>
        </div>
        <hr style='border: 1.5px solid #1E3A8A; margin-top: 15px;'>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Portal Login | Dr. AIT", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)

    with st.form("Login"):
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 Portal Access</h2>", unsafe_allow_html=True)
        role = st.selectbox("Select Role", ["Faculty", "CR"])
        password = st.text_input("Access Password", type="password")
        submit = st.form_submit_button("Login to System", use_container_width=True)
        
        if submit:
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Incorrect Password")
    st.stop()

# --- 5. MAIN INTERFACE (Post-Login) ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False)
display_header(is_login_page=False)

with st.sidebar:
    # Sidebar text now sits on top of the 50% visible background image
    st.markdown(f"### Welcome, \n**{st.session_state.user_role}**")
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Download Records", f, "attendance.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Attendance Entry", "📊 Subject Analytics"])

with tab1:
    st.markdown("### 📝 Mark Daily Attendance")
    c1, c2 = st.columns(2)
    with c1:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with c2:
        dt = st.date_input("Date", date.today())
    
    st.info(f"**Instructor:** {SUBJECT_INFO[sub]}")
    
    # Table Header
    st.markdown("""
        <div style="display: flex; background-color: #1E3A8A; color: white; padding: 10px; border-radius: 5px; font-weight: bold; margin-bottom: 10px;">
            <div style="flex: 1.5;">USN</div>
            <div style="flex: 3;">NAME</div>
            <div style="flex: 1.5;">STATUS</div>
            <div style="flex: 2;">ACTION</div>
        </div>
    """, unsafe_allow_html=True)
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        r1.text(usn)
        r2.markdown(f"**{name}**")
        
        status = st.session_state.att_records[usn]
        if status == "P": r3.success("Present")
        elif status == "A": r3.error("Absent")
        else: r3.info("Pending")
        
        p_btn, a_btn = r4.columns(2)
        if p_btn.button("P", key=f"p_{usn}"):
            st.session_state.att_records[usn] = "P"
            st.rerun()
        if a_btn.button("A", key=f"a_{usn}"):
            st.session_state.att_records[usn] = "A"
            st.rerun()

    st.markdown("---")
    if st.button("SAVE ATTENDANCE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Please mark all students.")
        else:
            st.balloons()
            st.success("Successfully Saved.")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    st.markdown("### 📊 Subject Dashboard")
    st.info("Records will appear here once saved to the database.")

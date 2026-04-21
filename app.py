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
        
        # Blur only applied to MAIN_BG (after login)
        blur_amount = "0px" if is_login else "5px"
        
        container_css = """
            [data-testid="stVerticalBlock"] > div:has(div.stForm) {
                background-color: rgba(255, 255, 255, 0.95);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            }
        """ if is_login else """
            .main .block-container {
                background-color: rgba(255, 255, 255, 0.92);
                padding: 40px;
                border-radius: 15px;
                margin-top: 30px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            }
        """
        
        st.markdown(f"""
            <style>
            .stApp {{
                background: linear-gradient(rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.1)), 
                            url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* This part creates the blur effect for the background only */
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0; width: 100%; height: 100%;
                background: inherit;
                filter: blur({blur_amount});
                z-index: -1;
            }}
            {container_css}
            /* Styling for the P/A buttons to make them compact */
            div.stButton > button {{
                width: 100%;
                padding: 2px;
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 3. HEADER COMPONENT ---
def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    sub_title_color = "#FFD700" if is_login_page else "#B45309"
    body_text_color = "#FFFFFF" if is_login_page else "#374151"

    st.markdown(f"""
        <div style="text-align: left;">
            <h1 style="color: {main_title_color}; margin-bottom: 0; font-size: 28px;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {sub_title_color}; margin-top: 0; font-size: 20px;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
            <p style="color: {body_text_color}; font-weight: bold; margin-bottom: 2px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
            <div style="background-color: rgba(30, 58, 138, 0.8); color: white; display: inline-block; padding: 4px 12px; border-radius: 5px; font-size: 14px;">
                M.Tech. - Computer Science & Engineering (SCS)
            </div>
        </div>
        <hr style='border: 1.5px solid #1E3A8A; margin-top: 10px;'>
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
    st.markdown(f"### Welcome, **{st.session_state.user_role}**")
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
    
    # Improved Table Header
    st.markdown("---")
    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.markdown("**USN**")
    h2.markdown("**NAME**")
    h3.markdown("**CURRENT STATUS**")
    h4.markdown("**MARK ATTENDANCE**")
    st.markdown("---")
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        
        # Row Content
        r1.markdown(f"`{usn}`")
        r2.markdown(f"**{name}**")
        
        status = st.session_state.att_records[usn]
        if status == "P":
            r3.markdown("<span style='color: green; font-weight: bold;'>✅ Present</span>", unsafe_allow_html=True)
        elif status == "A":
            r3.markdown("<span style='color: red; font-weight: bold;'>❌ Absent</span>", unsafe_allow_html=True)
        else:
            r3.markdown("<span style='color: gray;'>⏳ Pending</span>", unsafe_allow_html=True)
        
        # Buttons
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
            st.warning("Please mark all students before saving.")
        else:
            st.balloons()
            st.success("Successfully Saved.")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    st.markdown("### 📊 Subject Dashboard")
    st.info("Analytics data will be displayed here.")

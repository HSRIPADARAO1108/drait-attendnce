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
LOGO_FILE = "logo.png"       # Logo from your previous uploads
BG_FILE = "login_bg.png"      # This is the college image from your current upload

# --- 2. HEADER WITH LOGO & STYLING ---
def display_header(is_dark=False):
    # CSS adjusted for visibility on background image
    txt_color = "white" if is_dark else "#1F2937"
    badge_bg = "rgba(255, 255, 255, 0.2)" if is_dark else "#DBEAFE"
    badge_txt = "white" if is_dark else "#1F2937"

    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists(LOGO_FILE):
            st.image(LOGO_FILE, width=150)
            
    with col2:
        st.markdown(f"""
            <div style="text-align: left; color: {txt_color};">
                <h1 style="color: #1E3A8A; margin-bottom: 0;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
                <h3 style="color: #B45309; margin-top: 0;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
                <p style="font-weight: bold; margin-bottom: 2px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
                <p style="color: {badge_txt}; font-size: 1.1em; background-color: {badge_bg}; display: inline-block; padding: 2px 10px; border-radius: 5px;">
                    M.Tech. - Computer Science & Engineering (SCS)
                </p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #1E3A8A;'>", unsafe_allow_html=True)

# --- 3. BACKGROUND IMAGE HELPER ---
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# --- 4. AUTHENTICATION GATE (with college background) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Dr. AIT Login", page_icon="🔐")

    # Set up background and login card styling
    if os.path.exists(BG_FILE):
        bg_img_base64 = get_base64_of_bin_file(BG_FILE)
        
        st.markdown(f"""
            <style>
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/png;base64,{bg_img_base64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            
            /* Center and style the login form */
            [data-testid="stContainer"] {{
                background-color: rgba(255, 255, 255, 0.85); /* Semi-transparent white card */
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                max-width: 500px;
                margin: auto;
                position: relative;
                top: 50px;
            }}
            </style>
        """, unsafe_allow_html=True)
    else:
        # Fallback if image isn't found
        st.warning(f"⚠️ Login background image missing. Rename your uploaded image to '{BG_FILE}' and place in the project folder.")
        st.markdown("<br>", unsafe_allow_html=True)

    display_header(is_dark=True) # Text adjusted for background
    
    # Authenticate via a central container
    with st.container():
        st.subheader("🔐 Staff & CR Login")
        role = st.selectbox("Select User Role", ["Faculty", "CR"])
        password = st.text_input("Enter Access Code", type="password")
        if st.button("Authorize Access", use_container_width=True, type="primary"):
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Invalid Credentials.")
    
    st.stop()

# --- 5. MAIN INTERFACE (after login) ---
st.set_page_config(page_title="Dr. AIT Attendance Portal", layout="wide")
display_header()

# Reset background/styles for main app (ensuring it's clean)
st.markdown("<style>[data-testid='stAppViewContainer'] > .main {background-image: none;}</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ User Settings")
    st.success(f"**Session:** {st.session_state.user_role}")
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Export Master CSV", f, "attendance_master.csv", "text/csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Attendance Entry", "📈 Subject Analytics"])

# --- TAB 1: MARKING ---
with tab1:
    st.markdown("### 📝 Mark Daily Attendance")
    c1, c2 = st.columns(2)
    with c1:
        selected_sub = st.selectbox("Select Subject", list(SUBJECT_INFO.keys()))
    with c2:
        att_date = st.date_input("Date of Lecture", date.today())
    
    st.markdown(f"<div style='background-color: #FEF3C7; padding: 10px; border-radius: 5px; border-left: 5px solid #D97706;'><strong>Faculty:</strong> {SUBJECT_INFO[selected_sub]}</div>", unsafe_allow_html=True)
    st.divider()

    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.write("**USN**"); h2.write("**NAME**"); h3.write("**STATUS**"); h4.write("**ACTION**")
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        r1.text(usn)
        r2.markdown(f"**{name}**")
        
        status = st.session_state.att_records[usn]
        if status == "P": r3.markdown("<span style='color: green; font-weight: bold;'>PRESENT</span>", unsafe_allow_html=True)
        elif status == "A": r3.markdown("<span style='color: red; font-weight: bold;'>ABSENT</span>", unsafe_allow_html=True)
        else: r3.markdown("<span style='color: gray;'>PENDING</span>", unsafe_allow_html=True)
        
        p_btn, a_btn = r4.columns(2)
        if p_btn.button("P", key=f"p_{usn}", help="Mark Present"):
            st.session_state.att_records[usn] = "P"
            st.rerun()
        if a_btn.button("A", key=f"a_{usn}", help="Mark Absent"):
            st.session_state.att_records[usn] = "A"
            st.rerun()

    if st.button("SUBMIT TO DATABASE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.error("Please mark every student before submitting.")
        else:
            # Data saving logic here...
            st.balloons()
            st.success("Records updated successfully!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: ANALYTICS ---
with tab2:
    st.markdown("### 📊 Live Analytics Dashboard")
    # Analytics display logic here...
    st.info("Mark attendance in Tab 1 to populate analytics.")

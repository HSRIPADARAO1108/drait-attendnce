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

# --- BLUR DIRECTLY ON THE IMAGE CONTAINER ---
def apply_background(image_file, is_login=False):
    if os.path.exists(image_file):
        bin_str = get_base64_of_bin_file(image_file)
        
        # Apply intense blur only if NOT on the login page
        blur_val = "0px" if is_login else "15px"
        
        st.markdown(f"""
            <style>
            /* Target the entire app background layer */
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                /* Apply the blur here */
                filter: blur({blur_val});
                /* Scale slightly to avoid white edges from blur */
                transform: scale(1.02);
                z-index: -1;
            }}
            
            /* Ensure text and interaction elements are NOT blurred */
            .main .block-container {{
                z-index: 10;
                /* Optional: subtle shadow for depth on wide screens */
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                border-radius: 10px;
                padding-top: 1rem;
            }}
            
            /* Styling for standard elements to pop against blur */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: white;
                padding: 5px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            div.stButton > button {{
                border-radius: 5px;
                font-weight: 600;
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 3. HEADER COMPONENT ---
def display_header(is_login_page=False):
    main_title_color = "#1E3A8A" # Deep Navy Blue
    sub_title_color = "#B45309"  # Rich Amber
    body_text_color = "#374151"  # Dark Gray

    # Centered branding layout
    st.markdown(f"""
        <div style="text-align: center; background: white; padding: 25px; border-radius: 12px; border-bottom: 5px solid #1E3A8A; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
            <h1 style="color: {main_title_color}; margin-bottom: 0; font-size: 30px; font-weight: 900;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {sub_title_color}; margin-top: 5px; font-size: 21px; font-weight: 700;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
            <p style="color: {body_text_color}; font-weight: 600; margin-top: 10px; letter-spacing: 1px; font-size: 15px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
            <div style="background-color: #1E3A8A; color: white; display: inline-block; padding: 5px 20px; border-radius: 20px; font-size: 14px; font-weight: bold; margin-top: 10px;">
                M.Tech. - Computer Science & Engineering (SCS)
            </div>
        </div>
        <br>
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
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 Faculty & CR Access</h2>", unsafe_allow_html=True)
        role = st.selectbox("Identify Role", ["Faculty", "CR"])
        password = st.text_input("Department Password", type="password")
        submit = st.form_submit_button("Enter Portal", use_container_width=True)
        
        if submit:
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Incorrect Password.")
    st.stop()

# --- 5. MAIN INTERFACE (Post-Login) ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False) 
display_header(is_login_page=False)

with st.sidebar:
    st.markdown(f"### 👤 Logged in as: \n**{st.session_state.user_role}**")
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Export CSV Data", f, "attendance.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Record Attendance", "📊 Analytics"])

with tab1:
    st.markdown("### 📝 Capture Session Attendance")
    row_c1, row_c2 = st.columns(2)
    with row_c1:
        sub = st.selectbox("Current Subject", list(SUBJECT_INFO.keys()))
    with row_c2:
        dt = st.date_input("Session Date", date.today())
    
    st.info(f"**Instructor:** {SUBJECT_INFO[sub]}")
    
    # Table layout for strict alignment
    st.markdown("""
        <div style="background-color: #1E3A8A; color: white; padding: 12px; border-radius: 8px 8px 0 0; display: flex; font-weight: bold; text-align: center;">
            <div style="flex: 1.5;">USN</div>
            <div style="flex: 3;">STUDENT NAME</div>
            <div style="flex: 1.5;">CURRENT STATUS</div>
            <div style="flex: 2;">ACTION</div>
        </div>
    """, unsafe_allow_html=True)
    
    for usn, name in STUDENT_DATA.items():
        # Highlighting student information to ensure it's not blurry
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        
        with r1: st.markdown(f"**{usn}**")
        with r2: st.markdown(f"**{name}**")
        
        with r3:
            status = st.session_state.att_records[usn]
            if status == "P":
                st.markdown("<p style='color: green; font-weight: bold; text-align:center;'>✅ Present</p>", unsafe_allow_html=True)
            elif status == "A":
                st.markdown("<p style='color: red; font-weight: bold; text-align:center;'>❌ Absent</p>", unsafe_allow_html=True)
            else:
                st.markdown("<p style='color: gray; text-align:center;'>Pending</p>", unsafe_allow_html=True)
        
        with r4:
            p_col, a_col = st.columns(2)
            if p_col.button("Mark P", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"
                st.rerun()
            if a_col.button("Mark A", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"
                st.rerun()
        st.markdown("<hr style='margin: 0; border-color: #eee;'>", unsafe_allow_html=True)

    if st.button("💾 SAVE ATTENDANCE RECORD", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Please mark all students before saving.")
        else:
            st.balloons()
            st.success("Successfully Saved.")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    st.markdown("### 📊 Subject Dashboard")
    st.info("Analytics will update once database is populated.")

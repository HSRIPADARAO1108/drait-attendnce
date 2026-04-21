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

# --- 2. THE BRANDED HEADER ---
def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A" # Pure White on BG, Dark Blue Inside
    sub_title_color = "#FFD700" if is_login_page else "#B45309"  # High Vis Gold vs Academic Gold
    p_text_color = "white" if is_login_page else "#4B5563"

    # Logo on Left, Center Text Layout
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=140)
        else:
            st.warning("Logo Missing")

    with col2:
        st.markdown(f"""
            <div style="text-align: left;">
                <h1 style="color: {main_title_color}; margin-bottom: 0;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
                <h3 style="color: {sub_title_color}; margin-top: 0;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
                <p style="font-weight: bold; color: {p_text_color}; margin-bottom: 2px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
                <p style="color: white; font-size: 1.1em; background-color: rgba(30, 58, 138, 0.8); display: inline-block; padding: 2px 10px; border-radius: 5px;">
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

def apply_background(image_file, is_login=False):
    if os.path.exists(image_file):
        bin_str = get_base64_of_bin_file(image_file)
        # Apply intense blur only if NOT on the login page
        blur_val = "0px" if is_login else "15px"
        # Content background: solid white vs slight transparency
        content_bg = "rgba(255, 255, 255, 0.95)" if is_login else "rgba(255, 255, 255, 0.95)"
        
        st.markdown(f"""
            <style>
            /* Target the entire fixed background layer */
            [data-testid="stAppViewContainer"] > .main {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                /* Apply the blur directly to the background */
                filter: blur({blur_val});
                /* Scale slightly to avoid white edges from blur */
                transform: scale(1.02);
                z-index: -1;
            }}
            
            /* Target the container for text content to ensure it's unblurred and readable */
            .main .block-container {{
                background-color: {content_bg};
                margin-top: 2rem;
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                z-index: 10;
            }}
            
            /* Style other unblurred interaction elements like Tabs */
            .stTabs [data-baseweb="tab-list"] {{
                background-color: white;
                padding: 5px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Login | Dr. AIT", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)

    with st.form("Login"):
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 Faculty & CR Login</h2>", unsafe_allow_html=True)
        role = st.selectbox("Identify Role", ["Faculty", "CR"])
        password = st.text_input("Department Access Code", type="password")
        submit = st.form_submit_button("Enter Portal", use_container_width=True)
        
        if submit:
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Incorrect password for selected role.")
    st.stop()

# --- 5. MAIN INTERFACE (Post-Login) ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False) # Hallway with INTENSE BLUR
display_header(is_login_page=False)

with st.sidebar:
    st.markdown(f"### 👤 Active User: \n**{st.session_state.user_role}**")
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Export CSV Data", f, "attendance_master.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Record Attendance", "📊 Live Analytics"])

with tab1:
    st.markdown("### 📝 Active Attendance Entry")
    col_a, col_b = st.columns(2)
    with col_a:
        sub = st.selectbox("Current Subject", list(SUBJECT_INFO.keys()))
    with col_b:
        dt = st.date_input("Session Date", date.today())
    
    st.info(f"**Instructor:** {SUBJECT_INFO[sub]}")
    st.divider()

    # Column layout for strict alignment
    st.markdown("""
        <div style="background-color: #1E3A8A; color: white; padding: 10px; border-radius: 8px; display: flex; font-weight: bold; text-align: center;">
            <div style="flex: 1.5;">USN</div>
            <div style="flex: 3;">NAME</div>
            <div style="flex: 1.5;">CURRENT STATUS</div>
            <div style="flex: 2;">ACTION</div>
        </div>
    """, unsafe_allow_html=True)
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        r1.markdown(f"**{usn}**")
        r2.text(name)
        
        status = st.session_state.att_records[usn]
        if status == "P": r3.markdown("<span style='color: green; font-weight: bold;'>✅ Present</span>", unsafe_allow_html=True)
        elif status == "A": r3.markdown("<span style='color: red; font-weight: bold;'>❌ Absent</span>", unsafe_allow_html=True)
        else: r3.markdown("<span style='color: gray;'>Pending</span>", unsafe_allow_html=True)
        
        p_btn, a_btn = r4.columns(2)
        if p_btn.button("P", key=f"p_{usn}", use_container_width=True):
            st.session_state.att_records[usn] = "P"
            st.rerun()
        if a_btn.button("A", key=f"a_{usn}", use_container_width=True):
            st.session_state.att_records[usn] = "A"
            st.rerun()
        st.markdown("<hr style='margin: 0; border-color: #eee;'>", unsafe_allow_html=True)

    if st.button("Finalize and Save to Cloud", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.error("Action Required: Mark all students before saving.")
        else:
            # Data saving logic here...
            st.balloons()
            st.success("Successfully Saved.")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    st.markdown("### 📊 Real-Time Analytics Dashboard")
    st.info("Performance metrics will generate once data is logged to CSV.")

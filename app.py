import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

# --- 1. CONFIGURATION & DATA ---
# Fresh start configuration
START_DATE = "2026-04-23"
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

# --- 2. UI HELPERS & CSS ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    if bin_str:
        common_style = f"""
            <style>
            .stApp {{ background-color: transparent; }}
            .stApp::before {{
                content: ""; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover; background-position: center; background-attachment: fixed;
                {"filter: blur(8px); transform: scale(1.05);" if not is_login else ""}
                z-index: -1;
            }}
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.98) !important;
                padding: 1.5rem 1rem !important; border-radius: 15px; margin-top: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }}
            .student-label {{
                color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important;
                margin: 0px !important; -webkit-text-stroke: 0.5px #000000;
            }}
            @media (max-width: 768px) {{
                [data-testid="column"] {{ width: 100% !important; flex: 1 1 100% !important; margin-bottom: 2px !important; }}
                .hide-on-mobile {{ display: none !important; }}
                p, span, label, div {{ color: #000000 !important; }}
                .stButton > button {{ width: 100% !important; border: 1.2px solid #000 !important; }}
            }}
            </style>
        """
        st.markdown(common_style, unsafe_allow_html=True)

def display_header(is_login_page=False):
    m_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    s_color = "#FFD700" if is_login_page else "#B45309"
    b_color = "#FFFFFF" if is_login_page else "#000000"
    st.markdown(f"""
        <div style="text-align: left;">
            <h1 style="color: {m_color}; margin-bottom: 0; font-size: clamp(18px, 5vw, 26px); font-weight: 900;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {s_color}; margin-top: 0; font-size: clamp(14px, 4vw, 18px);">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
            <p style="color: {b_color}; font-weight: 900; font-size: 13px;">M.Tech. SCS | SESSION START: {START_DATE}</p>
        </div><hr style='border: 1.5px solid #1E3A8A; margin: 10px 0;'>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

# --- 4. LOGIN ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Portal Login", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)
    with st.form("Login"):
        role = st.selectbox("Select Role", ["Faculty", "CR"])
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Access System", use_container_width=True):
            if password == CREDENTIALS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else: st.error("Invalid Credentials")
    st.stop()

# --- 5. MAIN APP ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG)
display_header()

with st.sidebar:
    st.markdown(f"### User: {st.session_state.user_role}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("Download CSV", f, "attendance.csv")

tab1, tab2 = st.tabs(["📝 Attendance Entry", "📊 View Analytics"])

with tab1:
    col1, col2, col3 = st.columns([2, 1, 1])
    sub = col1.selectbox("Subject", list(SUBJECT_INFO.keys()))
    dt = col2.date_input("Date", date(2026, 4, 23)) # Default to your start date
    if col3.button("Mark All Present", use_container_width=True):
        for usn in STUDENT_DATA.keys(): st.session_state.att_records[usn] = "P"
        st.rerun()

    st.info(f"**Instructor:** {SUBJECT_INFO[sub]}")
    st.divider()

    for usn, name in STUDENT_DATA.items():
        with st.container():
            r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
            r1.markdown(f"<div class='student-label'>{usn}</div>", unsafe_allow_html=True)
            r2.markdown(f"<div class='student-label'>{name}</div>", unsafe_allow_html=True)
            
            status = st.session_state.att_records.get(usn)
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
            st.markdown("<hr style='margin:8px 0; border:0.5px solid #eee;'>", unsafe_allow_html=True)

    if st.button("SUBMIT ATTENDANCE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Please complete all entries.")
        else:
            new_data = [{"Date": str(dt), "Subject": sub, "USN": u, "Name": STUDENT_DATA[u], "Status": s} 
                        for u, s in st.session_state.att_records.items()]
            df_new = pd.DataFrame(new_data)
            df_final = pd.concat([pd.read_csv(FILE_PATH), df_new]) if os.path.exists(FILE_PATH) else df_new
            df_final.to_csv(FILE_PATH, index=False)
            st.success("Data saved for April 23!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}
            st.balloons()

with tab2:
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        if not df.empty:
            stats = df.groupby(['USN', 'Name']).agg(
                Total=('Status', 'count'),
                Present=('Status', lambda x: (x == 'P').sum())
            ).reset_index()
            stats['Percentage'] = (stats['Present'] / stats['Total'] * 100).round(1)
            stats['Status'] = stats['Percentage'].apply(lambda x: "✅" if x >= 75 else "⚠️")
            st.dataframe(stats, use_container_width=True, hide_index=True)
    else:
        st.write("No records found. Start taking attendance on 23rd April!")

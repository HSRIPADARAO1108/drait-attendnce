import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

# --- PAGE CONFIG ---
st.set_page_config(page_title="Attendance Portal", layout="wide")

# --- RESPONSIVE FIX ---
def responsive_fix():
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .block-container {
            padding: 10px !important;
        }
        button {
            width: 100% !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

responsive_fix()

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
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    if bin_str:
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
        }}
        .main .block-container {{
            background-color: rgba(255,255,255,0.9);
            padding: 20px;
            border-radius: 10px;
        }}
        </style>
        """, unsafe_allow_html=True)

# --- 3. HEADER ---
def display_header():
    st.markdown("""
    <h2 style='color:#1E3A8A;'>Dr. Ambedkar Institute of Technology</h2>
    <hr>
    """, unsafe_allow_html=True)

# --- SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {u: None for u in STUDENT_DATA}

# --- LOGIN ---
if not st.session_state.authenticated:
    apply_background(LOGIN_BG, True)

    role = st.selectbox("Role", ["Faculty", "CR"])
    pwd = st.text_input("Password", type="password")

    if st.button("Login"):
        if pwd == CREDENTIALS[role]:
            st.session_state.authenticated = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Wrong password")

    st.stop()

# --- MAIN ---
apply_background(MAIN_BG)
display_header()

with st.sidebar:
    st.write(f"Logged in: {st.session_state.role}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

    # MOBILE SWITCH
    is_mobile = st.checkbox("📱 Mobile View", value=False)

# --- TABS ---
tab1, tab2 = st.tabs(["Attendance", "Dashboard"])

# ---------------- TAB 1 ----------------
with tab1:

    if is_mobile:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
        dt = st.date_input("Date", date.today())

        if st.button("Mark All Present"):
            for u in STUDENT_DATA:
                st.session_state.att_records[u] = "P"
            st.rerun()
    else:
        c1, c2, c3 = st.columns([2,1,1])
        with c1:
            sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
        with c2:
            dt = st.date_input("Date", date.today())
        with c3:
            if st.button("Mark All Present"):
                for u in STUDENT_DATA:
                    st.session_state.att_records[u] = "P"
                st.rerun()

    st.info(SUBJECT_INFO[sub])

    for usn, name in STUDENT_DATA.items():

        if is_mobile:
            st.markdown(f"### {name}")
            st.caption(usn)

            status = st.radio("Status", ["Present","Absent"], key=f"m_{usn}", horizontal=True)
            st.session_state.att_records[usn] = "P" if status=="Present" else "A"
            st.divider()

        else:
            r1,r2,r3,r4 = st.columns([1.5,3,1.5,2])
            r1.text(usn)
            r2.write(name)

            s = st.session_state.att_records[usn]
            if s=="P": r3.success("P")
            elif s=="A": r3.error("A")
            else: r3.info("-")

            p,a = r4.columns(2)
            if p.button("P", key=f"p_{usn}"):
                st.session_state.att_records[usn] = "P"
                st.rerun()
            if a.button("A", key=f"a_{usn}"):
                st.session_state.att_records[usn] = "A"
                st.rerun()

    if st.button("Save"):
        if None in st.session_state.att_records.values():
            st.warning("Mark all")
        else:
            df = pd.DataFrame([
                {"Date":dt,"Subject":sub,"USN":u,"Name":STUDENT_DATA[u],"Status":s}
                for u,s in st.session_state.att_records.items()
            ])

            if os.path.exists(FILE_PATH):
                df.to_csv(FILE_PATH, mode="a", header=False, index=False)
            else:
                df.to_csv(FILE_PATH, index=False)

            st.success("Saved")
            st.session_state.att_records = {u:None for u in STUDENT_DATA}
            st.rerun()

# ---------------- TAB 2 ----------------
with tab2:
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)

        stats = df.groupby("Name")["Status"].value_counts().unstack(fill_value=0)
        if "P" in stats:
            stats["%"] = (stats["P"]/stats.sum(axis=1))*100

        st.dataframe(stats, use_container_width=True)
        st.bar_chart(stats["%"])
    else:
        st.info("No data")

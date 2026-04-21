import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

# ---------------- CONFIG ----------------
st.set_page_config(page_title="AIT Attendance Portal", layout="wide")

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
    "Big Data Analytics": "Dr. Prabha R.",
    "Adv DBMS": "Dr. Shamshekhar S. Patil",
    "Soft Computing": "Dr. K.R. Shylaja",
    "Blockchain": "Dr. Shamshekhar S. Patil",
    "Agile Tech": "Dr. Nandini N."
}

CREDENTIALS = {"Faculty": "scs123", "CR": "cr123"}
FILE_PATH = "attendance_records.csv"

# ---------------- STYLING ----------------
def apply_style():
    st.markdown("""
    <style>
    .main {background-color: #f5f7fb;}
    h1, h2, h3 {color: #1E3A8A;}
    .stButton>button {
        border-radius: 8px;
        height: 40px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

apply_style()

# ---------------- SESSION ----------------
if "auth" not in st.session_state:
    st.session_state.auth = False

# ---------------- LOGIN ----------------
if not st.session_state.auth:
    st.title("🔐 Attendance Portal Login")

    role = st.selectbox("Role", ["Faculty", "CR"])
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if password == CREDENTIALS[role]:
            st.session_state.auth = True
            st.session_state.role = role
            st.rerun()
        else:
            st.error("Invalid password")

    st.stop()

# ---------------- HEADER ----------------
st.title("📘 AIT Attendance Management System")
st.caption(f"Logged in as **{st.session_state.role}**")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.subheader("Controls")
    if st.button("Logout"):
        st.session_state.auth = False
        st.rerun()

    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        st.download_button("Download CSV", df.to_csv(index=False), "attendance.csv")

# ---------------- TABS ----------------
tab1, tab2 = st.tabs(["📝 Mark Attendance", "📊 Analytics"])

# ---------------- TAB 1 ----------------
with tab1:
    st.subheader("Mark Attendance")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with col2:
        today = st.date_input("Date", date.today())

    st.info(f"Instructor: {SUBJECT_INFO[subject]}")

    attendance = {}

    st.markdown("### Student List")

    for usn, name in STUDENT_DATA.items():
        c1, c2, c3 = st.columns([2, 4, 2])
        c1.write(usn)
        c2.write(name)

        status = c3.radio(
            " ",
            ["P", "A"],
            horizontal=True,
            key=usn
        )
        attendance[usn] = status

    if st.button("Save Attendance", type="primary"):
        df = pd.DataFrame([
            {
                "Date": today,
                "Subject": subject,
                "USN": usn,
                "Name": STUDENT_DATA[usn],
                "Status": attendance[usn]
            }
            for usn in attendance
        ])

        if os.path.exists(FILE_PATH):
            df.to_csv(FILE_PATH, mode='a', header=False, index=False)
        else:
            df.to_csv(FILE_PATH, index=False)

        st.success("Attendance saved successfully")

# ---------------- TAB 2 ----------------
with tab2:
    st.subheader("Analytics Dashboard")

    if not os.path.exists(FILE_PATH):
        st.warning("No data available")
    else:
        df = pd.read_csv(FILE_PATH)

        st.write("### Overall Summary")

        total_classes = df.groupby("Subject")["Date"].nunique()
        st.dataframe(total_classes)

        st.write("### Student Performance")

        pivot = df.pivot_table(
            index="Name",
            columns="Status",
            aggfunc="size",
            fill_value=0
        )

        if "P" in pivot.columns:
            pivot["Attendance %"] = (pivot["P"] / (pivot["P"] + pivot.get("A", 0))) * 100

        st.dataframe(pivot)

        st.write("### Visual")

        st.bar_chart(pivot["Attendance %"])

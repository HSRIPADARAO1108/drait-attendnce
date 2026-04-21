import streamlit as st
import pandas as pd
from datetime import date
import os

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

# Access Credentials
CREDENTIALS = {"Faculty": "scs123", "CR": "cr123"}
FILE_PATH = "attendance_records.csv"

# --- 2. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="M.Tech Login", page_icon="🔐")
    st.title("🛡️ M.Tech Dept. Attendance Portal")
    with st.container(border=True):
        role = st.selectbox("Select Role", ["Faculty", "CR"])
        password = st.text_input("Enter Access Code", type="password")
        if st.button("Authorize Access", use_container_width=True):
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# --- 3. MAIN APP INTERFACE ---
st.set_page_config(page_title="Attendance & Dashboard", layout="wide")

# Sidebar
with st.sidebar:
    st.title("Control Panel")
    st.write(f"Logged in: **{st.session_state.user_role}**")
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("Download CSV Database", f, "attendance_master.csv", "text/csv")

# Tabs for Navigation
tab1, tab2 = st.tabs(["📝 Mark Attendance", "📊 Student Dashboard"])

# --- TAB 1: ATTENDANCE MARKING ---
with tab1:
    st.header("Mark Daily Attendance")
    c_sel, d_sel = st.columns(2)
    with c_sel:
        selected_sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with d_sel:
        att_date = st.date_input("Date", date.today())
    
    st.info(f"**Faculty in Charge:** {SUBJECT_INFO[selected_sub]}")
    st.divider()

    # Table Header
    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.write("**USN**"); h2.write("**Name**"); h3.write("**Status**"); h4.write("**Action**")
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        r1.text(usn)
        r2.text(name)
        
        status = st.session_state.att_records[usn]
        if status == "P": r3.success("Present")
        elif status == "A": r3.error("Absent")
        else: r3.warning("Pending")
        
        p_btn, a_btn = r4.columns(2)
        if p_btn.button("P", key=f"p_{usn}"):
            st.session_state.att_records[usn] = "P"
            st.rerun()
        if a_btn.button("A", key=f"a_{usn}"):
            st.session_state.att_records[usn] = "A"
            st.rerun()

    if st.button("Submit to Archive", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.error("Please mark all students.")
        else:
            new_rows = []
            for usn, stat in st.session_state.att_records.items():
                new_rows.append({
                    "Date": str(att_date), "Subject": selected_sub,
                    "Faculty": SUBJECT_INFO[selected_sub], "USN": usn,
                    "Name": STUDENT_DATA[usn], "Status": stat,
                    "Marked_By": st.session_state.user_role
                })
            
            df_new = pd.DataFrame(new_rows)
            if os.path.exists(FILE_PATH):
                df_old = pd.read_csv(FILE_PATH)
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            else:
                df_final = df_new
            
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.success("Attendance strictly recorded!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: ANALYTICS DASHBOARD ---
with tab2:
    st.header("📈 Strict Attendance Analytics")
    if not os.path.exists(FILE_PATH):
        st.warning("No data found in records.")
    else:
        df = pd.read_csv(FILE_PATH)
        
        filter_sub = st.selectbox("Filter by Subject", list(SUBJECT_INFO.keys()), key="f_sub")
        filter_usn = st.selectbox("Search by USN", list(STUDENT_DATA.keys()), key="f_usn")
        
        # Calculation Logic
        sub_data = df[df['Subject'] == filter_sub]
        total_days = sub_data['Date'].nunique()
        student_sub_data = sub_data[sub_data['USN'] == filter_usn]
        present_days = len(student_sub_data[student_sub_data['Status'] == 'P'])
        absent_days = len(student_sub_data[student_sub_data['Status'] == 'A'])
        
        perc = (present_days / total_days * 100) if total_days > 0 else 0

        st.subheader(f"Summary for {STUDENT_DATA[filter_usn]}")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Classes", total_days)
        m2.metric("Days Present", present_days)
        m3.metric("Days Absent", absent_days)
        m4.metric("Attendance %", f"{perc:.1f}%")
        
        if perc < 75:
            st.error("⚠️ Shortage of Attendance detected (Below 75%)")
        else:
            st.success("✅ Attendance Requirement Satisfied")
            
        st.write("#### Detailed History for this Subject")
        st.table(student_sub_data[['Date', 'Status', 'Marked_By']])

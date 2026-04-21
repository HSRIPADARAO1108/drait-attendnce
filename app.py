import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 1. DATA SETUP ---
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

# --- 2. AUTHENTICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="M.Tech Login", layout="centered")
    st.title("🛡️ Dept. Attendance Access")
    with st.form("Login"):
        role = st.selectbox("Role", ["Faculty", "CR"])
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Authorize"):
            if pwd == CREDENTIALS[role]:
                st.session_state.authenticated, st.session_state.user_role = True, role
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. MAIN INTERFACE ---
st.set_page_config(page_title="M.Tech Dashboard", layout="wide")
tab1, tab2 = st.tabs(["📝 Attendance Entry", "📊 Subject Master Dashboard"])

# --- TAB 1: MARKING ---
with tab1:
    st.header("Daily Attendance Entry")
    c1, c2 = st.columns(2)
    with c1: selected_sub = st.selectbox("Select Subject", list(SUBJECT_INFO.keys()))
    with c2: att_date = st.date_input("Date", date.today())
    
    st.divider()
    # Table logic
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3 = st.columns([4, 1, 1])
        r1.write(f"**{usn}** - {name}")
        if r2.button("P", key=f"p_{usn}"): st.session_state.att_records[usn] = "P"
        if r3.button("A", key=f"a_{usn}"): st.session_state.att_records[usn] = "A"
        
        status = st.session_state.att_records[usn]
        if status == "P": st.success(f"{name} is Present")
        elif status == "A": st.error(f"{name} is Absent")

    if st.button("Finalize and Save", type="primary"):
        if None in st.session_state.att_records.values():
            st.warning("Please mark all students.")
        else:
            new_data = [{"Date": str(att_date), "Subject": selected_sub, "USN": u, "Name": STUDENT_DATA[u], "Status": s} for u, s in st.session_state.att_records.items()]
            df_new = pd.DataFrame(new_data)
            if os.path.exists(FILE_PATH):
                df_old = pd.read_csv(FILE_PATH)
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            else: df_final = df_new
            df_final.to_csv(FILE_PATH, index=False)
            st.success("Archived successfully!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: GLOBAL DASHBOARD ---
with tab2:
    st.header("📊 Subject Attendance Master List")
    if not os.path.exists(FILE_PATH):
        st.info("No records found yet.")
    else:
        df = pd.read_csv(FILE_PATH)
        target_sub = st.selectbox("Select Subject to Review", list(SUBJECT_INFO.keys()), key="dash_sub")
        
        # Filtering for the specific subject
        sub_df = df[df['Subject'] == target_sub]
        total_classes = sub_df['Date'].nunique()
        
        st.subheader(f"Summary for {target_sub}")
        st.write(f"**Total Classes Held to Date:** {total_classes}")

        if total_classes > 0:
            # logic to calculate for ALL students at once
            summary_list = []
            for usn, name in STUDENT_DATA.items():
                student_records = sub_df[sub_df['USN'] == usn]
                present_count = len(student_records[student_records['Status'] == 'P'])
                absent_count = len(student_records[student_records['Status'] == 'A'])
                percentage = (present_count / total_classes) * 100
                
                summary_list.append({
                    "USN": usn,
                    "Student Name": name,
                    "Attended": present_count,
                    "Missed": absent_count,
                    "Percentage (%)": round(percentage, 2),
                    "Status": "✅ OK" if percentage >= 75 else "⚠️ Shortage"
                })
            
            summary_df = pd.DataFrame(summary_list)
            
            # Highlight Shortage students in Red
            def highlight_shortage(s):
                return ['background-color: #ffcccc' if s.Status == "⚠️ Shortage" else '' for _ in s]

            st.table(summary_df) 
            
            # Quick Stats
            avg_attendance = summary_df['Percentage (%)'].mean()
            st.metric("Batch Average Attendance", f"{avg_attendance:.2f}%")
        else:
            st.warning("No classes have been recorded for this subject yet.")

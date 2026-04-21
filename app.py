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

tab1, tab2 = st.tabs(["📝 Mark Attendance", "📊 Subject Master Dashboard"])

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
            
            # Auto-remove duplicates based on Date, Subject, and USN to keep records "Strict"
            df_final = df_final.drop_duplicates(subset=['Date', 'Subject', 'USN'], keep='last')
            
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.success("Attendance strictly recorded!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: UPDATED ANALYTICS DASHBOARD ---
with tab2:
    st.header("📊 Subject Master Dashboard")
    if not os.path.exists(FILE_PATH):
        st.warning("No data found in records. Please mark attendance first.")
    else:
        df = pd.read_csv(FILE_PATH)
        df['Date'] = df['Date'].astype(str) # Ensure date is string for consistent comparison
        
        selected_dashboard_sub = st.selectbox("Select Subject to View All Students", list(SUBJECT_INFO.keys()), key="dash_sub")
        
        # Filter data for the chosen subject
        sub_df = df[df['Subject'] == selected_dashboard_sub]
        
        # Calculate strict total classes held for this subject (Unique dates)
        total_days = sub_df['Date'].nunique()
        
        st.subheader(f"Attendance Report: {selected_dashboard_sub}")
        st.write(f"**Total Classes Held:** {total_days}")
        
        if total_days > 0:
            summary_list = []
            
            for usn, name in STUDENT_DATA.items():
                student_sub_data = sub_df[sub_df['USN'] == usn]
                
                # Count only unique dates where student was present to avoid > 100% errors
                present_days = student_sub_data[student_sub_data['Status'] == 'P']['Date'].nunique()
                absent_days = total_days - present_days
                
                perc = (present_days / total_days * 100)
                
                summary_list.append({
                    "USN": usn,
                    "Name": name,
                    "Present": present_days,
                    "Absent": absent_days,
                    "Attendance %": f"{perc:.1f}%",
                    "Criteria": "✅ OK" if perc >= 75 else "⚠️ Shortage"
                })
            
            # Convert list to DataFrame for the table
            summary_df = pd.DataFrame(summary_list)
            
            # Display full class table
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            st.divider()
            # Individual History Search
            st.write("#### View Individual Detailed History")
            search_usn = st.selectbox("Select USN to see specific dates", list(STUDENT_DATA.keys()))
            hist_df = sub_df[sub_df['USN'] == search_usn]
            st.table(hist_df[['Date', 'Status', 'Marked_By']])
        else:
            st.info("No classes recorded for this subject yet.")

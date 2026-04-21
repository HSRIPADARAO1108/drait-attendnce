import streamlit as st
import pandas as pd
from datetime import date
import os

# --- 1. DATA SETUP ---
# Student List from your records
student_data = {
    "1DA25SCS01": "BALAPRIYA F", "1DA25SCS02": "BHAVANA A", "1DA25SCS03": "CHARAN A",
    "1DA25SCS04": "CHETHAN PRASAD L", "1DA25SCS05": "DEEPTHI K", "1DA25SCS06": "DILIP K",
    "1DA25SCS07": "GURUKIRAN K L", "1DA25SCS08": "HARSHITHA P", "1DA25SCS09": "KUSHI PATIL",
    "1DA25SCS10": "L TEJASHWINI", "1DA25SCS11": "PRAKASH V", "1DA25SCS12": "RAKSHA M K",
    "1DA25SCS13": "RAKSHITHA M J", "1DA25SCS14": "RUJULA R", "1DA25SCS15": "SAAKETH D H",
    "1DA25SCS16": "SHWETA", "1DA25SCS17": "SIBIN SIMON", "1DA25SCS18": "SRIPADA RAO H",
    "1DA25SCS20": "YASHASWINI"
}

# Subject & Faculty Mapping
subject_info = {
    "MCST201: Big Data Analytics": "Dr. Prabha R.",
    "MCSU202: Adv. DBMS": "Dr. Shamshekhar S. Patil",
    "MCST203: Soft Computing": "Dr. K.R. Shylaja",
    "MCS241: Block Chain Tech": "Dr. Shamshekhar S. Patil",
    "MCS254: Agile Technologies": "Dr. Nandini N."
}

# Credentials
CREDENTIALS = {"Faculty": "scs123", "CR": "cr123"}

# --- 2. SESSION STATE MANAGEMENT ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in student_data.keys()}

# --- 3. LOGIN SCREEN ---
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
                st.error("Access Denied: Incorrect Password")
    st.stop()

# --- 4. MAIN APP INTERFACE ---
st.set_page_config(page_title="Attendance System", layout="wide")

with st.sidebar:
    st.title("Control Panel")
    st.write(f"User: **{st.session_state.user_role}**")
    
    selected_sub = st.selectbox("Select Subject", list(subject_info.keys()))
    curr_faculty = subject_info[selected_sub]
    st.info(f"**Faculty:** {curr_faculty}")
    
    att_date = st.date_input("Date", date.today())
    
    st.divider()
    if st.button("Logout", color="red"):
        st.session_state.authenticated = False
        st.rerun()

st.title(f"📊 Marking: {selected_sub}")
st.write(f"Date: {att_date} | Faculty: {curr_faculty}")

# --- 5. ATTENDANCE TABLE ---
header_cols = st.columns([1.5, 3, 1.5, 2])
header_cols[0].write("**USN**")
header_cols[1].write("**Student Name**")
header_cols[2].write("**Status**")
header_cols[3].write("**Mark Attendance**")
st.divider()

for usn, name in student_data.items():
    c1, c2, c3, c4 = st.columns([1.5, 3, 1.5, 2])
    
    c1.text(usn)
    c2.text(name)
    
    # Status Display
    res = st.session_state.att_records[usn]
    if res == "P":
        c3.success("Present")
    elif res == "A":
        c3.error("Absent")
    else:
        c3.info("Pending")
    
    # Action Buttons
    p_btn, a_btn = c4.columns(2)
    if p_btn.button("P", key=f"p_{usn}", use_container_width=True):
        st.session_state.att_records[usn] = "P"
        st.rerun()
    if a_btn.button("A", key=f"a_{usn}", use_container_width=True):
        st.session_state.att_records[usn] = "A"
        st.rerun()

# --- 6. DATA SAVING LOGIC ---
st.divider()
present_count = list(st.session_state.att_records.values()).count("P")
absent_count = list(st.session_state.att_records.values()).count("A")
st.write(f"**Total Present:** {present_count} | **Total Absent:** {absent_count}")

if st.button("Submit Final Attendance", type="primary", use_container_width=True):
    if None in st.session_state.att_records.values():
        st.warning("Please mark attendance for every student before submitting.")
    else:
        # Create DataFrame for current session
        new_data = []
        for usn, status in st.session_state.att_records.items():
            new_data.append({
                "Date": att_date,
                "Subject": selected_sub,
                "Faculty": curr_faculty,
                "USN": usn,
                "Name": student_data[usn],
                "Status": status,
                "Marked_By": st.session_state.user_role
            })
        
        df_new = pd.DataFrame(new_data)
        
        # Save to Local/Cloud Storage (CSV)
        file_path = "attendance_records.csv"
        if os.path.exists(file_path):
            df_old = pd.read_csv(file_path)
            df_final = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df_final = df_new
            
        df_final.to_csv(file_path, index=False)
        
        st.balloons()
        st.success("Data successfully synced to global database!")
        # Reset for next session
        st.session_state.att_records = {usn: None for usn in student_data.keys()}

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

# --- 2. HEADER WITH LOGO & STYLING ---
def display_header():
    # Attempt to load the logo image
    col1, col2 = st.columns([1, 4])
    with col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=150)
        else:
            st.warning("Logo missing (Rename image to logo.png)")
            
    with col2:
        st.markdown("""
            <div style="text-align: left;">
                <h1 style="color: #1E3A8A; margin-bottom: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
                <h3 style="color: #B45309; margin-top: 0; font-weight: 500;">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
                <p style="font-weight: bold; color: #374151; margin-bottom: 2px;">COMPUTER SCIENCE & ENGINEERING PROGRAM</p>
                <p style="color: #1F2937; font-size: 1.1em; background-color: #DBEAFE; display: inline-block; padding: 2px 10px; border-radius: 5px;">
                    M.Tech. - Computer Science & Engineering (SCS)
                </p>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #1E3A8A;'>", unsafe_allow_html=True)

# --- 3. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Dr. AIT Login", page_icon="🔐")
    display_header()
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.subheader("🔐 Staff & CR Login")
        role = st.selectbox("Select User Role", ["Faculty", "CR"])
        password = st.text_input("Enter Department Access Code", type="password")
        if st.button("Authorize Access", use_container_width=True, type="primary"):
            if password == CREDENTIALS[role]:
                st.session_state.authenticated, st.session_state.user_role = True, role
                st.rerun()
            else:
                st.error("Invalid Credentials provided.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 4. MAIN INTERFACE ---
st.set_page_config(page_title="Dr. AIT Attendance Portal", layout="wide")
display_header()

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
            st.error("Action Required: Please mark every student before submitting.")
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
            df_final = df_final.drop_duplicates(subset=['Date', 'Subject', 'USN'], keep='last')
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.success("Records updated successfully!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: ANALYTICS ---
with tab2:
    st.markdown("### 📊 Live Analytics Dashboard")
    if not os.path.exists(FILE_PATH):
        st.warning("No data available.")
    else:
        df = pd.read_csv(FILE_PATH)
        sel_sub = st.selectbox("Filter by Subject", list(SUBJECT_INFO.keys()), key="an_sub")
        
        sub_df = df[df['Subject'] == sel_sub]
        total_classes = sub_df['Date'].nunique()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Classes Held", total_classes)
        
        if total_classes > 0:
            summary = []
            for usn, name in STUDENT_DATA.items():
                st_data = sub_df[sub_df['USN'] == usn]
                pres = st_data[st_data['Status'] == 'P']['Date'].nunique()
                perc = (pres / total_classes * 100)
                summary.append({
                    "USN": usn, "Student Name": name, 
                    "Present": pres, "Absent": total_classes - pres,
                    "Percentage": f"{perc:.1f}%",
                    "Remark": "✅" if perc >= 75 else "🔴 SHORTAGE"
                })
            
            # Colored Table display
            st.dataframe(pd.DataFrame(summary).style.applymap(
                lambda x: 'color: red; font-weight: bold' if x == "🔴 SHORTAGE" else '', subset=['Remark']
            ), use_container_width=True, hide_index=True)
            
            st.divider()
            st.markdown("#### 🔍 Student History Portal")
            st_opts = [f"{u} - {n}" for u, n in STUDENT_DATA.items()]
            sel_st = st.selectbox("Select Student", st_opts)
            s_usn = sel_st.split(" - ")[0]
            
            st.markdown(f"**Viewing History for:** {STUDENT_DATA[s_usn]}")
            h_df = sub_df[sub_df['USN'] == s_usn].sort_values(by='Date', ascending=False)
            st.table(h_df[['Date', 'Status', 'Marked_By']])

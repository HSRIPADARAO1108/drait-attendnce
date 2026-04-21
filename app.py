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

# --- 2. PROFESSIONAL HEADER COMPONENT ---
def display_header():
    # Styled Header Container
    st.markdown("""
        <style>
            .main-header {
                text-align: center;
                padding: 30px;
                background: rgba(255, 255, 255, 0.05); /* Works for dark/light mode */
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                margin-bottom: 20px;
            }
            .inst-name {
                color: #1E3A8A; 
                font-size: 32px; 
                font-weight: 800; 
                margin-bottom: 5px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            .school-name {
                color: #D97706; 
                font-size: 20px; 
                font-weight: 600; 
                margin-bottom: 0px;
            }
            .program-name {
                color: #64748B; 
                font-size: 16px; 
                font-weight: 500;
                margin-top: 5px;
                letter-spacing: 2px;
            }
            .badge {
                background-color: #1E3A8A;
                color: white;
                padding: 6px 20px;
                border-radius: 50px;
                font-size: 14px;
                font-weight: 600;
                display: inline-block;
                margin-top: 15px;
                box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3);
            }
        </style>
    """, unsafe_allow_html=True)

    # Wrap content in the styled div
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    
    # Centering the Logo
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=120)
    
    st.markdown('<div class="inst-name">Dr. Ambedkar Institute of Technology</div>', unsafe_allow_html=True)
    st.markdown('<div class="school-name">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</div>', unsafe_allow_html=True)
    st.markdown('<div class="program-name">COMPUTER SCIENCE & ENGINEERING PROGRAM</div>', unsafe_allow_html=True)
    st.markdown('<div class="badge">M.Tech. - Computer Science & Engineering (SCS)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. AUTHENTICATION LOGIC ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

st.set_page_config(page_title="Dr. AIT Attendance", layout="wide", page_icon="🎓")

if not st.session_state.authenticated:
    display_header()
    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            with st.form("Login"):
                st.subheader("🔐 Secure Portal Login")
                role = st.selectbox("Role", ["Faculty", "CR"])
                password = st.text_input("Access Code", type="password")
                if st.form_submit_button("Access System", use_container_width=True):
                    if password == CREDENTIALS[role]:
                        st.session_state.authenticated, st.session_state.user_role = True, role
                        st.rerun()
                    else:
                        st.error("Access Denied.")
    st.stop()

# --- 4. MAIN APP ---
display_header()

with st.sidebar:
    st.markdown("### 👤 User Info")
    st.info(f"**Role:** {st.session_state.user_role}")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("💾 Backup Data (CSV)", f, "attendance.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Attendance Entry", "📊 Subject Analytics"])

# --- TAB 1: MARKING ---
with tab1:
    st.markdown("### 📝 Active Attendance Sheet")
    c1, c2 = st.columns(2)
    with c1:
        selected_sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with c2:
        att_date = st.date_input("Date", date.today())
    
    st.markdown(f"<div style='padding:10px; border-radius:5px; background:rgba(217, 119, 6, 0.1); border-left: 5px solid #D97706; color: #D97706;'><b>Instructor:</b> {SUBJECT_INFO[selected_sub]}</div>", unsafe_allow_html=True)
    st.divider()

    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.write("**USN**"); h2.write("**NAME**"); h3.write("**STATUS**"); h4.write("**ACTION**")
    
    for usn, name in STUDENT_DATA.items():
        r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
        r1.text(usn)
        r2.markdown(f"**{name}**")
        
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

    if st.button("🔒 Finalize Records", type="primary", use_container_width=True):
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
            
            df_final = df_final.drop_duplicates(subset=['Date', 'Subject', 'USN'], keep='last')
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: ANALYTICS ---
with tab2:
    if not os.path.exists(FILE_PATH):
        st.warning("No database found.")
    else:
        df = pd.read_csv(FILE_PATH)
        sel_sub = st.selectbox("View Subject Report", list(SUBJECT_INFO.keys()))
        sub_df = df[df['Subject'] == sel_sub]
        total = sub_df['Date'].nunique()
        
        st.metric("Total Classes Conducted", total)
        
        if total > 0:
            summary = []
            for usn, name in STUDENT_DATA.items():
                p = sub_df[sub_df['USN'] == usn][sub_df['Status'] == 'P']['Date'].nunique()
                perc = (p/total*100)
                summary.append({"USN": usn, "Name": name, "Attendance %": f"{perc:.1f}%", "Status": "✅ OK" if perc >= 75 else "⚠️ Shortage"})
            
            st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

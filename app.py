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

# --- 2. PERFECTLY ALIGNED PROFESSIONAL HEADER ---
def display_header():
    # CSS for high-end professional alignment
    st.markdown("""
        <style>
            .header-box {
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: #ffffff;
                padding: 25px;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
                border-left: 10px solid #1e3a8a; /* Strong Navy Accent */
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                margin-bottom: 20px;
            }
            .logo-section {
                flex: 0 0 150px; /* Fixed width for logo area */
                text-align: center;
                margin-right: 30px;
                border-right: 2px solid #f0f0f0;
                padding-right: 20px;
            }
            .text-section {
                flex: 1;
            }
            .school-text {
                color: #B45309; /* Academic Gold */
                font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
                font-size: 24px;
                font-weight: 700;
                margin: 0;
                line-height: 1.2;
            }
            .program-text {
                color: #1e3a8a; /* Navy Blue */
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 18px;
                font-weight: 600;
                margin: 4px 0;
                letter-spacing: 0.5px;
            }
            .mtech-text {
                color: #4b5563; /* Slate Grey */
                font-family: 'Segoe UI', Tahoma, sans-serif;
                font-size: 16px;
                font-weight: 500;
                background: #f3f4f6;
                display: inline-block;
                padding: 3px 12px;
                border-radius: 4px;
                margin-top: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    # Creating the aligned layout
    header_col1, header_col2 = st.columns([1, 4])
    
    with header_col1:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=140)
        else:
            st.error("Logo missing")

    with header_col2:
        st.markdown("""
            <div style="padding-left: 20px; border-left: 2px solid #eee;">
                <div class="school-text">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</div>
                <div class="program-text">COMPUTER SCIENCE & ENGINEERING PROGRAM</div>
                <div class="mtech-text">M.Tech. - Computer Science & Engineering (SCS)</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<hr style='margin-top: 0; margin-bottom: 30px; border: 0; border-top: 1px solid #eee;'>", unsafe_allow_html=True)

# --- 3. AUTHENTICATION & SESSION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

st.set_page_config(page_title="Dr. AIT SCS Portal", layout="wide", page_icon="🎓")

if not st.session_state.authenticated:
    display_header()
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<h3 style='text-align: center;'>Portal Login</h3>", unsafe_allow_html=True)
        with st.form("Login_Form"):
            role = st.selectbox("Identify as", ["Faculty", "CR"])
            password = st.text_input("Access Password", type="password")
            if st.form_submit_button("Enter System", use_container_width=True):
                if password == CREDENTIALS[role]:
                    st.session_state.authenticated, st.session_state.user_role = True, role
                    st.rerun()
                else:
                    st.error("Access Denied: Incorrect Password")
    st.stop()

# --- 4. MAIN APPLICATION ---
display_header()

with st.sidebar:
    st.markdown("### 🛠️ Control Center")
    st.write(f"Logged in: **{st.session_state.user_role}**")
    if st.button("Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("Download CSV Database", f, "attendance_data.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Record Attendance", "📊 Subject Dashboard"])

with tab1:
    st.subheader("Attendance Entry")
    col_a, col_b = st.columns(2)
    with col_a:
        sub = st.selectbox("Choose Subject", list(SUBJECT_INFO.keys()))
    with col_b:
        d_val = st.date_input("Select Date", date.today())
    
    st.info(f"**Assigned Faculty:** {SUBJECT_INFO[sub]}")
    st.divider()

    # Column headers for the marking table
    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.write("**USN**"); h2.write("**NAME**"); h3.write("**STATUS**"); h4.write("**ACTION**")
    
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

    if st.button("Finalize and Save to Cloud", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.error("Please complete the attendance list.")
        else:
            rows = []
            for usn, stat in st.session_state.att_records.items():
                rows.append({
                    "Date": str(d_val), "Subject": sub, "Faculty": SUBJECT_INFO[sub],
                    "USN": usn, "Name": STUDENT_DATA[usn], "Status": stat, "By": st.session_state.user_role
                })
            df_new = pd.DataFrame(rows)
            if os.path.exists(FILE_PATH):
                df_old = pd.read_csv(FILE_PATH)
                df_final = pd.concat([df_old, df_new], ignore_index=True).drop_duplicates(subset=['Date', 'Subject', 'USN'], keep='last')
            else:
                df_final = df_new
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    if not os.path.exists(FILE_PATH):
        st.info("No data recorded yet.")
    else:
        df_log = pd.read_csv(FILE_PATH)
        sub_sel = st.selectbox("Select Subject for Analytics", list(SUBJECT_INFO.keys()), key="an_sub")
        df_filtered = df_log[df_log['Subject'] == sub_sel]
        total_sessions = df_filtered['Date'].nunique()
        
        st.metric("Total Classes Conducted", total_sessions)
        
        if total_sessions > 0:
            summary = []
            for usn, name in STUDENT_DATA.items():
                p_count = df_filtered[(df_filtered['USN'] == usn) & (df_filtered['Status'] == 'P')]['Date'].nunique()
                at_perc = (p_count / total_sessions * 100)
                summary.append({
                    "USN": usn, "Name": name, "Present": p_count,
                    "Attendance %": f"{at_perc:.1f}%",
                    "Status": "✅ OK" if at_perc >= 75 else "⚠️ Shortage"
                })
            st.dataframe(pd.DataFrame(summary), use_container_width=True, hide_index=True)

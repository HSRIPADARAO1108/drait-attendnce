import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

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

# --- 2. DATA PERSISTENCE HELPERS ---
def load_records():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["Date", "Subject", "USN", "Name", "Status"])

def save_records_to_csv(date_str, subject, records):
    df_existing = load_records()
    mask = ~((df_existing["Date"] == date_str) & (df_existing["Subject"] == subject))
    df_existing = df_existing[mask]
    
    new_rows = [{"Date": date_str, "Subject": subject, "USN": u, "Name": STUDENT_DATA[u], "Status": s} 
                for u, s in records.items()]
    df_final = pd.concat([df_existing, pd.DataFrame(new_rows)], ignore_index=True)
    df_final.to_csv(FILE_PATH, index=False)

# --- 3. UI HELPERS ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    # Mobile responsiveness meta tag and CSS
    st.markdown("""
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
        .stApp {
            background-image: url("data:image/jpeg;base64,""" + bin_str + """);
            background-size: cover; background-position: center; background-attachment: fixed;
        }
        /* Make containers more readable on mobile */
        @media (max-width: 640px) {
            .main .block-container { padding: 10px !important; }
            .stTabs [data-baseweb="tab"] { font-size: 14px; padding: 10px 5px; }
        }
        .badge-p { background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; }
        .badge-a { background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 5px; font-weight: bold; font-size: 0.8rem; }
        </style>
    """, unsafe_allow_html=True)

def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    st.markdown(f"""
        <div style="text-align: center; padding-bottom: 10px;">
            <h2 style="color: {main_title_color}; margin-bottom: 0; font-size: 22px;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h2>
            <p style="color: gray; font-size: 14px;">M.Tech - SCS Engineering</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Login | Dr. AIT", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)
    with st.form("Login"):
        role = st.selectbox("Select Role", ["Faculty", "CR"])
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login", use_container_width=True):
            if password == CREDENTIALS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG)
display_header()

with st.sidebar:
    st.write(f"Logged in: **{st.session_state.user_role}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

tab1, tab2 = st.tabs(["📝 Attendance", "📊 Analytics"])

with tab1:
    sub = st.selectbox("Select Subject", list(SUBJECT_INFO.keys()))
    # RESTRICTION: min_value=date.today() prevents choosing previous dates
    dt = st.date_input("Date", value=date.today(), min_value=date.today())
    
    if st.button("Mark All Present", type="secondary", use_container_width=True):
        for usn in STUDENT_DATA.keys(): st.session_state.att_records[usn] = "P"
        st.rerun()

    st.divider()
    
    # List for mobile
    for usn, name in STUDENT_DATA.items():
        with st.container():
            col1, col2 = st.columns([2, 1])
            status = st.session_state.att_records[usn]
            
            with col1:
                st.markdown(f"**{name}**")
                st.caption(usn)
            
            with col2:
                if status == "P": st.markdown('<span class="badge-p">PRESENT</span>', unsafe_allow_html=True)
                elif status == "A": st.markdown('<span class="badge-a">ABSENT</span>', unsafe_allow_html=True)
                else: st.caption("Pending")

            b1, b2 = st.columns(2)
            if b1.button(f"P", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"; st.rerun()
            if b2.button(f"A", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"; st.rerun()
            st.markdown("---")

    if st.button("💾 SAVE ATTENDANCE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.error("Mark all students first!")
        else:
            save_records_to_csv(str(dt), sub, st.session_state.att_records)
            st.balloons()
            st.success("Saved!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    df = load_records()
    if df.empty:
        st.info("No data available yet.")
    else:
        st.subheader("Subject-wise Attendance (%)")
        # Visual Graph
        sub_stats = df.groupby("Subject")["Status"].apply(lambda x: (x == "P").sum() / len(x) * 100)
        st.bar_chart(sub_stats)
        
        with st.expander("View Detailed Table"):
            student_perf = df.groupby(["Name"])["Status"].apply(lambda x: round((x == "P").sum() / len(x) * 100, 1)).reset_index()
            st.dataframe(student_perf.sort_values("Status", ascending=False), use_container_width=True)

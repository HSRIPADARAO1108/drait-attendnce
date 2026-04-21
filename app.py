import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta
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

# --- 2. DATA PERSISTENCE & 6-MONTH MAINTENANCE ---
def load_records():
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        # Maintenance: Auto-delete records older than 6 months (180 days)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        six_months_ago = date.today() - timedelta(days=180)
        df = df[df['Date'] >= six_months_ago]
        return df
    return pd.DataFrame(columns=["Date", "Subject", "USN", "Name", "Status"])

def save_records_to_csv(date_str, subject, records):
    df_existing = load_records()
    # Ensure current save is clean
    mask = ~((df_existing["Date"].astype(str) == date_str) & (df_existing["Subject"] == subject))
    df_existing = df_existing[mask]
    
    new_rows = [{"Date": date_str, "Subject": subject, "USN": u, "Name": STUDENT_DATA[u], "Status": s} 
                for u, s in records.items()]
    df_final = pd.concat([df_existing, pd.DataFrame(new_rows)], ignore_index=True)
    df_final.to_csv(FILE_PATH, index=False)

# --- 3. UI HELPERS (SMARTPHONE OPTIMIZED) ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    # Mobile responsiveness CSS
    container_css = """
        [data-testid="stVerticalBlock"] > div:has(div.stForm) {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 20px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
    """ if is_login else """
        .main .block-container {
            background-color: rgba(255, 255, 255, 0.95);
            padding: 15px; border-radius: 15px; margin-top: 10px;
        }
        /* Make buttons more touch-friendly on mobile */
        button {
            min-height: 45px !important;
        }
    """
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover; background-position: center; background-attachment: fixed;
        }}
        {container_css}
        .badge-p {{ background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px; }}
        .badge-a {{ background: #fee2e2; color: #991b1b; padding: 4px 10px; border-radius: 8px; font-weight: bold; font-size: 12px; }}
        </style>
    """, unsafe_allow_html=True)

def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    sub_title_color = "#FFD700" if is_login_page else "#B45309"
    st.markdown(f"""
        <div style="text-align: left;">
            <h1 style="color: {main_title_color}; margin-bottom: 0; font-size: 22px;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {sub_title_color}; margin-top: 0; font-size: 16px;">COMPUTER SCIENCE & ENGINEERING</h3>
        </div>
        <hr style='border: 1px solid #1E3A8A; margin: 10px 0;'>
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
        role = st.selectbox("Role", ["Faculty", "CR"])
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Sign In", use_container_width=True):
            if password == CREDENTIALS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else: st.error("Incorrect Password")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.set_page_config(page_title="Dr. AIT Portal", layout="wide")
apply_background(MAIN_BG, is_login=False)
display_header(is_login_page=False)

with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.user_role}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

tab1, tab2 = st.tabs(["📝 Attendance", "📊 Analytics"])

with tab1:
    st.subheader("Mark Daily Attendance")
    c1, c2 = st.columns(2)
    with c1:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with c2:
        # Restriction: Today's date is the maximum allowed date
        dt = st.date_input("Date", date.today(), max_value=date.today())
    
    if st.button("✅ Mark All Present", use_container_width=True):
        for usn in STUDENT_DATA.keys(): st.session_state.att_records[usn] = "P"
        st.rerun()

    st.markdown("---")
    
    # Mobile Optimized Table Replacement
    for usn, name in STUDENT_DATA.items():
        with st.container():
            # USN and Name in one row, buttons in another for mobile touch comfort
            r1, r2 = st.columns([3, 1])
            r1.markdown(f"**{name}** \n`{usn}`")
            
            status = st.session_state.att_records[usn]
            if status == "P": r2.markdown('<span class="badge-p">P</span>', unsafe_allow_html=True)
            elif status == "A": r2.markdown('<span class="badge-a">A</span>', unsafe_allow_html=True)
            else: r2.write("⏱️")
            
            btn_p, btn_a = st.columns(2)
            if btn_p.button("PRESENT", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"; st.rerun()
            if btn_a.button("ABSENT", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"; st.rerun()
            st.markdown("<hr style='margin:10px 0; opacity:0.1'>", unsafe_allow_html=True)

    if st.button("💾 SAVE ATTENDANCE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Please mark all students.")
        else:
            save_records_to_csv(str(dt), sub, st.session_state.att_records)
            st.success("Saved! Records will be kept for 6 months.")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

with tab2:
    df = load_records()
    if df.empty:
        st.info("No records found.")
    else:
        st.write("### Rolling 6-Month Summary")
        # Subject Percentage
        stats = df.groupby("Subject")["Status"].apply(lambda x: (x == "P").sum() / len(x) * 100).reset_index()
        for _, row in stats.iterrows():
            st.write(f"**{row['Subject']}** ({row['Status']:.1f}%)")
            st.progress(row['Status'] / 100)
        
        st.divider()
        st.write("### Individual Report")
        student_pivot = df.groupby(["USN", "Name"])["Status"].apply(lambda x: round((x == "P").sum() / len(x) * 100, 1)).reset_index()
        st.dataframe(student_pivot.sort_values("Status", ascending=False), use_container_width=True, hide_index=True)

import streamlit as st
import pandas as pd
from datetime import date
import os
import base64

# 1. CONFIGURATION & DATA
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

# 2. THEME & BACKGROUND HELPER
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            return base64.b64encode(f.read()).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    blur = "0px" if is_login else "8px"
    brightness = "1.0" if is_login else "0.8"
    
    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
        
        .stApp {{
            background-image: url("data:image/jpeg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            font-family: 'Plus Jakarta Sans', sans-serif;
        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: inherit;
            filter: blur({blur}) brightness({brightness});
            z-index: -1;
        }}

        [data-testid="stVerticalBlock"] > div:has(div.stForm), .main .block-container {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px !important;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}

        .badge-present {{ background: #dcfce7; color: #166534; padding: 4px 12px; border-radius: 20px; font-weight: 700; border: 1px solid #86efac; }}
        .badge-absent {{ background: #fee2e2; color: #991b1b; padding: 4px 12px; border-radius: 20px; font-weight: 700; border: 1px solid #fca5a5; }}
        </style>
    """, unsafe_allow_html=True)

def display_header():
    st.markdown("""
        <div style="background: linear-gradient(135deg, #1E3A8A 0%, #1e4fd6 100%); padding: 20px; border-radius: 15px; margin-bottom: 20px; border-left: 8px solid #B45309;">
            <h1 style="color: white; margin: 0; font-size: 24px;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <p style="color: #bfdbfe; margin: 0; font-weight: 600; text-transform: uppercase; font-size: 12px; letter-spacing: 1px;">School of Computer Science & Engineering</p>
            <div style="margin-top: 10px; background: rgba(255,255,255,0.2); display: inline-block; padding: 4px 12px; border-radius: 5px; color: white; font-size: 13px; font-weight: bold;">
                M.Tech · Computer Science & Engineering (SCS)
            </div>
        </div>
    """, unsafe_allow_html=True)

# 3. DATA LOGIC
def load_records():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    return pd.DataFrame(columns=["Date", "Subject", "USN", "Name", "Status"])

def save_records(date_str, subject, records):
    df_existing = load_records()
    mask = ~((df_existing["Date"] == date_str) & (df_existing["Subject"] == subject))
    df_existing = df_existing[mask]
    rows = [{"Date": date_str, "Subject": subject, "USN": u, "Name": STUDENT_DATA[u], "Status": s} 
            for u, s in records.items() if s]
    df_final = pd.concat([df_existing, pd.DataFrame(rows)], ignore_index=True)
    df_final.to_csv(FILE_PATH, index=False)

# 4. SESSION STATE & AUTH
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Login | Dr. AIT", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header()
    with st.form("Login"):
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 Portal Access</h2>", unsafe_allow_html=True)
        role = st.selectbox("Select Role", list(CREDENTIALS.keys()))
        password = st.text_input("Access Password", type="password")
        if st.form_submit_button("Sign In", use_container_width=True, type="primary"):
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else: st.error("Invalid Credentials")
    st.stop()

# 5. MAIN INTERFACE
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False)

with st.sidebar:
    st.markdown(f"### Welcome,\n## {st.session_state.user_role}")
    st.info(f"📅 {date.today().strftime('%B %d, %Y')}")
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Export CSV", f, "attendance.csv", use_container_width=True)

display_header()
tab1, tab2 = st.tabs(["📝 Mark Attendance", "📊 Subject Analytics"])

# --- TAB 1: MARK ATTENDANCE ---
with tab1:
    st.subheader("📝 Daily Entry")
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    with c2: dt = st.date_input("Date", date.today())
    with c3:
        if st.button("✅ All Present", use_container_width=True):
            for usn in STUDENT_DATA.keys(): st.session_state.att_records[usn] = "P"
            st.rerun()
    
    st.markdown(f"👨‍🏫 **Instructor:** {SUBJECT_INFO[sub]}")
    
    # Real-time Stats
    p_c = list(st.session_state.att_records.values()).count("P")
    a_c = list(st.session_state.att_records.values()).count("A")
    m1, m2, m3 = st.columns(3)
    m1.metric("Present", p_c)
    m2.metric("Absent", a_c)
    m3.metric("Total Strength", len(STUDENT_DATA))

    st.markdown("""<div style="background:#1E3A8A; color:white; padding:10px; border-radius:10px; display:flex; font-weight:bold;">
                <div style="flex:1.5;">USN</div><div style="flex:3;">Name</div><div style="flex:1.5;">Status</div><div style="flex:2;">Action</div></div>""", unsafe_allow_html=True)

    for usn, name in STUDENT_DATA.items():
        with st.container():
            r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
            r1.write(f"`{usn}`")
            r2.write(f"**{name}**")
            
            status = st.session_state.att_records[usn]
            if status == "P": r3.markdown('<span class="badge-present">P</span>', unsafe_allow_html=True)
            elif status == "A": r3.markdown('<span class="badge-absent">A</span>', unsafe_allow_html=True)
            else: r3.write("---")
            
            bp, ba = r4.columns(2)
            if bp.button("P", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"
                st.rerun()
            if ba.button("A", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"
                st.rerun()

    if st.button("💾 SAVE TO DATABASE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Mark all students before saving.")
        else:
            save_records(str(dt), sub, st.session_state.att_records)
            st.success("Attendance saved successfully!")
            st.balloons()
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}

# --- TAB 2: ANALYTICS ---
with tab2:
    df = load_records()
    if df.empty:
        st.info("No records found.")
    else:
        st.subheader("📊 Subject Progress")
        sub_stats = df.groupby("Subject")["Status"].apply(lambda x: (x == "P").sum() / len(x) * 100).reset_index()
        for _, row in sub_stats.iterrows():
            st.write(f"**{row['Subject']}**")
            st.progress(row['Status'] / 100)
            st.caption(f"Average Attendance: {row['Status']:.1f}%")

        st.divider()
        st.markdown("### Student-wise Attendance (%)")
        student_pivot = df.groupby(["USN", "Name"])["Status"].apply(lambda x: round((x == "P").sum() / len(x) * 100, 1)).reset_index()
        
        # Highlight low attendance (< 75%)
        st.dataframe(
            student_pivot.style.map(lambda x: 'color: red; font-weight: bold' if isinstance(x, (int, float)) and x < 75 else '', subset=['Status']),
            use_container_width=True, hide_index=True
        )

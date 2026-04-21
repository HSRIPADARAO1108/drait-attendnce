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

# --- 2. BACKGROUND IMAGE HELPER ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def apply_background(image_file, is_login=False):
    bin_str = get_base64_of_bin_file(image_file)
    if bin_str:
        # Base CSS for both Desktop and Mobile
        common_style = f"""
            <style>
            .stApp {{
                background-color: transparent;
            }}
            .stApp::before {{
                content: "";
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                {"filter: blur(6px); transform: scale(1.05);" if not is_login else ""}
                z-index: -1;
            }}
            
            /* Responsive Container Padding */
            .main .block-container {{
                background-color: rgba(255, 255, 255, 0.95);
                padding: 2rem 1rem !important;
                border-radius: 15px;
                margin-top: 20px;
            }}

            /* MOBILE RESPONSIVENESS FIX */
            @media (max-width: 768px) {{
                [data-testid="column"] {{
                    width: 100% !important;
                    flex: 1 1 100% !important;
                    min-width: 100% !important;
                    margin-bottom: 10px;
                }}
                .hide-on-mobile {{
                    display: none !important;
                }}
                .stButton > button {{
                    width: 100% !important;
                }}
            }}
            </style>
        """
        st.markdown(common_style, unsafe_allow_html=True)
        
        if is_login:
            st.markdown("""
                <style>
                [data-testid="stVerticalBlock"] > div:has(div.stForm) {
                    background-color: rgba(255, 255, 255, 0.9);
                    padding: 30px; border-radius: 20px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.5);
                }
                </style>
            """, unsafe_allow_html=True)

# --- 3. HEADER COMPONENT ---
def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    sub_title_color = "#FFD700" if is_login_page else "#B45309"
    body_text_color = "#FFFFFF" if is_login_page else "#374151"

    st.markdown(f"""
        <div style="text-align: left;">
            <h1 style="color: {main_title_color}; margin-bottom: 0; font-size: clamp(18px, 5vw, 28px);">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h1>
            <h3 style="color: {sub_title_color}; margin-top: 0; font-size: clamp(14px, 4vw, 20px);">SCHOOL OF COMPUTER SCIENCE & ENGINEERING</h3>
            <p style="color: {body_text_color}; font-weight: bold; margin-bottom: 2px; font-size: 13px;">M.Tech. SCS PROGRAM</p>
        </div>
        <hr style='border: 1px solid #1E3A8A; margin-top: 10px;'>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Portal Login | Dr. AIT", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)

    with st.form("Login"):
        st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🔐 Portal Access</h2>", unsafe_allow_html=True)
        role = st.selectbox("Select Role", ["Faculty", "CR"])
        password = st.text_input("Access Password", type="password")
        submit = st.form_submit_button("Login to System", use_container_width=True)
        
        if submit:
            if password == CREDENTIALS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Incorrect Password")
    st.stop()

# --- 5. MAIN INTERFACE (Post-Login) ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False)
display_header(is_login_page=False)

with st.sidebar:
    st.markdown(f"### Welcome, **{st.session_state.user_role}**")
    if st.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()
    st.divider()
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button("📂 Download Records", f, "attendance.csv", use_container_width=True)

tab1, tab2 = st.tabs(["📝 Entry", "📊 Dashboard"])

with tab1:
    st.markdown("### 📝 Mark Daily Attendance")
    
    # Responsive Controls
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()), key="entry_sub")
    with c2:
        dt = st.date_input("Date", date.today())
    with c3:
        st.markdown("<div style='height: 28px;' class='hide-on-mobile'></div>", unsafe_allow_html=True)
        if st.button("✅ Mark All Present", use_container_width=True):
            for usn in STUDENT_DATA.keys():
                st.session_state.att_records[usn] = "P"
            st.rerun()
    
    st.info(f"**Instructor:** {SUBJECT_INFO[sub]}")
    
    # Table Header (Hidden on Mobile)
    h1, h2, h3, h4 = st.columns([1.5, 3, 1.5, 2])
    h1.markdown("<b class='hide-on-mobile'>USN</b>", unsafe_allow_html=True)
    h2.markdown("<b class='hide-on-mobile'>NAME</b>", unsafe_allow_html=True)
    h3.markdown("<b class='hide-on-mobile'>STATUS</b>", unsafe_allow_html=True)
    h4.markdown("<b class='hide-on-mobile'>ACTION</b>", unsafe_allow_html=True)
    st.divider()

    for usn, name in STUDENT_DATA.items():
        # Row Container
        with st.container():
            r1, r2, r3, r4 = st.columns([1.5, 3, 1.5, 2])
            r1.markdown(f"**{usn}**")
            r2.markdown(name)
            
            status = st.session_state.att_records.get(usn)
            if status == "P": r3.success("Present")
            elif status == "A": r3.error("Absent")
            else: r3.info("Pending")
            
            p_btn, a_btn = r4.columns(2)
            if p_btn.button("P", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"
                st.rerun()
            if a_btn.button("A", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"
                st.rerun()
            st.markdown("<hr style='margin: 5px 0; opacity: 0.2;'>", unsafe_allow_html=True)

    if st.button("SAVE ATTENDANCE", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            st.warning("Please mark all students.")
        else:
            new_rows = [{"Date": str(dt), "Subject": sub, "USN": u, "Name": STUDENT_DATA[u], "Status": s} 
                        for u, s in st.session_state.att_records.items()]
            df_new = pd.DataFrame(new_rows)
            if os.path.exists(FILE_PATH):
                df_old = pd.read_csv(FILE_PATH)
                df_final = pd.concat([df_old, df_new], ignore_index=True)
            else:
                df_final = df_new
            df_final.to_csv(FILE_PATH, index=False)
            st.balloons()
            st.success("Successfully Saved!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}
            st.rerun()

with tab2:
    st.markdown("### 📊 Performance & Eligibility")
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        if not df.empty:
            stats = df.groupby(['USN', 'Name']).agg(
                Total=('Status', 'count'),
                Attended=('Status', lambda x: (x == 'P').sum())
            ).reset_index()
            
            stats['%'] = (stats['Attended'] / stats['Total'] * 100).round(1)
            stats['Eligibility'] = stats['%'].apply(lambda x: "✅ ELIGIBLE" if x >= 75 else "⚠️ SHORTAGE")

            # Dashboard Table
            st.dataframe(stats, use_container_width=True, hide_index=True)

            st.divider()
            st.markdown("#### 🔍 History Filter")
            f1, f2 = st.columns(2)
            with f1:
                student_options = ["All Students"] + [f"{usn} - {name}" for usn, name in STUDENT_DATA.items()]
                selected_student = st.selectbox("Select Student", student_options)
            with f2:
                selected_subject = st.selectbox("Select Subject", ["All Subjects"] + list(SUBJECT_INFO.keys()))

            # Filter logic
            filtered_df = df.copy()
            if selected_student != "All Students":
                filtered_df = filtered_df[filtered_df['USN'] == selected_student.split(" - ")[0]]
            if selected_subject != "All Subjects":
                filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]

            st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)

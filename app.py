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
        container_css = """
            [data-testid="stVerticalBlock"] > div:has(div.stForm) {
                background-color: rgba(255, 255, 255, 0.95);
                padding: 20px; border-radius: 15px;
            }
        """ if is_login else """
            .main .block-container {
                background-color: rgba(255, 255, 255, 0.95);
                padding: 1.5rem; border-radius: 10px;
            }
        """
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{bin_str}");
                background-size: cover; background-position: center; background-attachment: fixed;
            }}
            {container_css}
            /* Make buttons look better on touch screens */
            .stButton>button {{
                border-radius: 8px;
                height: 3em;
                font-weight: bold;
            }}
            </style>
        """, unsafe_allow_html=True)

# --- 3. HEADER COMPONENT ---
def display_header(is_login_page=False):
    main_title_color = "#FFFFFF" if is_login_page else "#1E3A8A"
    st.markdown(f"""
        <div style="text-align: left;">
            <h2 style="color: {main_title_color}; margin-bottom: 0; font-size: 22px;">Dr. AMBEDKAR INSTITUTE OF TECHNOLOGY</h2>
            <p style="color: #B45309; font-weight: bold; margin-bottom: 5px; font-size: 14px;">M.Tech. SCS - Attendance Portal</p>
        </div>
        <hr style='margin: 10px 0;'>
    """, unsafe_allow_html=True)

# --- 4. AUTHENTICATION GATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'att_records' not in st.session_state:
    st.session_state.att_records = {usn: None for usn in STUDENT_DATA.keys()}

if not st.session_state.authenticated:
    st.set_page_config(page_title="Portal Login", page_icon="🔐", layout="centered")
    apply_background(LOGIN_BG, is_login=True)
    display_header(is_login_page=True)

    with st.form("Login"):
        st.markdown("<h3 style='text-align: center;'>🔐 Access</h3>", unsafe_allow_html=True)
        role = st.selectbox("Role", ["Faculty", "CR"])
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login", use_container_width=True):
            if password == CREDENTIALS.get(role):
                st.session_state.authenticated = True
                st.session_state.user_role = role
                st.rerun()
            else:
                st.error("Invalid Password")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.set_page_config(page_title="Attendance Portal", layout="wide")
apply_background(MAIN_BG, is_login=False)
display_header(is_login_page=False)

with st.sidebar:
    st.write(f"Logged in: **{st.session_state.user_role}**")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

tab1, tab2 = st.tabs(["📝 Entry", "📊 Dashboard"])

with tab1:
    # Top controls - stacks automatically on mobile
    col_a, col_b = st.columns([1, 1])
    with col_a:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()), key="entry_sub")
    with col_b:
        dt = st.date_input("Date", date.today())
    
    if st.button("✅ Mark All Present", use_container_width=True):
        for usn in STUDENT_DATA.keys():
            st.session_state.att_records[usn] = "P"
        st.rerun()

    st.divider()

    # Mobile Friendly List
    for usn, name in STUDENT_DATA.items():
        # Using a container for each student to keep it clean on mobile
        with st.container():
            # USN and Name on one line
            st.markdown(f"**{usn}** - {name}")
            
            # Buttons and Status on the second line
            c1, c2, c3 = st.columns([1, 1, 1])
            
            status = st.session_state.att_records.get(usn)
            
            if c1.button("✅ P", key=f"p_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "P"
                st.rerun()
            if c2.button("❌ A", key=f"a_{usn}", use_container_width=True):
                st.session_state.att_records[usn] = "A"
                st.rerun()
            
            with c3:
                if status == "P": st.success("P")
                elif status == "A": st.error("A")
                else: st.info("?")
        st.markdown("---")

    if st.button("💾 SAVE ATTENDANCE", type="primary", use_container_width=True):
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
            st.success("Saved!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA.keys()}
            st.rerun()

with tab2:
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        if not df.empty:
            # 1. Eligibility Table
            stats = df.groupby(['USN', 'Name']).agg(
                Total=('Status', 'count'),
                Attended=('Status', lambda x: (x == 'P').sum())
            ).reset_index()
            stats['%'] = (stats['Attended'] / stats['Total'] * 100).round(1)
            stats['Status'] = stats['%'].apply(lambda x: "✅ OK" if x >= 75 else "⚠️ Low")

            st.markdown("#### % Attendance Report")
            # Using st.dataframe with use_container_width=True makes it scrollable on mobile
            st.dataframe(stats, use_container_width=True, hide_index=True)

            st.divider()
            
            # 2. Search & Filter
            st.markdown("#### 🔍 Filter Records")
            student_list = ["All Students"] + [f"{usn} - {name}" for usn, name in STUDENT_DATA.items()]
            sel_student = st.selectbox("Select Student", student_list)
            sel_sub = st.selectbox("Select Subject", ["All Subjects"] + list(SUBJECT_INFO.keys()))

            filtered_df = df.copy()
            if sel_student != "All Students":
                filtered_df = filtered_df[filtered_df['USN'] == sel_student.split(" - ")[0]]
            if sel_sub != "All Subjects":
                filtered_df = filtered_df[filtered_df['Subject'] == sel_sub]

            st.dataframe(filtered_df.sort_values(by="Date", ascending=False), use_container_width=True, hide_index=True)
        else:
            st.info("No records found.")
    else:
        st.info("No attendance file found.")

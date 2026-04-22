import streamlit as st
import pandas as pd
from datetime import date
import os
import base64
import math
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURATION & DATA ---
# Dr. AIT Coordinates
COLLEGE_LAT = 12.9634 
COLLEGE_LON = 77.5065
RADIUS = 100  # 100 meters

STUDENT_DATA = {
    "1DA25SCS01": {"name": "BALAPRIYA F", "email": "parent1@mail.com", "phone": "9000000001"},
    "1DA25SCS18": {"name": "SRIPADA RAO H", "email": "parent18@mail.com", "phone": "9000000018"},
    "1DA25SCS20": {"name": "YASHASWINI", "email": "parent20@mail.com", "phone": "9000000020"}
    # Add others here following this dictionary format
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

# --- 2. HELPERS ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000 # Earth radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def apply_background():
    st.markdown("""
        <style>
        .stApp { background-color: #f0f2f6; }
        .main .block-container { background: white; border-radius: 20px; padding: 2rem; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
        .dev-footer { position: fixed; bottom: 0; width: 100%; text-align: center; background: white; padding: 10px; font-weight: bold; color: #1E3A8A; border-top: 2px solid #1E3A8A; z-index: 100; }
        </style>
    """, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'session_ended' not in st.session_state: st.session_state.session_ended = False
if 'verified_students' not in st.session_state: st.session_state.verified_students = {}

# --- 4. AUTHENTICATION ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Login | Dr. AIT")
    st.header("🔐 Dr. AIT Portal")
    with st.form("login"):
        role = st.selectbox("Role", ["Faculty", "CR"])
        pwd = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if pwd == CREDENTIALS.get(role):
                st.session_state.authenticated, st.session_state.user_role = True, role
                st.rerun()
    st.stop()

# --- 5. MAIN INTERFACE ---
st.set_page_config(page_title="Attendance System", layout="wide")
apply_background()

# Capture Location
loc = streamlit_js_eval(js_expressions="window.navigator.geolocation.getCurrentPosition(pos => {return [pos.coords.latitude, pos.coords.longitude]})", want_output=True)

with st.sidebar:
    st.title(f"Hi, {st.session_state.user_role}")
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()

st.title("🏫 Dr. Ambedkar Institute of Technology")
tab1, tab2 = st.tabs(["📝 Session Management", "📊 Records"])

with tab1:
    sub = st.selectbox("Current Subject", list(SUBJECT_INFO.keys()))
    st.info(f"Instructor: {SUBJECT_INFO[sub]}")

    # GPS CHECK
    is_on_campus = False
    if loc:
        dist = calculate_distance(loc[0], loc[1], COLLEGE_LAT, COLLEGE_LON)
        if dist <= RADIUS:
            is_on_campus = True
            st.success(f"📍 GPS Verified: Within 100m of Dr. AIT")
        else:
            st.error(f"🚫 GPS Error: You are {round(dist)}m away. Attendance blocked.")

    # FACULTY CONTROL
    if st.session_state.user_role == "Faculty":
        if not st.session_state.session_ended:
            if st.button("🔴 FINISH CLASS & OPEN BIOMETRIC LOCK", type="primary"):
                st.session_state.session_ended = True
                st.rerun()
        else:
            if st.button("🟢 RESTART SESSION"):
                st.session_state.session_ended = False
                st.session_state.verified_students = {}
                st.rerun()

    st.divider()

    # BIOMETRIC SECTION
    if st.session_state.session_ended:
        st.warning("🔒 The class has ended. Students must verify now.")
        if is_on_campus:
            st.subheader("Student Self-Verification")
            usn_to_verify = st.text_input("Enter your USN to verify")
            if st.button("🧬 SCAN BIOMETRICS (Fingerprint/Face)"):
                if usn_to_verify in STUDENT_DATA:
                    st.session_state.verified_students[usn_to_verify] = "P"
                    st.success(f"Verified {usn_to_verify} successfully!")
                else:
                    st.error("Invalid USN")
        else:
            st.error("Verification unavailable: You are not physically in the classroom.")

    # FINAL SAVE (CR or Faculty)
    if st.button("💾 SAVE FINAL ATTENDANCE & NOTIFY PARENTS", type="secondary"):
        records = []
        absentees = []
        
        for usn, info in STUDENT_DATA.items():
            status = st.session_state.verified_students.get(usn, "A")
            records.append({
                "Date": str(date.today()),
                "Subject": sub,
                "USN": usn,
                "Name": info['name'],
                "Status": status
            })
            if status == "A":
                absentees.append(info)

        # Save to CSV
        df_new = pd.DataFrame(records)
        if os.path.exists(FILE_PATH):
            df_final = pd.concat([pd.read_csv(FILE_PATH), df_new], ignore_index=True)
        else:
            df_final = df_new
        df_final.to_csv(FILE_PATH, index=False)

        # Send Notifications (Simulation)
        for student in absentees:
            st.toast(f"📧 Email sent to {student['email']}")
            st.toast(f"📱 SMS sent to {student['phone']}")
        
        st.balloons()
        st.success(f"Saved! {len(absentees)} parents notified.")
        st.session_state.session_ended = False
        st.session_state.verified_students = {}

with tab2:
    if os.path.exists(FILE_PATH):
        st.dataframe(pd.read_csv(FILE_PATH), use_container_width=True)

st.markdown('<div class="dev-footer">Developed by H Sripada Rao | Dr. AIT</div>', unsafe_allow_html=True)

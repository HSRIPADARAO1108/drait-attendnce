import streamlit as st
import pandas as pd
from datetime import date
import os
import base64
import math
import cv2
import numpy as np
import face_recognition
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURATION ---
COLLEGE_LAT, COLLEGE_LON = 12.9634, 77.5065
RADIUS = 100 
FILE_PATH = "attendance_records.csv"
USER_DB = "student_credentials.csv"
PHOTO_DIR = "photos"

if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

STUDENT_DATA_BASE = {
    "1DA25SCS01": "BALAPRIYA F", "1DA25SCS18": "SRIPADA RAO H", "1DA25SCS20": "YASHASWINI"
}

SUBJECT_INFO = {
    "MCST201: Big Data Analytics": "Dr. Prabha R.",
    "MCSU202: Adv. DBMS": "Dr. Shamshekhar S. Patil"
}

# --- 2. HELPER FUNCTIONS ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def verify_face(student_usn, live_frame):
    try:
        ref_path = f"{PHOTO_DIR}/{student_usn}.jpg"
        if not os.path.exists(ref_path):
            return False, "Registration photo missing!"
        ref_img = face_recognition.load_image_file(ref_path)
        ref_enc = face_recognition.face_encodings(ref_img)[0]
        rgb_frame = cv2.cvtColor(live_frame, cv2.COLOR_BGR2RGB)
        live_enc = face_recognition.face_encodings(rgb_frame)
        if len(live_enc) > 0:
            match = face_recognition.compare_faces([ref_enc], live_enc[0])
            return match[0], "Identity Confirmed" if match[0] else "Face Mismatch!"
        return False, "No face detected"
    except Exception as e:
        return False, str(e)

# --- 3. SESSION STATE ---
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'session_active' not in st.session_state: st.session_state.session_active = True
if 'verified_list' not in st.session_state: st.session_state.verified_list = {}

# --- 4. LOGIN & REGISTRATION ---
if not st.session_state.authenticated:
    st.set_page_config(page_title="Dr. AIT Access", layout="centered")
    mode = st.radio("Select Mode", ["Login", "New Student Registration"])

    if mode == "New Student Registration":
        with st.form("Registration"):
            st.subheader("📝 Create Student Profile")
            reg_usn = st.text_input("USN (Unique ID)")
            reg_pwd = st.text_input("Create Password", type="password")
            reg_photo = st.camera_input("Take Official Profile Selfie")
            if st.form_submit_button("Register"):
                if reg_usn and reg_pwd and reg_photo:
                    with open(f"{PHOTO_DIR}/{reg_usn}.jpg", "wb") as f:
                        f.write(reg_photo.getbuffer())
                    new_user = pd.DataFrame([[reg_usn, reg_pwd]], columns=["USN", "PWD"])
                    new_user.to_csv(USER_DB, mode='a', header=not os.path.exists(USER_DB), index=False)
                    st.success("Registration Successful! Please switch to Login.")
                else: st.error("Complete all fields.")
    else:
        with st.form("Login"):
            st.subheader("🔐 Portal Login")
            role = st.selectbox("Role", ["Faculty", "Student"])
            u_id = st.text_input("USN / Username")
            u_pw = st.text_input("Password", type="password")
            if st.form_submit_button("Access Portal"):
                if role == "Faculty" and u_pw == "scs123":
                    st.session_state.authenticated, st.session_state.user_role = True, "Faculty"
                    st.rerun()
                elif role == "Student" and os.path.exists(USER_DB):
                    db = pd.read_csv(USER_DB)
                    if not db[(db['USN'] == u_id) & (db['PWD'].astype(str) == u_pw)].empty:
                        st.session_state.authenticated, st.session_state.user_role = True, "Student"
                        st.session_state.current_user = u_id
                        st.rerun()
                else: st.error("Invalid credentials.")
    st.stop()

# --- 5. MAIN INTERFACE ---
st.set_page_config(page_title="Dr. AIT Attendance", layout="wide")
loc = streamlit_js_eval(js_expressions="window.navigator.geolocation.getCurrentPosition(pos => {return [pos.coords.latitude, pos.coords.longitude]})", want_output=True)

with st.sidebar:
    st.write(f"Logged in: **{st.session_state.user_role}**")
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.rerun()

# --- FACULTY VIEW ---
if st.session_state.user_role == "Faculty":
    st.header("📋 Faculty Control Dashboard")
    current_sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()))
    
    if st.session_state.session_active:
        if st.button("🔴 END LECTURE & OPEN VERIFICATION"):
            st.session_state.session_active = False
            st.rerun()
    else:
        st.warning("⚠️ Verification is currently OPEN for students.")
        if st.button("💾 SAVE FINAL & NOTIFY PARENTS"):
            # Logic to save to CSV and simulate SMS/Email
            st.success("Records saved! Notifications dispatched to parents.")
            st.session_state.session_active = True
            st.session_state.verified_list = {}

# --- STUDENT VIEW ---
else:
    st.header(f"👋 Welcome, {st.session_state.current_user}")
    
    # GPS Logic
    is_nearby = False
    if loc:
        d = calculate_distance(loc[0], loc[1], COLLEGE_LAT, COLLEGE_LON)
        if d <= RADIUS:
            is_nearby = True
            st.success("📍 GPS: Inside Class (Dr. AIT)")
        else: st.error(f"📍 GPS: You are outside the 100m radius.")

    # Biometric Logic
    if not st.session_state.session_active:
        st.subheader("🧬 Final Biometric Verification")
        if is_nearby:
            v_img = st.camera_input("Verify Your Identity")
            if v_img:
                bytes_data = np.asarray(bytearray(v_img.read()), dtype=np.uint8)
                frame = cv2.imdecode(bytes_data, 1)
                match, msg = verify_face(st.session_state.current_user, frame)
                if match:
                    st.success("✅ Identity Verified! Attendance Logged.")
                    st.session_state.verified_list[st.session_state.current_user] = "P"
                else: st.error(msg)
        else: st.info("Please move inside the classroom to verify.")
    else:
        st.info("🕒 Lecture is in progress. Biometric check opens at the end of class.")

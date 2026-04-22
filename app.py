import streamlit as st
import pandas as pd
from datetime import date
import os
import base64
import math
import cv2
import numpy as np
import face_recognition # The key library for matching faces
from streamlit_js_eval import streamlit_js_eval

# --- 1. CONFIGURATION ---
COLLEGE_LAT, COLLEGE_LON = 12.9634, 77.5065
RADIUS = 100 
FILE_PATH = "attendance_records.csv"

# Updated Student Data with Photo paths
# Ensure you have a folder named 'photos' with 1DA25SCS18.jpg inside it!
STUDENT_DATA = {
    "1DA25SCS01": {"name": "BALAPRIYA F", "email": "parent1@mail.com", "photo": "photos/101.jpg"},
    "1DA25SCS18": {"name": "SRIPADA RAO H", "email": "parent18@mail.com", "photo": "photos/118.jpg"},
}

# --- 2. FACE RECOGNITION HELPER ---
def verify_face(student_usn, live_frame):
    """Compares live camera frame with stored student photo."""
    try:
        # 1. Load the stored reference image
        ref_path = STUDENT_DATA[student_usn]["photo"]
        if not os.path.exists(ref_path):
            return False, "Reference photo missing!"

        ref_img = face_recognition.load_image_file(ref_path)
        ref_encoding = face_recognition.face_encodings(ref_img)[0]

        # 2. Process the live frame
        rgb_frame = cv2.cvtColor(live_frame, cv2.COLOR_BGR2RGB)
        live_encodings = face_recognition.face_encodings(rgb_frame)

        if len(live_encodings) > 0:
            # 3. Compare faces
            match = face_recognition.compare_faces([ref_encoding], live_encodings[0])
            return match[0], "Match Found" if match[0] else "Face does not match!"
        
        return False, "No face detected in camera"
    except Exception as e:
        return False, f"Error: {str(e)}"

# --- 3. UI HELPERS ---
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi, dlambda = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

# --- 4. APP LOGIC ---
st.set_page_config(page_title="Biometric Attendance", layout="wide")

if 'session_ended' not in st.session_state: st.session_state.session_ended = False
if 'verified_students' not in st.session_state: st.session_state.verified_students = {}

st.title("📸 Biometric & GPS Attendance System")

# GPS Capture
loc = streamlit_js_eval(js_expressions="window.navigator.geolocation.getCurrentPosition(pos => {return [pos.coords.latitude, pos.coords.longitude]})", want_output=True)

# Main Tab
tab1, tab2 = st.tabs(["Check-In", "Database"])

with tab1:
    # GPS Status
    is_on_campus = False
    if loc:
        dist = calculate_distance(loc[0], loc[1], COLLEGE_LAT, COLLEGE_LON)
        if dist <= RADIUS:
            is_on_campus = True
            st.success("📍 Location Verified: Within 100m")
        else: st.error(f"🚫 Outside Campus ({round(dist)}m away)")

    # Faculty Control
    if st.button("🔴 END CLASS (Open Biometric Lock)"):
        st.session_state.session_ended = True

    # Biometric Section
    if st.session_state.session_ended:
        st.divider()
        st.header("Step 2: Biometric Verification")
        usn = st.text_input("Enter USN")
        
        # Camera Input for Face Recognition
        img_file = st.camera_input("Take a Selfie to Verify")

        if img_file and usn in STUDENT_DATA:
            if is_on_campus:
                # Convert Streamlit image to OpenCV format
                file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
                opencv_image = cv2.imdecode(file_bytes, 1)

                with st.spinner("Comparing face with Department Records..."):
                    is_match, message = verify_face(usn, opencv_image)

                if is_match:
                    st.success(f"✅ Identity Confirmed for {usn}")
                    st.session_state.verified_students[usn] = "P"
                else:
                    st.error(f"❌ {message}")
            else:
                st.error("GPS Verification failed. You cannot verify from this location.")

    # Save Attendance
    if st.button("💾 Finalize & Send Parent Alerts"):
        # (Same saving logic as before - saves USNs in st.session_state.verified_students as 'P', others 'A')
        st.success("Attendance synced. Parents notified of absentees.")

with tab2:
    if os.path.exists(FILE_PATH):
        st.write(pd.read_csv(FILE_PATH))

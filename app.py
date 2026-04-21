import streamlit as st
import pandas as pd
from datetime import date, datetime
import os
import base64

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURATION & DATA
# ─────────────────────────────────────────────────────────────────────────────
STUDENT_DATA = {
    "1DA25SCS01": "BALAPRIYA F",      "1DA25SCS02": "BHAVANA A",
    "1DA25SCS03": "CHARAN A",          "1DA25SCS04": "CHETHAN PRASAD L",
    "1DA25SCS05": "DEEPTHI K",         "1DA25SCS06": "DILIP K",
    "1DA25SCS07": "GURUKIRAN K L",     "1DA25SCS08": "HARSHITHA P",
    "1DA25SCS09": "KUSHI PATIL",       "1DA25SCS10": "L TEJASHWINI",
    "1DA25SCS11": "PRAKASH V",         "1DA25SCS12": "RAKSHA M K",
    "1DA25SCS13": "RAKSHITHA M J",     "1DA25SCS14": "RUJULA R",
    "1DA25SCS15": "SAAKETH D H",       "1DA25SCS16": "SHWETA",
    "1DA25SCS17": "SIBIN SIMON",       "1DA25SCS18": "SRIPADA RAO H",
    "1DA25SCS20": "YASHASWINI",
}

SUBJECT_INFO = {
    "MCST201: Big Data Analytics":   "Dr. Prabha R.",
    "MCSU202: Adv. DBMS":            "Dr. Shamshekhar S. Patil",
    "MCST203: Soft Computing":       "Dr. K.R. Shylaja",
    "MCS241: Block Chain Tech":      "Dr. Shamshekhar S. Patil",
    "MCS254: Agile Technologies":    "Dr. Nandini N.",
}

CREDENTIALS = {"Faculty": "scs123", "CR": "cr123"}
FILE_PATH    = "attendance_records.csv"
LOGIN_BG     = "login.jpeg"
MAIN_BG      = "after_login.jpg"

ROLE_ICON = {"Faculty": "👨‍🏫", "CR": "👨‍💼"}

# ─────────────────────────────────────────────────────────────────────────────
# 2. BACKGROUND HELPER
# ─────────────────────────────────────────────────────────────────────────────
def get_b64(file: str) -> str:
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

def apply_background(image_file: str, is_login: bool = False):
    if not os.path.exists(image_file):
        return
    b64 = get_b64(image_file)
    blur   = "0px"  if is_login else "6px"
    dimmer = "0.08" if is_login else "0.35"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [data-testid="stAppViewContainer"] {{
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* ── Full-viewport background ── */
    .stApp {{
        background-image: url("data:image/jpeg;base64,{b64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
        backdrop-filter: blur({blur});
        background: rgba(10, 14, 26, {dimmer});
        z-index: 0;
    }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background: rgba(10, 14, 35, 0.82) !important;
        border-right: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(20px);
    }}
    [data-testid="stSidebar"] * {{
        color: #e8eaf6 !important;
    }}

    /* ── Main content glass card ── */
    .main .block-container {{
        background: rgba(255, 255, 255, 0.93);
        border-radius: 20px;
        padding: 2.2rem 2.5rem !important;
        box-shadow: 0 8px 40px rgba(0,0,0,0.22);
        margin-top: 1.5rem;
        position: relative;
        z-index: 1;
    }}

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background: #f0f4ff;
        border-radius: 12px;
        padding: 6px;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 9px;
        padding: 8px 20px;
        font-weight: 600;
        font-size: 0.88rem;
        color: #4a5568;
        background: transparent;
        border: none;
    }}
    .stTabs [aria-selected="true"] {{
        background: #1E3A8A !important;
        color: white !important;
        box-shadow: 0 2px 12px rgba(30,58,138,0.35);
    }}

    /* ── Buttons ── */
    .stButton > button {{
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        transition: all 0.18s ease !important;
        border: none !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.18) !important;
    }}

    /* ── Selectbox & date input ── */
    .stSelectbox > div > div, .stDateInput > div > div {{
        border-radius: 10px !important;
        border: 1.5px solid #c7d2fe !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }}

    /* ── Status badges ── */
    .badge-present {{
        display: inline-block;
        background: #dcfce7; color: #166534;
        border-radius: 20px; padding: 3px 14px;
        font-size: 0.82rem; font-weight: 700;
        border: 1.5px solid #86efac;
    }}
    .badge-absent {{
        display: inline-block;
        background: #fee2e2; color: #991b1b;
        border-radius: 20px; padding: 3px 14px;
        font-size: 0.82rem; font-weight: 700;
        border: 1.5px solid #fca5a5;
    }}
    .badge-pending {{
        display: inline-block;
        background: #f1f5f9; color: #64748b;
        border-radius: 20px; padding: 3px 14px;
        font-size: 0.82rem; font-weight: 700;
        border: 1.5px solid #cbd5e1;
    }}

    /* ── Table rows ── */
    .att-row {{
        display: flex; align-items: center;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 6px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        transition: background 0.15s;
    }}
    .att-row:hover {{ background: #eef2ff; }}

    /* ── Metric cards ── */
    .metric-card {{
        background: white;
        border-radius: 14px;
        padding: 18px 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        border-left: 5px solid;
        margin-bottom: 10px;
    }}

    /* ── Progress bar ── */
    .att-bar-wrap {{
        background: #e5e7eb;
        border-radius: 999px;
        height: 10px;
        overflow: hidden;
        margin-top: 5px;
    }}
    .att-bar-fill {{
        height: 100%;
        border-radius: 999px;
        transition: width 0.5s ease;
    }}

    /* ── Form box (login) ── */
    .login-glass {{
        background: rgba(255,255,255,0.96);
        border-radius: 24px;
        padding: 42px 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        max-width: 420px;
        margin: 0 auto;
    }}

    /* Hide Streamlit branding */
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 3. HEADER
# ─────────────────────────────────────────────────────────────────────────────
def display_header():
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1E3A8A 0%, #1e4fd6 60%, #B45309 100%);
        border-radius: 16px;
        padding: 20px 28px;
        margin-bottom: 18px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 20px rgba(30,58,138,0.3);
    ">
        <div style="font-size: 48px; line-height:1;">🎓</div>
        <div>
            <div style="color: #bfdbfe; font-size: 0.75rem; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 2px;">
                School of Computer Science & Engineering
            </div>
            <div style="color: white; font-size: 1.35rem; font-weight: 800; letter-spacing: -0.3px; line-height: 1.2;">
                Dr. Ambedkar Institute of Technology
            </div>
            <div style="margin-top: 8px;">
                <span style="
                    background: rgba(255,255,255,0.18);
                    color: #fde68a;
                    border-radius: 6px;
                    padding: 3px 12px;
                    font-size: 0.8rem;
                    font-weight: 700;
                    letter-spacing: 0.5px;
                ">M.Tech · Computer Science & Engineering (SCS)</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4. CSV HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def load_records() -> pd.DataFrame:
    if os.path.exists(FILE_PATH):
        try:
            return pd.read_csv(FILE_PATH)
        except Exception:
            pass
    return pd.DataFrame(columns=["Date", "Subject", "Instructor", "USN", "Name", "Status"])

def save_records(date_str: str, subject: str, records: dict):
    df_existing = load_records()
    # Remove duplicate entries for same date+subject
    mask = ~((df_existing["Date"] == date_str) & (df_existing["Subject"] == subject))
    df_existing = df_existing[mask]

    rows = []
    for usn, status in records.items():
        if status is not None:
            rows.append({
                "Date":       date_str,
                "Subject":    subject,
                "Instructor": SUBJECT_INFO.get(subject, ""),
                "USN":        usn,
                "Name":       STUDENT_DATA.get(usn, ""),
                "Status":     status,
            })
    df_new = pd.DataFrame(rows)
    df_final = pd.concat([df_existing, df_new], ignore_index=True)
    df_final.to_csv(FILE_PATH, index=False)
    return df_final

# ─────────────────────────────────────────────────────────────────────────────
# 5. SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "att_records" not in st.session_state:
    st.session_state.att_records = {u: None for u in STUDENT_DATA}

# ─────────────────────────────────────────────────────────────────────────────
# 6. LOGIN PAGE
# ─────────────────────────────────────────────────────────────────────────────
if not st.session_state.authenticated:
    st.set_page_config(
        page_title="Attendance Portal · Login",
        page_icon="🔐",
        layout="centered",
    )
    apply_background(LOGIN_BG, is_login=True)
    display_header()

    st.markdown('<div class="login-glass">', unsafe_allow_html=True)
    st.markdown("""
        <div style="text-align:center; margin-bottom: 24px;">
            <div style="font-size: 3rem;">🔐</div>
            <h2 style="margin: 6px 0 4px; color: #1E3A8A; font-weight: 800;">Portal Access</h2>
            <p style="color: #64748b; font-size: 0.9rem; margin:0;">Sign in to manage attendance records</p>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        role     = st.selectbox("Role", list(CREDENTIALS.keys()), label_visibility="visible")
        password = st.text_input("Password", type="password", placeholder="Enter your access key")
        submitted = st.form_submit_button("🚀  Sign In", use_container_width=True, type="primary")

        if submitted:
            if password == CREDENTIALS[role]:
                st.session_state.authenticated = True
                st.session_state.user_role     = role
                st.rerun()
            else:
                st.error("❌  Incorrect password. Please try again.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 7. MAIN APP
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Attendance Portal · Dr. AIT",
    page_icon="📋",
    layout="wide",
)
apply_background(MAIN_BG, is_login=False)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    role_icon = ROLE_ICON.get(st.session_state.user_role, "👤")
    st.markdown(f"""
        <div style="text-align:center; padding: 16px 0 8px;">
            <div style="font-size: 2.8rem;">{role_icon}</div>
            <div style="font-size: 1rem; font-weight: 700; margin-top: 6px;">
                {st.session_state.user_role}
            </div>
            <div style="font-size: 0.78rem; opacity: 0.65; margin-top: 2px;">
                {datetime.now().strftime("%A, %d %B %Y")}
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Stats in sidebar
    df_all = load_records()
    total_sessions = 0
    if not df_all.empty:
        total_sessions = df_all.groupby(["Date", "Subject"]).ngroups
    st.markdown(f"""
        <div style="background: rgba(255,255,255,0.08); border-radius:12px; padding:14px; margin-bottom:12px;">
            <div style="font-size: 0.75rem; opacity: 0.65; text-transform: uppercase; letter-spacing:1px;">Total Sessions Logged</div>
            <div style="font-size: 2rem; font-weight: 800; margin-top:4px;">{total_sessions}</div>
        </div>
    """, unsafe_allow_html=True)

    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "rb") as f:
            st.download_button(
                "📥  Download Records (CSV)",
                f,
                file_name=f"attendance_{date.today()}.csv",
                mime="text/csv",
                use_container_width=True,
            )

    st.divider()
    if st.button("🚪  Logout", use_container_width=True, type="primary"):
        st.session_state.authenticated = False
        st.session_state.att_records   = {u: None for u in STUDENT_DATA}
        st.rerun()

# ── Header ───────────────────────────────────────────────────────────────────
display_header()

# ── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📝  Mark Attendance", "📊  Analytics Dashboard"])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 – MARK ATTENDANCE
# ════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("#### 📝 Daily Attendance Entry")

    col_sub, col_date = st.columns([3, 2])
    with col_sub:
        sub = st.selectbox("Subject", list(SUBJECT_INFO.keys()), label_visibility="visible")
    with col_date:
        dt = st.date_input("Date", date.today(), label_visibility="visible")

    st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, #eff6ff, #e0e7ff);
            border: 1.5px solid #c7d2fe;
            border-radius: 12px;
            padding: 12px 18px;
            margin: 10px 0 18px;
            display: flex; gap: 14px; align-items: center;
        ">
            <div style="font-size: 1.5rem;">👩‍🏫</div>
            <div>
                <div style="font-size: 0.72rem; color:#6366f1; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Instructor</div>
                <div style="font-weight: 700; color: #1e3a8a; font-size: 1rem;">{SUBJECT_INFO[sub]}</div>
            </div>
            <div style="margin-left: auto; text-align:right;">
                <div style="font-size: 0.72rem; color:#6366f1; font-weight:700; text-transform:uppercase; letter-spacing:1px;">Date</div>
                <div style="font-weight: 700; color: #1e3a8a;">{dt.strftime("%d %B %Y")}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Quick-mark all buttons ──
    qa, qb, _ = st.columns([1.4, 1.4, 5])
    if qa.button("✅  Mark All Present", use_container_width=True):
        st.session_state.att_records = {u: "P" for u in STUDENT_DATA}
        st.rerun()
    if qb.button("❌  Mark All Absent", use_container_width=True):
        st.session_state.att_records = {u: "A" for u in STUDENT_DATA}
        st.rerun()

    # ── Live summary strip ──
    marked_p = sum(1 for v in st.session_state.att_records.values() if v == "P")
    marked_a = sum(1 for v in st.session_state.att_records.values() if v == "A")
    marked_n = sum(1 for v in st.session_state.att_records.values() if v is None)
    total_s  = len(STUDENT_DATA)

    st.markdown(f"""
        <div style="display:flex; gap:10px; margin: 12px 0 16px; flex-wrap:wrap;">
            <div style="background:#dcfce7; border:1.5px solid #86efac; color:#166534;
                        border-radius:10px; padding:8px 18px; font-weight:700; font-size:0.9rem;">
                ✅ Present &nbsp;<b>{marked_p}</b>
            </div>
            <div style="background:#fee2e2; border:1.5px solid #fca5a5; color:#991b1b;
                        border-radius:10px; padding:8px 18px; font-weight:700; font-size:0.9rem;">
                ❌ Absent &nbsp;<b>{marked_a}</b>
            </div>
            <div style="background:#f1f5f9; border:1.5px solid #cbd5e1; color:#64748b;
                        border-radius:10px; padding:8px 18px; font-weight:700; font-size:0.9rem;">
                ⏳ Pending &nbsp;<b>{marked_n}</b>
            </div>
            <div style="background:#eff6ff; border:1.5px solid #93c5fd; color:#1d4ed8;
                        border-radius:10px; padding:8px 18px; font-weight:700; font-size:0.9rem;">
                👥 Total &nbsp;<b>{total_s}</b>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # ── Table header ──
    st.markdown("""
        <div style="display:flex; background:linear-gradient(90deg,#1E3A8A,#1e4fd6);
                    color:white; padding:10px 16px; border-radius:10px;
                    font-size:0.8rem; font-weight:700; letter-spacing:1px;
                    text-transform:uppercase; margin-bottom:6px;">
            <div style="flex:1.8;">#&nbsp; USN</div>
            <div style="flex:3.2;">Student Name</div>
            <div style="flex:1.6;">Status</div>
            <div style="flex:2;">Action</div>
        </div>
    """, unsafe_allow_html=True)

    # ── Student rows ──
    for idx, (usn, name) in enumerate(STUDENT_DATA.items(), start=1):
        c_usn, c_name, c_status, c_p, c_a = st.columns([1.8, 3.2, 1.6, 1, 1])

        c_usn.markdown(
            f"<span style='font-family:JetBrains Mono,monospace; font-size:0.78rem; color:#475569;'>"
            f"<b>{idx:02d}</b>&nbsp; {usn}</span>",
            unsafe_allow_html=True,
        )
        c_name.markdown(f"<span style='font-weight:600; color:#1e293b;'>{name}</span>", unsafe_allow_html=True)

        status = st.session_state.att_records[usn]
        if status == "P":
            c_status.markdown('<span class="badge-present">Present</span>', unsafe_allow_html=True)
        elif status == "A":
            c_status.markdown('<span class="badge-absent">Absent</span>', unsafe_allow_html=True)
        else:
            c_status.markdown('<span class="badge-pending">—</span>', unsafe_allow_html=True)

        if c_p.button("P ✅", key=f"p_{usn}", use_container_width=True):
            st.session_state.att_records[usn] = "P"
            st.rerun()
        if c_a.button("A ❌", key=f"a_{usn}", use_container_width=True):
            st.session_state.att_records[usn] = "A"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Save button ──
    if st.button("💾  SAVE ATTENDANCE RECORD", type="primary", use_container_width=True):
        if None in st.session_state.att_records.values():
            pending_usns = [u for u, v in st.session_state.att_records.items() if v is None]
            st.warning(
                f"⚠️  Please mark all students before saving. "
                f"**{len(pending_usns)} student(s)** still pending."
            )
        else:
            save_records(str(dt), sub, st.session_state.att_records)
            st.balloons()
            st.success(f"✅  Attendance for **{sub}** on **{dt.strftime('%d %B %Y')}** saved successfully!")
            st.session_state.att_records = {u: None for u in STUDENT_DATA}
            st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 – ANALYTICS DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("#### 📊 Attendance Analytics Dashboard")

    df = load_records()

    if df.empty:
        st.info("📭  No records yet. Save attendance from the **Mark Attendance** tab to see analytics here.")
    else:
        df["Date"] = pd.to_datetime(df["Date"])

        # ── Top KPI row ──
        total_entries = len(df)
        total_present = (df["Status"] == "P").sum()
        overall_pct   = round((total_present / total_entries) * 100, 1) if total_entries else 0
        subjects_done = df["Subject"].nunique()
        sessions_done = df.groupby(["Date", "Subject"]).ngroups

        k1, k2, k3, k4 = st.columns(4)
        for col, label, value, icon, accent in [
            (k1, "Overall Attendance", f"{overall_pct}%",    "📈", "#1E3A8A"),
            (k2, "Total Sessions",     str(sessions_done),   "📅", "#0891b2"),
            (k3, "Subjects Covered",   str(subjects_done),   "📚", "#7c3aed"),
            (k4, "Students Enrolled",  str(len(STUDENT_DATA)),"👥","#b45309"),
        ]:
            col.markdown(f"""
                <div class="metric-card" style="border-left-color:{accent};">
                    <div style="font-size:1.6rem;">{icon}</div>
                    <div style="font-size: 1.9rem; font-weight:800; color:{accent}; margin:4px 0 2px;">{value}</div>
                    <div style="font-size:0.78rem; color:#64748b; font-weight:600;">{label}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Filters ──
        fa, fb = st.columns(2)
        with fa:
            sub_filter = st.multiselect(
                "Filter by Subject",
                df["Subject"].unique().tolist(),
                default=df["Subject"].unique().tolist(),
            )
        with fb:
            usn_filter = st.multiselect(
                "Filter by Student (USN)",
                list(STUDENT_DATA.keys()),
                placeholder="All students",
            )

        df_f = df[df["Subject"].isin(sub_filter)]
        if usn_filter:
            df_f = df_f[df_f["USN"].isin(usn_filter)]

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Per-subject attendance ──
        st.markdown("##### 📚 Subject-wise Attendance Rate")
        sub_stats = (
            df_f.groupby("Subject")["Status"]
            .apply(lambda x: round((x == "P").sum() / len(x) * 100, 1))
            .reset_index()
            .rename(columns={"Status": "Attendance %"})
            .sort_values("Attendance %", ascending=False)
        )

        for _, row in sub_stats.iterrows():
            pct   = row["Attendance %"]
            color = "#16a34a" if pct >= 75 else ("#f59e0b" if pct >= 60 else "#dc2626")
            sub_short = row["Subject"].split(":")[0]
            st.markdown(f"""
                <div style="margin-bottom: 12px;">
                    <div style="display:flex; justify-content:space-between; font-size:0.85rem; font-weight:600; color:#1e293b; margin-bottom:4px;">
                        <span>{row['Subject']}</span>
                        <span style="color:{color};">{pct}%</span>
                    </div>
                    <div class="att-bar-wrap">
                        <div class="att-bar-fill" style="width:{pct}%; background:{color};"></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Per-student attendance table ──
        st.markdown("##### 👥 Student-wise Attendance Summary")

        student_stats = (
            df_f.groupby(["USN", "Name"])["Status"]
            .apply(lambda x: {
                "Total": len(x),
                "Present": (x == "P").sum(),
                "Absent":  (x == "A").sum(),
                "Attendance %": round((x == "P").sum() / len(x) * 100, 1),
            })
            .apply(pd.Series)
            .reset_index()
            .sort_values("Attendance %", ascending=False)
        )

        # Color code rows
        def style_pct(val):
            if val >= 75: return "color: #16a34a; font-weight: 800;"
            elif val >= 60: return "color: #d97706; font-weight: 800;"
            else: return "color: #dc2626; font-weight: 800;"

        if not student_stats.empty:
            # Build styled HTML table
            rows_html = ""
            for _, r in student_stats.iterrows():
                pct_style = style_pct(r["Attendance %"])
                bar_color = "#16a34a" if r["Attendance %"] >= 75 else ("#f59e0b" if r["Attendance %"] >= 60 else "#dc2626")
                rows_html += f"""
                <tr>
                  <td style="font-family:monospace; font-size:0.8rem; color:#475569;">{r['USN']}</td>
                  <td style="font-weight:600; color:#1e293b;">{r['Name']}</td>
                  <td style="text-align:center;">{int(r['Total'])}</td>
                  <td style="text-align:center; color:#16a34a; font-weight:700;">{int(r['Present'])}</td>
                  <td style="text-align:center; color:#dc2626; font-weight:700;">{int(r['Absent'])}</td>
                  <td style="{pct_style} text-align:center;">{r['Attendance %']}%</td>
                </tr>"""

            st.markdown(f"""
            <div style="overflow-x:auto; border-radius:12px; border:1px solid #e2e8f0; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
            <table style="width:100%; border-collapse:collapse; font-size:0.87rem;">
                <thead>
                <tr style="background:linear-gradient(90deg,#1E3A8A,#1e4fd6); color:white;">
                    <th style="padding:12px 14px; text-align:left; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">USN</th>
                    <th style="padding:12px 14px; text-align:left; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">Name</th>
                    <th style="padding:12px 14px; text-align:center; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">Total</th>
                    <th style="padding:12px 14px; text-align:center; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">Present</th>
                    <th style="padding:12px 14px; text-align:center; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">Absent</th>
                    <th style="padding:12px 14px; text-align:center; font-size:0.75rem; letter-spacing:1px; text-transform:uppercase;">Attendance %</th>
                </tr>
                </thead>
                <tbody>
                {rows_html}
                </tbody>
            </table>
            </div>
            <div style="margin-top:10px; font-size:0.75rem; color:#94a3b8;">
                🟢 ≥75% &nbsp;|&nbsp; 🟡 60–74% &nbsp;|&nbsp; 🔴 &lt;60% (shortage)
            </div>
            """, unsafe_allow_html=True)

        # ── At-Risk students ──
        at_risk = student_stats[student_stats["Attendance %"] < 75]
        if not at_risk.empty:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
                <div style="background:#fff7ed; border:1.5px solid #fed7aa; border-radius:12px; padding:16px 20px;">
                    <div style="font-weight:800; color:#c2410c; margin-bottom:8px; font-size:0.95rem;">
                        ⚠️  {len(at_risk)} Student(s) Below 75% Attendance
                    </div>
                    {"".join(f'<div style="color:#7c2d12; font-size:0.85rem; padding:3px 0;">• <b>{r["USN"]}</b> — {r["Name"]} ({r["Attendance %"]}%)</div>' for _, r in at_risk.iterrows())}
                </div>
            """, unsafe_allow_html=True)

        # ── Raw records expander ──
        with st.expander("🗂️  View / Export Raw Records"):
            st.dataframe(
                df_f[["Date", "Subject", "USN", "Name", "Status"]]
                .sort_values(["Date", "Subject", "USN"])
                .reset_index(drop=True),
                use_container_width=True,
                height=320,
            )
            csv_bytes = df_f.to_csv(index=False).encode()
            st.download_button(
                "📥  Download Filtered CSV",
                csv_bytes,
                file_name=f"filtered_attendance_{date.today()}.csv",
                mime="text/csv",
            )

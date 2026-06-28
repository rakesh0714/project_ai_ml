# app.py

import streamlit as st

# ==========================
# IMPORT PAGES
# ==========================

from views.dashboard import show as dashboard_page
from views.registration import show as registration_page
from views.qr_attendance import show as qr_page
from views.prediction import show as prediction_page
from views.analytics import show as analytics_page
from views.students import show as students_page
from views.reports import show as reports_page
from views.admin import show as admin_page


# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Event Attendance System",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# CUSTOM CSS
# ==========================

st.markdown(
    """
    <style>

    .main{
        padding-top:1rem;
    }

    section[data-testid="stSidebar"]{
        width:280px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ==========================
# SIDEBAR
# ==========================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
    width=90
)

st.sidebar.title("AI Event System")

st.sidebar.markdown("---")

menu = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Dashboard",

        "👨‍🎓 Student Registration",

        "📷 QR Attendance",

        "🤖 AI Prediction",

        "📊 Analytics",

        "👥 Students",

        "📄 Reports",

        "⚙ Admin"

    ]

)

st.sidebar.markdown("---")

st.sidebar.info(
"""
AI Event Attendance &
Resource Optimization System

Version : 1.0
"""
)

# ==========================
# ROUTING
# ==========================

if menu == "🏠 Dashboard":

    dashboard_page()

elif menu == "👨‍🎓 Student Registration":

    registration_page()

elif menu == "📷 QR Attendance":

    qr_page()

elif menu == "🤖 AI Prediction":

    prediction_page()

elif menu == "📊 Analytics":

    analytics_page()

elif menu == "👥 Students":

    students_page()

elif menu == "📄 Reports":

    reports_page()

elif menu == "⚙ Admin":

    admin_page()

# ==========================
# FOOTER
# ==========================

st.sidebar.markdown("---")

st.sidebar.caption(
    "Developed by Rakesh Boyina"
)
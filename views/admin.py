# pages/admin.py

import streamlit as st
import bcrypt
from database.db import db


def show():

    st.title("⚙ Admin Panel")

    st.markdown("---")

    # =====================================
    # LOGIN
    # =====================================

    if "admin_login" not in st.session_state:
        st.session_state.admin_login = False

    if not st.session_state.admin_login:

        st.subheader("Admin Login")

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            admin = db.fetch_one(
                """
                SELECT *
                FROM admins
                WHERE username=%s
                """,
                (username,)
            )

            if admin:

                if bcrypt.checkpw(
                    password.encode(),
                    admin["password"].encode()
                ):

                    st.session_state.admin_login = True
                    st.success("Login Successful")
                    st.rerun()

                else:

                    st.error("Invalid Password")

            else:

                st.error("Username Not Found")

        return

    # =====================================
    # DASHBOARD
    # =====================================

    st.success("Welcome Admin")

    st.markdown("---")

    total_students = db.fetch_one(
        "SELECT COUNT(*) AS total FROM students"
    )["total"]

    total_attendance = db.fetch_one(
        "SELECT COUNT(*) AS total FROM attendance"
    )["total"]

    total_predictions = db.fetch_one(
        "SELECT COUNT(*) AS total FROM predictions"
    )["total"]

    total_events = db.fetch_one(
        "SELECT COUNT(*) AS total FROM events"
    )["total"]

    c1, c2 = st.columns(2)

    c1.metric("Students", total_students)
    c2.metric("Attendance", total_attendance)

    c3, c4 = st.columns(2)

    c3.metric("Predictions", total_predictions)
    c4.metric("Events", total_events)

    st.markdown("---")

    # =====================================
    # DATABASE STATUS
    # =====================================

    st.subheader("Database Status")

    try:

        db.fetch_one("SELECT 1")

        st.success("🟢 MySQL Connected")

    except Exception:

        st.error("🔴 Database Disconnected")

    st.markdown("---")

    # =====================================
    # MAINTENANCE
    # =====================================

    st.subheader("Maintenance")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("Delete Attendance"):

            db.delete(
                "DELETE FROM attendance",
                ()
            )

            st.success("Attendance Cleared")

    with col2:

        if st.button("Delete Predictions"):

            db.delete(
                "DELETE FROM predictions",
                ()
            )

            st.success("Prediction History Cleared")

    st.markdown("---")

    # =====================================
    # EVENT DETAILS
    # =====================================

    st.subheader("Current Event")

    event = db.fetch_one(
        """
        SELECT *
        FROM events
        ORDER BY event_id DESC
        LIMIT 1
        """
    )

    if event:

        st.write("**Event Name:**", event["event_name"])
        st.write("**Date:**", event["event_date"])
        st.write("**Venue:**", event["venue"])
        st.write("**Venue Limit:**", event["venue_limit"])

    else:

        st.warning("No Event Found")

    st.markdown("---")

    # =====================================
    # LOGOUT
    # =====================================

    if st.button("Logout"):

        st.session_state.admin_login = False

        st.success("Logged Out Successfully")

        st.rerun()
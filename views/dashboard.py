# pages/dashboard.py

import streamlit as st
import pandas as pd
from database.db import db
from config import APP_NAME, VENUE_LIMIT, RICE_PER_PERSON


def show():

    st.title("🏠 Dashboard")
    st.markdown("---")

    # =====================================
    # FETCH DATA
    # =====================================

    total_students = db.fetch_one(
        "SELECT COUNT(*) AS total FROM students"
    )["total"]

    today_attendance = db.fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE DATE(scan_time)=CURDATE()
        """
    )["total"]

    latest_prediction = db.fetch_one(
        """
        SELECT *
        FROM predictions
        ORDER BY prediction_time DESC
        LIMIT 1
        """
    )

    remaining_capacity = VENUE_LIMIT - today_attendance

    attendance_percentage = 0

    if total_students > 0:
        attendance_percentage = round(
            (today_attendance / total_students) * 100,
            2
        )

    # =====================================
    # TOP METRICS
    # =====================================

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Registered Students",
        total_students
    )

    col2.metric(
        "Today's Attendance",
        today_attendance
    )

    col3.metric(
        "Attendance %",
        f"{attendance_percentage}%"
    )

    col4.metric(
        "Remaining Capacity",
        remaining_capacity
    )

    st.markdown("---")

    # =====================================
    # AI PREDICTION
    # =====================================

    st.subheader("🤖 Latest AI Prediction")

    if latest_prediction:

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "Predicted Attendance",
            latest_prediction["predicted_attendance"]
        )

        c2.metric(
            "Rice Needed",
            f'{latest_prediction["rice_needed"]} kg'
        )

        c3.metric(
            "Expected Waste",
            f'{latest_prediction["predicted_waste"]} kg'
        )

        c4, c5, c6 = st.columns(3)

        c4.metric(
            "Peak Hour",
            f'{latest_prediction["peak_hour"]}:00'
        )

        c5.metric(
            "Weather",
            latest_prediction["weather"]
        )

        c6.metric(
            "Registrations",
            latest_prediction["registrations"]
        )

    else:

        st.info("No prediction available.")

    st.markdown("---")

    # =====================================
    # EVENT INFORMATION
    # =====================================

    st.subheader("🎉 Current Event")

    event = db.fetch_one(
        """
        SELECT *
        FROM events
        ORDER BY event_date DESC
        LIMIT 1
        """
    )

    if event:

        left, right = st.columns(2)

        with left:

            st.write("### Event Name")
            st.success(event["event_name"])

            st.write("### Event Date")
            st.info(event["event_date"])

        with right:

            st.write("### Venue")
            st.success(event["venue"])

            st.write("### Venue Capacity")
            st.info(event["venue_limit"])

    else:

        st.warning("No event found.")

    st.markdown("---")

    # =====================================
    # RECENT ATTENDANCE
    # =====================================

    st.subheader("📷 Recent Attendance")

    attendance = db.fetch_all(
        """
        SELECT

        students.roll_number,
        students.student_name,
        students.branch,
        attendance.scan_time

        FROM attendance

        JOIN students

        ON attendance.student_id=students.id

        ORDER BY attendance.scan_time DESC

        LIMIT 10
        """
    )

    if attendance:

        df = pd.DataFrame(attendance)

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No attendance recorded.")

    st.markdown("---")

    # =====================================
    # OVERCROWD WARNING
    # =====================================

    st.subheader("🚨 Venue Status")

    if today_attendance >= VENUE_LIMIT:

        st.error("Venue Capacity Exceeded!")

    elif today_attendance >= VENUE_LIMIT * 0.8:

        st.warning("Venue is almost full.")

    else:

        st.success("Venue capacity is normal.")

    st.markdown("---")

    # =====================================
    # QUICK STATISTICS
    # =====================================

    st.subheader("📈 Quick Statistics")

    left, right = st.columns(2)

    branch = db.fetch_all(
        """
        SELECT

        branch,
        COUNT(*) AS total

        FROM students

        GROUP BY branch
        """
    )

    year = db.fetch_all(
        """
        SELECT

        year,
        COUNT(*) AS total

        FROM students

        GROUP BY year
        """
    )

    with left:

        st.write("### Students by Branch")

        if branch:
            st.dataframe(
                pd.DataFrame(branch),
                width="stretch",
                hide_index=True
            )

    with right:

        st.write("### Students by Year")

        if year:
            st.dataframe(
                pd.DataFrame(year),
                width="stretch",
                hide_index=True
            )

    st.markdown("---")

    st.success("Dashboard Loaded Successfully.")
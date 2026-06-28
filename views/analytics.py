import streamlit as st
import pandas as pd
import plotly.express as px

from database.db import db


def show():

    st.title("📊 Analytics Dashboard")

    st.markdown("---")

    # ===================================
    # BRANCH WISE STUDENTS
    # ===================================

    branch_data = db.fetch_all(
        """
        SELECT
            branch,
            COUNT(*) AS total
        FROM students
        GROUP BY branch
        """
    )

    if branch_data:

        df_branch = pd.DataFrame(branch_data)

        fig = px.bar(
            df_branch,
            x="branch",
            y="total",
            title="Students by Branch",
            text="total"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ===================================
    # YEAR WISE STUDENTS
    # ===================================

    year_data = db.fetch_all(
        """
        SELECT
            year,
            COUNT(*) AS total
        FROM students
        GROUP BY year
        """
    )

    if year_data:

        df_year = pd.DataFrame(year_data)

        fig = px.pie(
            df_year,
            names="year",
            values="total",
            title="Students by Year"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ===================================
    # ATTENDANCE TREND
    # ===================================

    attendance = db.fetch_all(
        """
        SELECT
            DATE(scan_time) AS day,
            COUNT(*) AS total
        FROM attendance
        GROUP BY DATE(scan_time)
        ORDER BY DATE(scan_time)
        """
    )

    if attendance:

        df = pd.DataFrame(attendance)

        fig = px.line(
            df,
            x="day",
            y="total",
            markers=True,
            title="Attendance Trend"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    else:

        st.info("No attendance data available.")

    st.markdown("---")

    # ===================================
    # PREDICTION HISTORY
    # ===================================

    predictions = db.fetch_all(
        """
        SELECT
            prediction_time,
            predicted_attendance,
            rice_needed,
            predicted_waste,
            peak_hour
        FROM predictions
        ORDER BY prediction_time
        """
    )

    if predictions:

        df = pd.DataFrame(predictions)

        fig = px.line(
            df,
            x="prediction_time",
            y="predicted_attendance",
            markers=True,
            title="Predicted Attendance History"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ===================================
    # RICE REQUIREMENT
    # ===================================

    if predictions:

        fig = px.bar(
            df,
            x="prediction_time",
            y="rice_needed",
            title="Rice Requirement"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ===================================
    # PEAK HOURS
    # ===================================

    if predictions:

        fig = px.histogram(
            df,
            x="peak_hour",
            title="Peak Crowd Hours"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    st.markdown("---")

    # ===================================
    # SUMMARY
    # ===================================

    total_students = db.fetch_one(
        "SELECT COUNT(*) AS total FROM students"
    )["total"]

    total_attendance = db.fetch_one(
        "SELECT COUNT(*) AS total FROM attendance"
    )["total"]

    total_predictions = db.fetch_one(
        "SELECT COUNT(*) AS total FROM predictions"
    )["total"]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Students",
        total_students
    )

    c2.metric(
        "Attendance Records",
        total_attendance
    )

    c3.metric(
        "Predictions",
        total_predictions
    )

    st.success("Analytics Loaded Successfully.")
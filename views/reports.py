# pages/reports.py

import streamlit as st
import pandas as pd
from io import BytesIO

from database.db import db


def show():

    st.title("📄 Reports")

    st.markdown("---")

    report_type = st.selectbox(

        "Select Report",

        [

            "Student Report",

            "Attendance Report",

            "Prediction Report"

        ]

    )

    # ==========================================
    # STUDENT REPORT
    # ==========================================

    if report_type == "Student Report":

        students = db.fetch_all(

            """
            SELECT

            roll_number,

            student_name,

            email,

            branch,

            year,

            created_at

            FROM students

            ORDER BY student_name

            """

        )

        if students:

            df = pd.DataFrame(students)

            st.subheader("Student Report")

            st.dataframe(

                df,

                width="stretch",

                hide_index=True

            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(

                label="⬇ Download Student Report",

                data=csv,

                file_name="students_report.csv",

                mime="text/csv"

            )

        else:

            st.warning("No students found.")

    # ==========================================
    # ATTENDANCE REPORT
    # ==========================================

    elif report_type == "Attendance Report":

        attendance = db.fetch_all(

            """

            SELECT

            students.roll_number,

            students.student_name,

            students.branch,

            attendance.scan_time,

            attendance.status

            FROM attendance

            JOIN students

            ON attendance.student_id = students.id

            ORDER BY attendance.scan_time DESC

            """

        )

        if attendance:

            df = pd.DataFrame(attendance)

            st.subheader("Attendance Report")

            st.dataframe(

                df,

                width="stretch",

                hide_index=True

            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(

                label="⬇ Download Attendance Report",

                data=csv,

                file_name="attendance_report.csv",

                mime="text/csv"

            )

        else:

            st.warning("No attendance available.")

    # ==========================================
    # PREDICTION REPORT
    # ==========================================

    elif report_type == "Prediction Report":

        predictions = db.fetch_all(

            """

            SELECT

            prediction_time,

            registrations,

            weather,

            weekend,

            celebrity,

            predicted_attendance,

            rice_needed,

            predicted_waste,

            peak_hour

            FROM predictions

            ORDER BY prediction_time DESC

            """

        )

        if predictions:

            df = pd.DataFrame(predictions)

            st.subheader("Prediction Report")

            st.dataframe(

                df,

                width="stretch",

                hide_index=True

            )

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(

                label="⬇ Download Prediction Report",

                data=csv,

                file_name="prediction_report.csv",

                mime="text/csv"

            )

        else:

            st.warning("No prediction records available.")

    st.markdown("---")

    # ==========================================
    # QUICK SUMMARY
    # ==========================================

    total_students = db.fetch_one(

        "SELECT COUNT(*) AS total FROM students"

    )["total"]

    total_attendance = db.fetch_one(

        "SELECT COUNT(*) AS total FROM attendance"

    )["total"]

    total_predictions = db.fetch_one(

        "SELECT COUNT(*) AS total FROM predictions"

    )["total"]

    col1, col2, col3 = st.columns(3)

    col1.metric(

        "Students",

        total_students

    )

    col2.metric(

        "Attendance Records",

        total_attendance

    )

    col3.metric(

        "Predictions",

        total_predictions

    )

    st.success("Reports Generated Successfully.")
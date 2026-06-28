# pages/students.py

import streamlit as st
import pandas as pd
from database.db import db


def show():

    st.title("👥 Student Management")

    st.markdown("---")

    # =====================================
    # SEARCH
    # =====================================

    search = st.text_input(
        "🔍 Search by Roll Number or Name"
    )

    # =====================================
    # FETCH STUDENTS
    # =====================================

    if search:

        students = db.fetch_all(

            """
            SELECT *

            FROM students

            WHERE

            roll_number LIKE %s

            OR

            student_name LIKE %s

            ORDER BY student_name

            """,

            (

                f"%{search}%",

                f"%{search}%"

            )

        )

    else:

        students = db.fetch_all(

            """
            SELECT *

            FROM students

            ORDER BY student_name
            """

        )

    # =====================================
    # SHOW TABLE
    # =====================================

    st.subheader("Student List")

    if students:

        df = pd.DataFrame(students)

        st.dataframe(

            df,

            width="stretch",

            hide_index=True

        )

    else:

        st.warning("No students found.")

        return

    st.markdown("---")

    # =====================================
    # EDIT STUDENT
    # =====================================

    st.subheader("✏ Edit Student")

    roll = st.text_input(
        "Enter Roll Number"
    )

    if st.button("Load Student"):

        student = db.fetch_one(

            """
            SELECT *

            FROM students

            WHERE roll_number=%s
            """,

            (roll,)

        )

        if student:

            st.session_state["student"] = student

        else:

            st.error("Student not found.")

    if "student" in st.session_state:

        student = st.session_state["student"]

        with st.form("edit_form"):

            name = st.text_input(
                "Student Name",
                student["student_name"]
            )

            email = st.text_input(
                "Email",
                student["email"]
            )

            branch = st.text_input(
                "Branch",
                student["branch"]
            )

            year = st.text_input(
                "Year",
                student["year"]
            )

            update = st.form_submit_button(
                "Update Student"
            )

            if update:

                db.update(

                    """
                    UPDATE students

                    SET

                    student_name=%s,

                    email=%s,

                    branch=%s,

                    year=%s

                    WHERE roll_number=%s
                    """,

                    (

                        name,

                        email,

                        branch,

                        year,

                        student["roll_number"]

                    )

                )

                st.success(
                    "Student Updated Successfully."
                )

                del st.session_state["student"]

    st.markdown("---")

    # =====================================
    # DELETE STUDENT
    # =====================================

    st.subheader("🗑 Delete Student")

    delete_roll = st.text_input(
        "Roll Number to Delete"
    )

    if st.button("Delete Student"):

        exists = db.fetch_one(

            """
            SELECT *

            FROM students

            WHERE roll_number=%s
            """,

            (delete_roll,)

        )

        if exists:

            db.delete(

                """
                DELETE FROM students

                WHERE roll_number=%s
                """,

                (delete_roll,)

            )

            st.success(
                "Student Deleted Successfully."
            )

        else:

            st.error(
                "Student not found."
            )

    st.markdown("---")

    # =====================================
    # TOTAL STUDENTS
    # =====================================

    total = db.fetch_one(

        """
        SELECT COUNT(*) AS total

        FROM students
        """

    )["total"]

    st.metric(

        "Total Registered Students",

        total

    )
# pages/registration.py

import streamlit as st
import qrcode
import os
from database.db import db
from config import QR_FOLDER

# ==============================
# CREATE QR FOLDER
# ==============================

os.makedirs(QR_FOLDER, exist_ok=True)


def show():

    st.title("👨‍🎓 Student Registration")

    with st.form("registration_form"):

        name = st.text_input("Student Name")

        roll = st.text_input("Roll Number")

        email = st.text_input("Email")

        branch = st.selectbox(
            "Branch",
            [
                "CSE",
                "ECE",
                "EEE",
                "MECH",
                "CIVIL"
            ]
        )

        year = st.selectbox(
            "Year",
            [
                "1st Year",
                "2nd Year",
                "3rd Year",
                "4th Year"
            ]
        )

        submit = st.form_submit_button("Register Student")

    if submit:

        # -----------------------------
        # VALIDATION
        # -----------------------------

        if name == "" or roll == "" or email == "":

            st.error("Please fill all fields.")
            return

        # -----------------------------
        # CHECK DUPLICATE ROLL NUMBER
        # -----------------------------

        query = """
        SELECT *
        FROM students
        WHERE roll_number=%s
        """

        student = db.fetch_one(query, (roll,))

        if student:

            st.error("Student already registered.")
            return

        # -----------------------------
        # INSERT INTO DATABASE
        # -----------------------------

        insert_query = """
        INSERT INTO students
        (
            roll_number,
            student_name,
            email,
            branch,
            year
        )
        VALUES
        (%s,%s,%s,%s,%s)
        """

        values = (
            roll,
            name,
            email,
            branch,
            year
        )

        db.insert(insert_query, values)

        # -----------------------------
        # GENERATE QR
        # -----------------------------

        qr_text = roll

        qr = qrcode.make(qr_text)

        qr_path = os.path.join(
            QR_FOLDER,
            f"{roll}.png"
        )

        qr.save(qr_path)

        # -----------------------------
        # SUCCESS
        # -----------------------------

        st.success("Student Registered Successfully!")

        st.image(
            qr_path,
            width=250,
            caption="Generated QR Code"
        )

        with open(qr_path, "rb") as file:

            st.download_button(
                "Download QR",
                file,
                file_name=f"{roll}.png",
                mime="image/png"
            )

    # -----------------------------
    # SHOW REGISTERED STUDENTS
    # -----------------------------

    st.divider()

    st.subheader("Registered Students")

    students = db.fetch_all(
        """
        SELECT
            roll_number,
            student_name,
            email,
            branch,
            year
        FROM students
        ORDER BY student_name
        """
    )

    if students:

        st.dataframe(
            students,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No students registered yet.")
# pages/prediction.py

import streamlit as st
import pandas as pd
import joblib
import os

from database.db import db
from config import MODEL_PATHS, RICE_PER_PERSON


def show():

    st.title("🤖 AI Attendance Prediction")

    st.markdown("---")

    # ===============================
    # LOAD MODELS
    # ===============================

    attendance_model = joblib.load(
        MODEL_PATHS["attendance"]
    )

    waste_model = joblib.load(
        MODEL_PATHS["waste"]
    )

    peak_model = joblib.load(
        MODEL_PATHS["peak"]
    )

    # ===============================
    # INPUTS
    # ===============================

    col1, col2 = st.columns(2)

    with col1:

        registrations = st.number_input(
            "Registrations",
            min_value=0,
            value=300
        )

        weather = st.selectbox(
            "Weather",
            [
                "Good",
                "Rainy"
            ]
        )

    with col2:

        weekend = st.selectbox(
            "Weekend",
            [
                "Yes",
                "No"
            ]
        )

        celebrity = st.selectbox(
            "Celebrity Present",
            [
                "Yes",
                "No"
            ]
        )

    # ===============================
    # CONVERT VALUES
    # ===============================

    weather_value = 0 if weather == "Good" else 1

    weekend_value = 1 if weekend == "Yes" else 0

    celebrity_value = 1 if celebrity == "Yes" else 0

    # ===============================
    # PREDICT BUTTON
    # ===============================

    if st.button("Predict"):

        input_df = pd.DataFrame([{

            "registrations": registrations,

            "weather": weather_value,

            "weekend": weekend_value,

            "celebrity": celebrity_value,

            "morning_tiffin": 1

        }])

        predicted_attendance = int(
            attendance_model.predict(input_df)[0]
        )

        predicted_waste = round(
            waste_model.predict(input_df)[0],
            2
        )

        peak_hour = int(
            peak_model.predict(input_df)[0]
        )

        rice_needed = round(
            predicted_attendance * RICE_PER_PERSON,
            2
        )

        attendance_percentage = 0

        if registrations > 0:

            attendance_percentage = round(
                (predicted_attendance / registrations) * 100,
                2
            )

        # ===============================
        # STORE IN DATABASE
        # ===============================

        db.insert(

            """
            INSERT INTO predictions(

                registrations,

                weather,

                weekend,

                celebrity,

                predicted_attendance,

                rice_needed,

                predicted_waste,

                peak_hour

            )

            VALUES

            (%s,%s,%s,%s,%s,%s,%s,%s)

            """,

            (

                registrations,

                weather,

                weekend_value,

                celebrity_value,

                predicted_attendance,

                rice_needed,

                predicted_waste,

                peak_hour

            )

        )

        # ===============================
        # RESULTS
        # ===============================

        st.success("Prediction Successful")

        st.markdown("---")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Attendance",
            predicted_attendance
        )

        c2.metric(
            "Attendance %",
            f"{attendance_percentage}%"
        )

        c3.metric(
            "Rice Needed",
            f"{rice_needed} kg"
        )

        c4.metric(
            "Peak Hour",
            f"{peak_hour}:00"
        )

        st.markdown("---")

        st.warning(
            f"Expected Rice Waste : {predicted_waste} kg"
        )

        # ===============================
        # AI RECOMMENDATIONS
        # ===============================

        st.subheader("AI Recommendations")

        if predicted_attendance > 450:

            st.success(
                "Increase food counters."
            )

            st.success(
                "Increase water packets."
            )

            st.success(
                "Deploy extra volunteers."
            )

        elif predicted_attendance > 300:

            st.info(
                "Arrange one additional food counter."
            )

        else:

            st.success(
                "Current arrangements are sufficient."
            )

        if predicted_waste > 10:

            st.warning(
                "Reduce rice preparation."
            )

        if weather == "Rainy":

            st.warning(
                "Arrange rain shelters."
            )

        # ===============================
        # OVERCROWD WARNING
        # ===============================

        st.markdown("---")

        venue_limit = 250

        if predicted_attendance > venue_limit:

            st.error(
                "⚠ Overcrowding Risk Detected"
            )

        else:

            st.success(
                "Venue Capacity is Safe."
            )

    # ===============================
    # HISTORY
    # ===============================

    st.markdown("---")

    st.subheader("Prediction History")

    history = db.fetch_all(

        """
        SELECT

        prediction_time,

        registrations,

        predicted_attendance,

        rice_needed,

        predicted_waste,

        peak_hour

        FROM predictions

        ORDER BY prediction_time DESC

        LIMIT 10

        """

    )

    if history:

        st.dataframe(

            history,

            width="stretch",

            hide_index=True

        )

    else:

        st.info(
            "No prediction history available."
        )
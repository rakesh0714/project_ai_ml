import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import os
from streamlit_autorefresh import st_autorefresh

# =====================================
# AUTO REFRESH EVERY 5 SECONDS
# =====================================

st_autorefresh(interval=5000, key="refresh")

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Event System",
    layout="wide"
)

# =====================================
# CHECK MODEL FILES
# =====================================

required_models = [
    "models/attendance_model.pkl",
    "models/waste_model.pkl",
    "models/peak_model.pkl"
]

for model_file in required_models:
    if not os.path.exists(model_file):
        st.error(f"Missing Model File: {model_file}")
        st.stop()

# =====================================
# LOAD AI MODELS
# =====================================

attendance_model = joblib.load(
    "models/attendance_model.pkl"
)

waste_model = joblib.load(
    "models/waste_model.pkl"
)

peak_model = joblib.load(
    "models/peak_model.pkl"
)

# =====================================
# TITLE
# =====================================

st.title("AI Event Attendance & Resource Optimization System")

st.subheader("Bhogi Event Prediction Dashboard")
import qrcode
import csv

# =====================================
# STUDENT REGISTRATION FORM
# =====================================

st.header("Student Registration")

with st.form("registration_form"):

    student_name = st.text_input("Student Name")

    student_id = st.text_input("Roll Number")

    branch = st.selectbox(
        "Branch",
        ["CSE", "ECE", "MECH", "CIVIL", "EEE"]
    )

    year = st.selectbox(
        "Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )

    submit_button = st.form_submit_button(
        "Generate Registration QR"
    )

# =====================================
# WHEN FORM SUBMITTED
# =====================================

if submit_button:

    # Create student data
    student_data = f"""
    ID: {student_id}
    Name: {student_name}
    Branch: {branch}
    Year: {year}
    """

    # =================================
    # GENERATE QR
    # =================================

    qr = qrcode.make(student_data)

    qr_path = f"qr_codes/{student_id}.png"

    qr.save(qr_path)

    # =================================
    # SAVE REGISTRATION DATA
    # =================================

    csv_file = "registered_students/students.csv"

    file_exists = os.path.exists(csv_file)

    with open(csv_file, "a", newline="") as f:

        writer = csv.writer(f)

        # Header
        if not file_exists:
            writer.writerow([
                "Student_ID",
                "Name",
                "Branch",
                "Year"
            ])

        # Data
        writer.writerow([
            student_id,
            student_name,
            branch,
            year
        ])

    # =================================
    # SUCCESS MESSAGE
    # =================================

    st.success("Registration Successful!")

    # Show QR
    st.image(
        qr_path,
        caption="Student Registration QR"
    )

    # Download button
    with open(qr_path, "rb") as file:

        st.download_button(
            label="Download QR Code",
            data=file,
            file_name=f"{student_id}.png",
            mime="image/png"
        )

# =====================================
# USER INPUTS
# =====================================

col1, col2 = st.columns(2)

with col1:

    registrations = st.number_input(
        "Registrations",
        min_value=0,
        max_value=5000,
        value=300
    )

    weather = st.selectbox(
        "Weather",
        ["Good", "Rainy"]
    )

with col2:

    weekend = st.selectbox(
        "Weekend",
        ["Yes", "No"]
    )

    celebrity = st.selectbox(
        "Celebrity Present",
        ["Yes", "No"]
    )

# =====================================
# CONVERT INPUTS
# =====================================

weather_val = 0 if weather == "Good" else 1

weekend_val = 1 if weekend == "Yes" else 0

celebrity_val = 1 if celebrity == "Yes" else 0

# =====================================
# CREATE INPUT DATAFRAME
# =====================================

input_data = pd.DataFrame([{
    "registrations": registrations,
    "weather": weather_val,
    "weekend": weekend_val,
    "celebrity": celebrity_val,
    "morning_tiffin": 1
}])

# =====================================
# PREDICTION BUTTON
# =====================================

if st.button("Predict Event Details"):

    # Attendance Prediction
    predicted_attendance = int(
        attendance_model.predict(input_data)[0]
    )

    # Waste Prediction
    predicted_waste = round(
        waste_model.predict(input_data)[0],
        2
    )

    # Peak Crowd Prediction
    peak_hour = int(
        peak_model.predict(input_data)[0]
    )

    # Attendance Percentage
    attendance_percentage = round(
        (predicted_attendance / registrations) * 100,
        2
    )

    # Rice Calculation
    rice_needed = round(
        predicted_attendance * 0.15,
        2
    )

    # =================================
    # METRICS
    # =================================

    st.subheader("Prediction Results")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Predicted Attendance",
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

    # =================================
    # EXTRA RESULTS
    # =================================

    st.warning(
        f"Expected Rice Waste: {predicted_waste} kg"
    )

    st.info(
        f"Peak Crowd Time: {peak_hour} AM"
    )

    # =================================
    # OVERCROWDING ALERT
    # =================================

    venue_limit = 250

    if predicted_attendance > venue_limit:
        st.error("⚠ Overcrowding Risk Detected!")

    else:
        st.success("Crowd Level Normal")

    # =================================
    # AI RECOMMENDATIONS
    # =================================

    st.subheader("AI Recommendations")

    if predicted_waste > 10:
        st.write("✅ Reduce rice preparation")

    if predicted_attendance > 350:
        st.write("✅ Add 2 more food counters")

    if predicted_attendance > 450:
        st.write("✅ Increase water packets")

# =====================================
# LIVE ATTENDANCE SYSTEM
# =====================================

st.subheader("Live Attendance Monitoring")

attendance_file = "attendance/attendance.csv"

if os.path.exists(attendance_file):

    attendance_data = pd.read_csv(attendance_file)

    current_attendance = len(attendance_data)

    live_rice_needed = round(
        current_attendance * 0.15,
        2
    )

    # =================================
    # LIVE METRICS
    # =================================

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "Current Attendance",
        current_attendance
    )

    m2.metric(
        "Live Rice Needed",
        f"{live_rice_needed} kg"
    )

    venue_limit = 250

    remaining_capacity = venue_limit - current_attendance

    m3.metric(
        "Remaining Capacity",
        remaining_capacity
    )

    # =================================
    # LIVE OVERCROWD ALERT
    # =================================

    if current_attendance > venue_limit:
        st.error("⚠ LIVE OVERCROWDING ALERT!")

    # =================================
    # LIVE ATTENDANCE TABLE
    # =================================

    st.subheader("Recent QR Scans")

    st.dataframe(
        attendance_data.tail(10),
        use_container_width=True
    )

    # =================================
    # LIVE ATTENDANCE GRAPH
    # =================================

    attendance_data["Scan_Number"] = range(
        1,
        len(attendance_data) + 1
    )

    fig_live = px.line(
        attendance_data,
        x="Scan_Number",
        title="Live Attendance Growth"
    )

    st.plotly_chart(
        fig_live,
        use_container_width=True
    )

else:

    st.warning("No attendance data found!")

# =====================================
# HISTORICAL EVENT GRAPH
# =====================================

st.subheader("Historical Attendance Trend")

event_data = pd.read_csv(
    "datasets/bhogi_event.csv"
)

fig = px.line(
    event_data,
    x="date",
    y="actual_attendance",
    title="Bhogi Event Attendance Trend",
    markers=True
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.caption(
    "AI-Based Event Attendance & Resource Optimization System"
)
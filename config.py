# ==============================
# DATABASE CONFIGURATION
# ==============================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Rakesh@1439",
    "database": "ai_event_system"
}
# ==============================
# APPLICATION CONFIGURATION
# ==============================

APP_NAME = "AI Event Attendance & Resource Optimization System"

VENUE_LIMIT = 250

RICE_PER_PERSON = 0.15

QR_FOLDER = "qr_codes"

MODEL_PATHS = {
    "attendance": "models/attendance_model.pkl",
    "waste": "models/waste_model.pkl",
    "peak": "models/peak_model.pkl"
}
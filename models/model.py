import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import joblib

# ==============================
# LOAD DATASET
# ==============================

data = pd.read_csv("datasets/bhogi_event.csv")

# ==============================
# INPUT FEATURES
# ==============================

X = data[[
    "registrations",
    "weather",
    "weekend",
    "celebrity",
    "morning_tiffin"
]]

# ==============================
# TARGETS
# ==============================

attendance_target = data["actual_attendance"]

waste_target = data["rice_wasted_kg"]

peak_target = data["peak_hour"]

# ==============================
# TRAIN TEST SPLIT
# ==============================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    attendance_target,
    test_size=0.2,
    random_state=42
)

# ==============================
# ATTENDANCE MODEL
# ==============================

attendance_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

attendance_model.fit(X_train, y_train)

# ==============================
# WASTE PREDICTION MODEL
# ==============================

waste_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

waste_model.fit(X, waste_target)

# ==============================
# PEAK CROWD MODEL
# ==============================

peak_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

peak_model.fit(X, peak_target)

# ==============================
# SAVE MODELS
# ==============================

joblib.dump(attendance_model, "attendance_model.pkl")

joblib.dump(waste_model, "waste_model.pkl")

joblib.dump(peak_model, "peak_model.pkl")

# ==============================
# SUCCESS MESSAGE
# ==============================

print("===================================")
print(" All AI Models Trained Successfully!")
print("===================================")

print("\nSaved Models:")
print("attendance_model.pkl")
print("waste_model.pkl")
print("peak_model.pkl")
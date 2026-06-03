import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Load dataset
data = pd.read_csv("datasets/bhogi_event.csv")

# Input features
X = data[["registrations", "weather", "weekend", "celebrity"]]

# Target output
y = data["actual_attendance"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create AI model
model = RandomForestRegressor()

# Train model
model.fit(X_train, y_train)

print("AI Model Trained Successfully!")

# -----------------------------
# Predict New Event Attendance
# -----------------------------

print("\nEnter New Event Details")

registrations = int(input("Registrations: "))
weather = int(input("Weather (0=Good, 1=Rainy): "))
weekend = int(input("Weekend? (1=Yes, 0=No): "))
celebrity = int(input("Celebrity Present? (1=Yes, 0=No): "))

# Predict attendance
new_event = pd.DataFrame([{
    "registrations": registrations,
    "weather": weather,
    "weekend": weekend,
    "celebrity": celebrity
}])

prediction = model.predict(new_event)
predicted_attendance = int(prediction[0])

print("\n========== RESULT ==========")
print(f"Predicted Attendance: {predicted_attendance}")

# Food estimation
rice_needed = predicted_attendance * 0.15

print(f"Estimated Rice Needed: {rice_needed:.2f} kg")

# Crowd warning
if predicted_attendance > 800:
    print("ALERT: Very High Crowd Expected!")

elif predicted_attendance > 500:
    print("Moderate Crowd Expected")

else:
    print("Low Crowd Expected")
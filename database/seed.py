from database.db import db

# ==========================================
# INSERT DEFAULT EVENT
# ==========================================

event_query = """
INSERT INTO events
(
    event_name,
    event_date,
    venue,
    venue_limit
)
VALUES
(%s,%s,%s,%s)
"""

event_data = (
    "Bhogi Festival",
    "2026-01-13",
    "SVNIT Ground",
    250
)

existing_event = db.fetch_one(
    """
    SELECT *
    FROM events
    WHERE event_name=%s
    """,
    ("Bhogi Festival",)
)

if not existing_event:

    db.insert(event_query, event_data)

    print("✅ Default event inserted.")

else:

    print("⚡ Event already exists.")

# ==========================================
# INSERT SAMPLE STUDENTS
# ==========================================

students = [

    (
        "U23CS001",
        "Rakesh",
        "rakesh@gmail.com",
        "CSE",
        "4th Year"
    ),

    (
        "U23CS002",
        "Rahul",
        "rahul@gmail.com",
        "CSE",
        "4th Year"
    ),

    (
        "U23EC001",
        "Anil",
        "anil@gmail.com",
        "ECE",
        "4th Year"
    )

]

for student in students:

    exists = db.fetch_one(

        """
        SELECT *
        FROM students
        WHERE roll_number=%s
        """,

        (student[0],)

    )

    if not exists:

        db.insert(

            """
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
            """,

            student

        )

print("✅ Sample students inserted.")

# ==========================================
# INSERT SAMPLE PREDICTION
# ==========================================

prediction_exists = db.fetch_one(
    "SELECT * FROM predictions LIMIT 1"
)

if not prediction_exists:

    db.insert(

        """
        INSERT INTO predictions
        (
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
            300,
            "Good",
            True,
            False,
            280,
            42,
            5,
            11
        )

    )

    print("✅ Sample prediction inserted.")

else:

    print("⚡ Prediction already exists.")

print("\nDatabase seeded successfully.")
# pages/qr_attendance.py

import streamlit as st
import cv2
from database.db import db


def show():

    st.title("📷 QR Attendance")

    st.info("Click the button below and scan the student's QR Code.")

    if st.button("Start QR Scanner"):

        detector = cv2.QRCodeDetector()
        cap = cv2.VideoCapture(0)

        status = st.empty()

        while True:

            ret, frame = cap.read()

            if not ret:
                status.error("Unable to access webcam.")
                break

            data, bbox, _ = detector.detectAndDecode(frame)

            if bbox is not None:

                bbox = bbox.astype(int)

                for i in range(len(bbox[0])):

                    pt1 = tuple(bbox[0][i])
                    pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])

                    cv2.line(
                        frame,
                        pt1,
                        pt2,
                        (0,255,0),
                        2
                    )

            if data:

                roll_number = data.strip()

                student = db.fetch_one(
                    """
                    SELECT *
                    FROM students
                    WHERE roll_number=%s
                    """,
                    (roll_number,)
                )

                if student:

                    already = db.fetch_one(
                        """
                        SELECT *
                        FROM attendance
                        WHERE student_id=%s
                        AND DATE(scan_time)=CURDATE()
                        """,
                        (student["id"],)
                    )

                    if already:

                        status.warning(
                            f"{student['student_name']} is already marked present."
                        )

                    else:

                        db.insert(
                            """
                            INSERT INTO attendance
                            (
                                student_id,
                                status
                            )
                            VALUES
                            (%s,%s)
                            """,
                            (
                                student["id"],
                                "Present"
                            )
                        )

                        status.success(
                            f"Attendance marked for {student['student_name']}"
                        )

                else:

                    status.error("Student not found.")

                cv2.waitKey(1500)
                break

            cv2.imshow(
                "QR Attendance Scanner",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()

    st.markdown("---")

    st.subheader("Today's Attendance")

    attendance = db.fetch_all(
        """
        SELECT

        students.roll_number,
        students.student_name,
        students.branch,
        attendance.scan_time

        FROM attendance

        JOIN students

        ON attendance.student_id = students.id

        WHERE DATE(attendance.scan_time)=CURDATE()

        ORDER BY attendance.scan_time DESC
        """
    )

    if attendance:

        st.dataframe(
            attendance,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No attendance recorded today.")

    st.markdown("---")

    total = db.fetch_one(
        """
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE DATE(scan_time)=CURDATE()
        """
    )["total"]

    st.metric(
        "Today's Attendance",
        total
    )
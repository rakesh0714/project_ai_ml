import cv2

# Open webcam
cap = cv2.VideoCapture(0)

# QR detector
detector = cv2.QRCodeDetector()

print("QR Scanner Started...")

while True:

    ret, frame = cap.read()

    if not ret:
        break

    # Detect QR
    data, bbox, _ = detector.detectAndDecode(frame)

    if data:

        print("Attendance Marked:", data)

        # Draw box
        if bbox is not None:

            bbox = bbox.astype(int)

            for i in range(len(bbox[0])):
                pt1 = tuple(bbox[0][i])
                pt2 = tuple(bbox[0][(i + 1) % len(bbox[0])])

                cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        cv2.putText(
            frame,
            f"Scanned: {data}",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("QR Attendance Scanner", frame)

    # Press q to exit
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
import qrcode

# Your registration page link
event_link = "https://abc123.ngrok-free.app"

# Generate QR
qr = qrcode.make(event_link)

# Save QR
qr.save("event_registration_qr.png")

print("Event QR Generated Successfully!")
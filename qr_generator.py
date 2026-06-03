import qrcode

student_id = input("Enter Student ID: ")

img = qrcode.make(student_id)

img.save(f"{student_id}.png")

print("QR Generated Successfully!")
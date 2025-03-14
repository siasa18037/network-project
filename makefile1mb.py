import os
import random
import string

# กำหนดขนาดไฟล์ 1MB (1048576 ไบต์)
target_size = 1048576  

# สุ่มตัวอักษรและตัวเลขให้ได้ขนาดพอดี
file_content = ''.join(random.choices(string.ascii_letters + string.digits, k=target_size))

# บันทึกลงไฟล์
file_path = "test.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(file_content)

# ตรวจสอบขนาดไฟล์
print(f"ขนาดไฟล์: {os.path.getsize(file_path)} ไบต์")

import os
# สร้างไฟล์ใหม่ที่มีขนาด 1MB อย่างแม่นยำ
target_size = 1048576  # 1MB ในหน่วยไบต์
text = "A"  # ใช้ตัวอักษรเดียวเพื่อลดขนาดที่เกินมา

# สร้างเนื้อหาของไฟล์ให้พอดี 1MB
file_content = text * target_size

# บันทึกไฟล์ใหม่
file_path = "test.txt"
with open(file_path, "w", encoding="utf-8") as file:
    file.write(file_content)

# ตรวจสอบขนาดไฟล์
os.path.getsize(file_path)

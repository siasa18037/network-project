import subprocess

def get_md5sum(file_path):
    """ คำนวณค่า MD5 ของไฟล์โดยใช้คำสั่ง md5sum """
    result = subprocess.run(['md5sum', file_path], stdout=subprocess.PIPE, text=True)
    return result.stdout.split()[0]  # ค่าผลลัพธ์ MD5 จะอยู่ในตำแหน่งแรก

def compare_files(file1, file2):
    """ ตรวจสอบว่าไฟล์สองไฟล์มีเนื้อหาตรงกันหรือไม่ """
    return get_md5sum(file1) == get_md5sum(file2)

# ตัวอย่างการใช้งาน
file1 = "test/test.txt"
file2 = "test.txt"

if compare_files(file1, file2):
    print("ไฟล์ทั้งสองเหมือนกัน ✅")
else:
    print("ไฟล์ทั้งสองแตกต่างกัน ❌")

import subprocess

def get_md5sum(file_path):
    """ คำนวณค่า MD5 ของไฟล์โดยใช้คำสั่ง certutil ใน Windows """
    result = subprocess.run(['certutil', '-hashfile', file_path, 'MD5'], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
    if result.returncode == 0:
        # certutil จะให้ผลลัพธ์ MD5 ในบรรทัดที่สอง
        return result.stdout.splitlines()[1].strip()
    else:
        return None

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

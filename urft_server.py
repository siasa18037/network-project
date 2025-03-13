import socket
import sys
import os
from datetime import datetime as dt

buf = 1024  # ขนาด buffer
timeout = 60  # ระยะเวลา timeout
sep = '/||/'  # ตัวแบ่งข้อมูลใน packet

file_name = ''
file_data = bytearray()  # ใช้ bytearray เพื่อเก็บข้อมูลไบนารี
expected_seq = 0  # ลำดับ packet ที่คาดหวัง


if len(sys.argv) < 3:
    print("python urft_server.py <IP เซิร์ฟเวอร์> <พอร์ตเซิร์ฟเวอร์>")
    sys.exit(1)

# สร้าง UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (sys.argv[1], int(sys.argv[2]))
server_socket.bind(server_address)
server_socket.settimeout(timeout)

print("เซิร์ฟเวอร์พร้อมทำงาน")
while True:
    try:
        # รับข้อมูลจาก client
        data, client_address = server_socket.recvfrom(buf + 20)
        packet_parts = data.split(sep.encode('utf-8'))  # แยกข้อมูลไบนารี

        seq = int(packet_parts[0].decode('utf-8'))  # ลำดับ packet
        payload = packet_parts[1]  # ข้อมูล payload

        print(f"กำลังรับแพ็กเก็ตลำดับที่: {seq}, ลำดับที่คาดหวัง: {expected_seq}")
        
        if seq == -2:  # เริ่มต้นการส่ง (ส่งชื่อไฟล์)
            file_name = os.path.basename(payload.decode('utf-8'))  # ใช้เฉพาะชื่อไฟล์ ไม่รวม path
            server_socket.sendto(f"ACK{sep}{dt.now()}".encode('utf-8'), client_address)
            print(f"ได้รับชื่อไฟล์: {file_name}")
            continue
        if seq == -1:  # สิ้นสุดการส่ง
            print("การรับไฟล์เสร็จสิ้น!")
            packet = f'FIN{sep}{seq}'.encode('utf-8')
            server_socket.sendto(packet, client_address)
            break
        if seq == expected_seq:  # รับ packet ตามลำดับที่คาดหวัง
            file_data.extend(payload)  # เพิ่มข้อมูลไบนารี
            expected_seq += buf  # อัปเดตลำดับที่คาดหวัง
            server_socket.sendto(f"ACK{sep}{expected_seq}".encode('utf-8'), client_address)
            print(f"ส่ง ACK: {expected_seq}")
        else:
            print(f"ได้รับแพ็กเก็ตลำดับไม่ตรงกัน : {expected_seq}, ได้รับ: {seq}")

    except socket.timeout:
        print("ไม่มีการเชื่อมต่อ หรือหมดเวลาเชื่อมต่อ")
        break

server_socket.close()

# บันทึกข้อมูลลงไฟล์
if file_name:
    try:
        with open(file_name, "wb") as file:
            file.write(file_data)
        print(f"บันทึกไฟล์สำเร็จ: {file_name}")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการบันทึกไฟล์: {e}")


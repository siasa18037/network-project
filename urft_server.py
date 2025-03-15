import socket
import sys
import os
from datetime import datetime as dt

buf = 1024
timeout = 60
sep = b'/||/'  # เปลี่ยนเป็น bytes แทน string
file_name = ''
file_data = bytearray()
expected_seq = 0
wndw = {}

if len(sys.argv) < 3:
    print("python urft_server.py <server_ip> <server_port>")
    sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (sys.argv[1], int(sys.argv[2]))
server_socket.bind(server_address)
server_socket.settimeout(timeout)

print("--------- Server online พร้อมรับข้อมูล ---------")

while True:
    try:
        data, client_address = server_socket.recvfrom(buf + 20)
        packet_parts = data.split(sep)  # ใช้ bytes แยกข้อมูล

        seq = int(packet_parts[0].decode('utf-8'))  # แปลงค่า seq เป็น int
        payload = packet_parts[1]  # ดึงข้อมูลไบต์ออกมาโดยไม่ decode

        print(f"กำลังรับข้อมูล SEQ: {seq} คาดหวัง: {expected_seq} 📨")

        if seq == -2:  # รับชื่อไฟล์
            file_name = payload.decode("utf-8")  # ถอดรหัสเฉพาะชื่อไฟล์
            server_socket.sendto(b"ACK" + sep + dt.now().strftime("%Y-%m-%d %H:%M:%S.%f").encode('utf-8'), client_address)
            print(f"ได้รับชื่อไฟล์แล้ว 📂: {file_name}")
            continue

        if seq == -1:  # สิ้นสุดการรับไฟล์
            print("เสร็จสิ้นการรับไฟล์! ✅")
            packet = sep + str(seq).encode('utf-8')
            server_socket.sendto(packet, client_address)
            break

        wndw[seq] = payload  # จัดเก็บข้อมูลที่ได้รับ

        while expected_seq in wndw:
            file_data.extend(wndw[expected_seq])  # รวมข้อมูลไบต์
            expected_seq += buf

        server_socket.sendto(b"ACK" + sep + str(expected_seq).encode('utf-8'), client_address)
        print(f"กำลังส่ง ACK: {expected_seq} 📨")

    except socket.timeout:
        print("ไม่พบการเชื่อมต่อจากไคลเอนต์แล้ว ⏳")
        break

    except ConnectionResetError:
        print("การเชื่อมต่อถูกปิดโดยเซิร์ฟเวอร์ หรือการเชื่อมต่อล้มเหลว ⛔")

server_socket.close()

with open(file_name, "wb") as file:
    file.write(file_data)

print(f"ไฟล์ {file_name} ถูกบันทึกเรียบร้อยแล้ว! 🎉")
print("--------- จบการทำงานเเล้ว ---------")

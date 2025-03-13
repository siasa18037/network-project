import socket
import sys
from datetime import datetime as dt

buf = 1024  # ขนาด buffer
timeout = 1.0  # ระยะเวลา timeout
sep = '/||/'  # ตัวแบ่งข้อมูลใน packet
current_ack = 0  # ลำดับ packet ที่รอรับ ACK


if len(sys.argv) < 4:
    print("python urft_client.py <เส้นทางไฟล์> <IP เซิร์ฟเวอร์> <พอร์ตเซิร์ฟเวอร์>")
    sys.exit(1)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)
server_address = (sys.argv[2], int(sys.argv[3]))


# อ่านไฟล์ที่ต้องการส่ง
with open(sys.argv[1], 'rb') as file:
    file_data = file.read()
    print(f"อ่านไฟล์สำเร็จ: {sys.argv[1]}")

file_size = len(file_data)

# ส่งชื่อไฟล์ไปยังเซิร์ฟเวอร์
while True:
    sender_time = dt.now()
    packet = f'-2{sep}{sys.argv[1]}'.encode('utf-8')
    client_socket.sendto(packet, server_address)
    try:
        ack_data, server = client_socket.recvfrom(buf)
        ack, time = ack_data.decode('utf-8').split(sep)
        if ack == "ACK":
            time = dt.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
            rtt = (time - sender_time).total_seconds()
            print(f"เริ่มส่งข้อมูลด้วยค่า RTT: {rtt}")
            break
    except socket.timeout:
        print("--หมดเวลารอ ติดส่งใหม่อีกครั้ง--")

# ส่งข้อมูลไฟล์
while current_ack < file_size:
    chunk = file_data[current_ack:current_ack + buf]
    packet = f"{current_ack}{sep}".encode('utf-8') + chunk
    client_socket.sendto(packet, server_address)
    print(f"กำลังส่งแพ็กเก็ตที่: {current_ack}")

    try:
        ack_data, server = client_socket.recvfrom(40)
        ack_parts = ack_data.decode('utf-8').split(sep)
        ack_seq = int(ack_parts[1])
        if ack_seq == current_ack + buf:
            current_ack = ack_seq
            print(f"ได้รับ ACK: {current_ack}")
    except socket.timeout:
        print("--หมดเวลารอ ติดส่งใหม่อีกครั้ง--")

# ส่งแพ็กเก็ตสิ้นสุดการส่ง
packet = f'-1{sep}FIN'.encode('utf-8')
client_socket.sendto(packet, server_address)
print("กำลังส่งแพ็กเก็ตสุดท้าย")

client_socket.close()

print("ส่งไฟล์เสร็จสิ้นเรียบร้อย!")
print("จบการทำงาน !!!!")


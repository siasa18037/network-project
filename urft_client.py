import socket
import sys
from datetime import datetime as dt
import os

buf = 1024
timeout = 0.25
sep = '/||/'
current_ack = 0

if len(sys.argv) < 4:
    print("python urft_client.py <file_path> <server_ip> <server_port>")  # แสดงวิธีการใช้โปรแกรม
    sys.exit(1)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(timeout)
server_address = (sys.argv[2], int(sys.argv[3]))
client_socket.setblocking(True)

file_path = sys.argv[1]
file_name = os.path.basename(file_path) 

with open(file_path, 'rb') as file:
    file_data = file.read()
    print("อ่านไฟล์เรียบร้อยแล้ว 📖")

file_size = len(file_data)

while True:
    sender_time = dt.now()
    packet = f'-2{sep}{file_name}'.encode('utf-8')  
    client_socket.sendto(packet, server_address)
    
    try:
        ack_data, server = client_socket.recvfrom(buf)
        ack, time = ack_data.decode('utf-8').split(sep) 
        
        if ack != "ACK": 
            continue

        time = dt.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
        rtt = (time.microsecond - sender_time.microsecond) * 0.000001
        client_socket.settimeout(timeout)
        
        print(f"เริ่มส่งข้อมูลพร้อม RTT: {rtt} วินาที ⏱️")
        
        break

    except socket.timeout:
        print("--หมดเวลา รีเทรานสมิชชันใหม่ ⏳--")

while True:
    
    if current_ack == -1: 
        break

    if current_ack >= file_size:
        packet = f'-1{sep}FIN'.encode('utf-8')
        client_socket.sendto(packet, server_address)
        print(f"กำลังส่ง FIN: {current_ack} 📤")

    print(f"กำลังส่ง SEQ: {current_ack} - {file_size - buf} 📦")
    
    for seq in range(current_ack, file_size, buf):  
        chunk = file_data[seq: seq + buf]
        packet = f"{seq}{sep}".encode('utf-8') + chunk
        client_socket.sendto(packet, server_address)

    try:
        while True:
            ack_data, server = client_socket.recvfrom(40) 
            ack_parts = ack_data.decode('utf-8').split(sep)  

            flag = ack_parts[0]
            current_ack = int(ack_parts[1])
            print(f'รับ ACK จาก {flag}: {current_ack} 📨')

            if flag == 'END':
                break

    except socket.timeout:
        print("--หมดเวลา รีเทรานสมิชชันใหม่ ⏳--")
        
    except ConnectionResetError as e:
        print("การเชื่อมต่อถูกปิดโดยเซิร์ฟเวอร์ หรือการเชื่อมต่อล้มเหลว ⛔")


print("ส่งไฟล์เสร็จเรียบร้อยแล้ว 🎉")
print("--------- จบการทำงานเเล้ว ---------")
client_socket.close()

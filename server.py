# Server
import socket
import json

host = '192.168.10.4'  # Server ip
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))

while True:
    data, addr = s.recvfrom(1024)
    # print(str(addr))
    message = json.dumps({"msg": 'success'})
    s.sendto(message.encode(), addr)



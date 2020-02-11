# Server
import socket
import json

port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))

print("Server Started")
while True:
    data, addr = s.recvfrom(1024)
    data = json.loads(data.decode())
    # print(str(addr), data.get("msg"))
    message = json.dumps({"msg": 'success'})
    s.sendto(message.encode(), addr)
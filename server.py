# Server
import socket
import json
import numpy as np
import dill


title = 'edge-m1/autoencoder.h5'
with open(title, 'rb') as pickle_file:
    clf = dill.load(pickle_file)

host = '192.168.10.3'  # Server ip
port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

print("Server Started")
while True:
    data, addr = s.recvfrom(1024)
    data = json.loads(data.decode())
    x_test_subset = np.array(data.get("msg"))
    print("Message from: " + str(addr))
    print("From connected user: ", len(x_test_subset))
    y_test_pred = clf.predict(x_test_subset)
    message = json.dumps({"msg": y_test_pred})
    s.sendto(message.encode(), addr)
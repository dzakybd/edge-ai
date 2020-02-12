# Server
import numpy as np
import socket
import json
from keras.models import load_model

title = 'model_cloud.h5'
# title = 'model_edge.h5'
# title = 'model_all.h5'

clf = load_model(title)


port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', port))

while True:
    data, addr = s.recvfrom(1024)
    data = json.loads(data.decode())
    x = np.array(data.get("msg"))
    x = np.array(x).reshape(1, -1)
    y = clf.predict(x)
    y = np.array(y).tolist()
    message = json.dumps({"msg": y})
    s.sendto(message.encode(), addr)



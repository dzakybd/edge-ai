# Server
import numpy as np
import socket
import json
from keras.models import load_model

title = 'model_all.h5'


clf = load_model(title)


port = 4000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))

s.listen(1)
while True:
    print('waiting for a connection')
    connection, client_address = s.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        msg = ''
        while True:
            data = connection.recv(16)

            if data:
                temp = data.decode()
                if '!' in temp:
                    msg += temp[:-1]
                    data = json.loads(msg)
                    x = np.array(data.get("msg"))
                    x = np.array(x).reshape(1, -1)
                    y = clf.predict_classes(x)
                    y = np.array(y).tolist()
                    message = json.dumps({"msg": y}).encode()
                    print('send result', y)
                    connection.send(message)
                    msg = ''
                else:
                    msg += temp
            else:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        print("Closing current connection")
        connection.close()



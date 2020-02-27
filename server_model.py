# Server
import numpy as np
import socket
import json
import pickle
from keras.models import load_model

dir_model = 'model/'

use_nn = False
# title = 'model_lr.pkl'
# title = 'model_nb.pkl'
# title = 'model_dt.pkl'
# title = 'model_svm.pkl'
title = 'model_knn.pkl'

# use_nn = True
# title = 'model_all.h5'
# title = 'model_cloud.h5'
# title = 'model_edge_pca.h5'
# title = 'model_edge_cfs_60.h5'
# title = 'model_edge_clfs_20.h5'
# title = 'model_edge_clfs_40.h5'
# title = 'model_edge_clfs_60.h5'
# title = 'model_edge_clfs_80.h5'
# title = 'model_edge_clfs_100.h5'

print('Test using', title)

if use_nn:
    clf = load_model(dir_model+title)
else:
    clf = pickle.load(open(dir_model+title, 'rb'))

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
                    if use_nn:
                        y = clf.predict_classes(x)
                    else:
                        y = clf.predict(x)
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



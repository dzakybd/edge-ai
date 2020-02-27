# Client
import datetime
import socket
import json
import pandas as pd
import pickle
import numpy as np
import time

dir_prepro = 'prepro/'
dir_featsel = 'featsel/'
dir_shared = 'shared/'


# ip = '128.199.240.41'
# name = 'cloud'

ip = '192.168.10.4'
name = 'edge'

server = (ip, 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server)

# teston = 'all'
# teston = 'cloud'
# teston = 'pca'
# teston = 'cfs_60'
# teston = 'clfs_20'
# teston = 'clfs_40'
# teston = 'clfs_60'
# teston = 'clfs_80'
# teston = 'clfs_100'

# teston = 'lr'
# teston = 'nb'
# teston = 'dt'
# teston = 'svm'
teston = 'knn'

print('teston', teston)

data_prepro_sample = pd.read_pickle(dir_prepro+'data_prepro_sample.pkl')
x_sample = data_prepro_sample.iloc[:, :-1]

if teston == 'cloud':
    with open(dir_featsel+'variables_cloud.pkl', 'rb') as pickle_file:
        variables_cloud = pickle.load(pickle_file)
    x_sample = x_sample.loc[:, variables_cloud]
elif teston == 'all':
    x_sample = x_sample
elif teston == 'lr' or teston == 'nb' or teston == 'dt' or teston == 'svm' or teston == 'knn':
    with open(dir_featsel+'variables_edge_clfs_60.pkl', 'rb') as pickle_file:
        variables_edge = pickle.load(pickle_file)
    x_sample = x_sample.loc[:, variables_edge]
elif teston == 'pca':
    # x_train_pca = pd.read_pickle(dir_featsel + 'x_train_pca.pkl')
    x_sample = pd.read_pickle(dir_featsel + 'x_test_pca.pkl')
else:
    with open(dir_featsel+'variables_edge_{}.pkl'.format(teston), 'rb') as pickle_file:
        variables_edge = pickle.load(pickle_file)
    x_sample = x_sample.loc[:, variables_edge]

print('shape', x_sample.shape)

min_time = max_time = var_time = 0

while min_time <= 0 or max_time <= 0 or var_time <= 0:
    info = np.ones(300)
    info = info.tolist()
    min_time = 9999
    max_time = -1
    var_time = 0
    try:
        response = []
        for idx, x in enumerate(x_sample.values):
            start = datetime.datetime.now()
            x = x.tolist()
            message = json.dumps({"msg": x, "info": info}).encode()
            s.sendall(message)
            s.send(b'!')
            data = s.recv(16)
            temp = data.decode()
            data = json.loads(temp)
            y = data.get("msg")
            print(idx, y)
            end = datetime.datetime.now()
            interval = (end - start).microseconds / 1000
            if interval < min_time:
                min_time = interval
            if interval > max_time:
                max_time = interval
            response.append(interval)
            if idx == 49:
                break
    finally:
        print('End')

    var_time = np.var(response)
    print('min_time', min_time)
    print('max_time', max_time)
    print('var_time', var_time)
    time.sleep(3)

s.close()
response_data = pd.DataFrame(response, columns=['Time'])
response_data.to_csv(dir_shared+'{}_{}_response_time.csv'.format(name, teston))
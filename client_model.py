# Client
import datetime
import socket
import json
import pandas as pd
import pickle
from tqdm import tqdm

# ip = '128.199.240.41'
ip = '192.168.10.4'
server = (ip, 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(server)

# teston = 'all'
# teston = 'cloud'
# teston = 'edge'

# teston = 'lr'
# teston = 'nb'
# teston = 'dt'
# teston = 'svm'
teston = 'knn'

print('teston', teston)

data_prepro_sample = pd.read_pickle('data_prepro_sample.pkl')
x_sample = data_prepro_sample.iloc[:, :-1]

if teston == 'cloud':
    with open('variables_cloud.pkl', 'rb') as pickle_file:
        variables_cloud = pickle.load(pickle_file)
    x_sample = x_sample.loc[:, variables_cloud]
elif teston == 'all':
    x_sample = x_sample
else:
    with open('variables_edge.pkl', 'rb') as pickle_file:
        variables_edge = pickle.load(pickle_file)
    x_sample = x_sample.loc[:, variables_edge]

try:
    response = []
    for idx, x in enumerate(x_sample.values):
        start = datetime.datetime.now()
        x = x.tolist()
        message = json.dumps({"msg": x}).encode()
        s.sendall(message)
        s.send(b'!')
        data = s.recv(16)
        temp = data.decode()
        data = json.loads(temp)
        y = data.get("msg")
        print(idx, y)
        end = datetime.datetime.now()
        interval = (end - start).microseconds / 1000
        response.append(interval)
        # if idx == 99:
        #     break
finally:
    print('closing socket')
    s.close()


response_data = pd.DataFrame(response, columns=['Time'])
response_data.to_csv('{}_response_data_{}.csv'.format(ip, teston))
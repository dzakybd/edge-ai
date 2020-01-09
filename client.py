# Client
import datetime
import numpy as np
import socket
import json
import pickle
import pandas as pd
from sklearn.metrics import classification_report

m_subsets = 3
x_test = pd.read_pickle('shared/x_test.pkl')
with open('shared/feature_subsets.pkl', 'rb') as pickle_file:
    feature_subsets = pickle.load(pickle_file)
with open('shared/k_best_index.pkl', 'rb') as pickle_file:
    k_best_index = pickle.load(pickle_file)


# Connection setting
host = '192.168.10.3'  # client ip
port = 4005
server = ('192.168.10.3', 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))

# Test on each edge
subset_i = 0
x_test_subset = x_test.loc[:, feature_subsets[subset_i]]

# Test on Cloud-k
x_test_subset = x_test.loc[:, k_best_index]

# Test on Cloud-all
x_test_subset = x_test

start = datetime.datetime.now()
for x in x_test_subset.values:
    x = x.tolist()
    message = json.dumps({"msg": x})
    s.sendto(message.encode(), server)
    data, addr = s.recvfrom(1024)
    data = json.loads(data.decode())
    y_test_pred = data.get("msg")
    print("Received from server: ", y_test_pred)
s.close()
end = datetime.datetime.now()
interval = end - start
print(interval)

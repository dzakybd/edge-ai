# Client
import datetime
import socket
import json
import pandas as pd
from tqdm import tqdm

#  reading the data
data_ori = pd.read_csv('uci-secom.csv')
data_ori = data_ori.drop(['Time'], axis = 1)
data_ori.loc[data_ori['Fault'] == 1, 'Fault'] = 1
data_ori.loc[data_ori['Fault'] == -1, 'Fault'] = 0
data_ori = data_ori.iloc[:, :-1]

# getting the shape of the data
print(data_ori.shape)
ip = '192.168.10.3'
server = (ip, 4000)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(server)

latency = {}
for (columnName, columnData) in tqdm(data_ori.iteritems()):
    start = datetime.datetime.now()
    for x in columnData.values:
        message = json.dumps({"msg": x})
        s.sendto(message.encode(), server)
        data, addr = s.recvfrom(1024)
        data = json.loads(data.decode())
        data.get("msg")
        # print("Received from server: ", data.get("msg"))
    end = datetime.datetime.now()
    interval = (end - start).microseconds / 1000
    latency[str(columnName)] = interval
    # print(columnName, interval)
s.close()

latency_data = pd.DataFrame.from_dict(latency, orient='index', columns=['Latency'])
latency_data.to_csv(ip+'latency_data.csv')
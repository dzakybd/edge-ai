import numpy as np
import matplotlib.pyplot as plt
import tensorflow
from keras.models import Sequential
from keras.layers import Dense, LSTM
from keras.utils import to_categorical
from keras.utils import np_utils

# Sequence to LSTM dataset format
def seq2dataset(seq, window_size):
    dataset = []
    for i in range(len(seq)-window_size):
        subset = seq[i:(i+window_size+1)]
        dataset.append([item for item in subset])
    return np.array(dataset)

# Hyperparameters
np.random.seed(1)
nb_epoch = 100
window_size = 4
batch_size = 20

# Load Fibonaci numbers modular 100 dataset
seq = np.genfromtxt("uci-secom.csv")
dataset = seq2dataset(seq, window_size)
print(dataset.shape)

# Split sequence data (x) and the next output (y)
x_train = dataset[:,0:window_size]
y_train = dataset[:,window_size]

# Add 1 dimension at last, as the feature only 1
x_train = np.expand_dims(x_train, axis=-1)
# Change output to one hot encoded format
y_train = to_categorical(y_train)
one_hot_vec_size = y_train.shape[1]
print("one hot encoding vector size is ", one_hot_vec_size)

print(x_train.shape, y_train.shape)

# Build model
model = Sequential()
model.add(LSTM(128, input_shape = (window_size, 1)))
model.add(Dense(one_hot_vec_size, activation='softmax'))

# Get model summary
model.summary()

# Train the model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['acc'])
hist = model.fit(x_train, y_train, epochs=nb_epoch, batch_size=batch_size, verbose=1)

# Save loss graph
xc = range(nb_epoch)
a = hist.history['loss']
plt.figure()
plt.plot(xc, a)
plt.xlabel('epoch')
plt.ylabel('loss')
plt.title('Loss graph on batch: ' + str(batch_size))
plt.grid(True)
plt.legend(['train'])
plt.savefig('lab09_lstm_loss_graph.png')

# Save accuracy graph
xc = range(nb_epoch)
a = hist.history['acc']
plt.figure()
plt.plot(xc, a)
plt.xlabel('epoch')
plt.ylabel('acc')
plt.title('Accuracy graph on batch: ' + str(batch_size))
plt.grid(True)
plt.legend(['train'])
plt.savefig('lab09_lstm_acc_graph.png')

# Predict example sequence
example_seq = [0, 1, 1, 2]
example_seq = np.reshape(example_seq, (1, window_size, 1))
predicted = model.predict_classes(example_seq)
print("Predicted : ", predicted)
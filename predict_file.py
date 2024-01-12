import numpy as np

f = open(r"parameters.txt")
line = f.readline()
data_list = []
while line :
    num = list(map(float, line.split()))
    data_list.append(num)
    line = f.readline()
f.close()
theta = np.array(data_list)

def sigmoid(z) :
    return 1 / (1 + np.exp(-z))

def serialize(a, b) :
    return np.concatenate((np.ravel(a), np.ravel(b)))

def deserialize(seq) :
    return seq[:3 * 4].reshape(3, 4), seq[3 * 4 :].reshape(2, 4)

def feed_forward(theta, X) :
    t1, t2 = deserialize(theta)
    m = X.shape[0]
    a1 = X

    z2 = a1 @ t1.T
    a2 = sigmoid(z2)
    a2 = np.insert(a2, 0, values = np.ones(m), axis = 1)

    z3 = a2 @ t2.T
    h = sigmoid(z3)

    return a1, z2, a2, z3, h
    
def predict(theta, X) :
    _, _, _, _, h = feed_forward(theta, X)
    y_pred = np.argmax(h, axis = 1)
    
    return y_pred
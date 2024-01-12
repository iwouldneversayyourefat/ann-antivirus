import numpy as np
import pandas as pd

import scipy.optimize as opt
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from sklearn.metrics import classification_report


path = 'test.txt'
data = pd.read_csv(path, header = None, names = ['Exam 1', 'Exam 2', 'Exam 3', 'Admitted'])

'''
data.head()
(data.describe())

x, y, z = data['Exam 1'], data['Exam 2'], data['Exam 3']
ax = plt.subplot(111, projection='3d')

ax.scatter(x[:115], y[:115], z[:115], c='r')
ax.scatter(x[115:], y[115:], z[115:], c='g')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
#plt.show()
#print(data)
'''

data.insert(0, 'Ones', 1)     #插入一列1  常数项的x
#print(data)
cols = data.shape[1]

def get_X(df) :
    X = data.iloc[:,0:cols-1]
    return np.array(X.values)

def get_y(df) :
    y = data.iloc[:,cols-1:cols]
    return np.array(y.values)

X_raw = get_X(data)#获取x

y_raw = get_y(data)#获取y
#print(X_raw,y_raw)

def expand_y(y):
    res = []
    for i in y :
        y_array = np.zeros(2)
        y_array[i] = 1
        res.append(y_array)
        
    return np.array(res)

y = expand_y(y_raw)  #y转换成向量
#print(y)

def sigmoid(z) :
    return 1 / (1 + np.exp(-z))

'''
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(np.arange(-10, 10, step=0.01),
        sigmoid(np.arange(-10, 10, step=0.01)))
ax.set_ylim((-0.1,1.1))
ax.set_xlabel('z', fontsize=18)
ax.set_ylabel('g(z)', fontsize=18)
ax.set_title('sigmoid function', fontsize=18)
#plt.show()
'''

def serialize(a, b) :
    return np.concatenate((np.ravel(a), np.ravel(b))) #concatenate连接数组 ravel展开成n x 1的数组

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

def cost(theta, X, y) :
    m = X.shape[0] 
    _, _, _, _, h = feed_forward(theta, X)
    pair_computation = -np.multiply(y, np.log(h)) - np.multiply((1 - y), np.log(1 - h))

    return pair_computation.sum() / m

def regularized_cost(theta, X, y, l = 1) :
    t1, t2 = deserialize(theta)
    m = X.shape[0]

    reg_t1 = (1 / (2 * m)) * np.power(t1[:, 1:], 2).sum()
    reg_t2 = (1 / (2 * m)) * np.power(t2[:, 1:], 2).sum()

    return cost(theta, X, y) + reg_t1 + reg_t2

def sigmoid_gradient(z) :
    return np.multiply(sigmoid(z), 1 - sigmoid(z))

def gradient(theta, X, y) :
    t1, t2 = deserialize(theta)
    m = X.shape[0]
    
    delta1 = np.zeros(t1.shape)
    delta2 = np.zeros(t2.shape)

    a1, z2, a2, z3, h = feed_forward(theta, X)

    for i in range(m) :
        a1i = a1[i, :]
        z2i = z2[i, :]
        a2i = a2[i, :]

        hi = h[i, :]
        yi = y[i, :]

        d3i = hi - yi

        z2i = np.insert(z2i, 0, np.ones(1))
        d2i = np.multiply(t2.T @ d3i, sigmoid_gradient(z2i))

        delta2 += np.matrix(d3i).T @ np.matrix(a2i)
        delta1 += np.matrix(d2i[1:]).T @ np.matrix(a1i)

    delta1 = delta1 / m
    delta2 = delta2 / m
    
    return serialize(delta1, delta2)

def regularized_gradient(theta, X, y, l = 1) :
    m = X.shape[0]
    delta1, delta2 = deserialize(gradient(theta, X, y))
    t1, t2 = deserialize(theta)

    t1[:, 0] = 0
    reg_term_d1 = (1 / m) * t1
    delta1 = delta1 + reg_term_d1

    t2[:, 0] = 0
    reg_term_d2 = (1 / m) * t2
    delta2 = delta2 + reg_term_d2

    return serialize(delta1, delta2)

def random_init(size) :
    return np.random.uniform(-0.12, 0.12, size)

def nn_training(X, y) :
    init_theta = random_init(20)   # 3*4 + 2*4
    res = opt.minimize(fun = cost,x0 = init_theta,args = (X, y),method = 'TNC',jac = gradient,options = {'maxiter' : 400})
    
    return res

res = nn_training(X_raw, y)
print(res)

final_theta = res.x
np.savetxt("parameters.txt", final_theta)

def show_accuracy(theta, X, y) :
    _, _, _, _, h = feed_forward(theta, X)
    y_pred = np.argmax(h, axis = 1)
    print(h)
    print(y_pred)
    print(classification_report(y, y_pred))

show_accuracy(final_theta, X_raw, y_raw)

# 梯度检验
def gradient_checking(theta, X, y, epsilon, regularized = False) :
    def a_numeric_grad(plus, minus, regularized = False) :
        if regularized :
            return (regularized_cost(plus, X, y) - regularized_cost(minus, X, y)) / (2 * epsilon)
        else :
            return (cost(plus, X, y) - cost(minus, X, y)) / (2 * epsilon)
    
    theta_matrix = expand_array(theta)
    epsilon_matrix = np.identity(len(theta)) * epsilon

    plus_matrix = theta_matrix + epsilon_matrix
    minus_matrix = theta_matrix - epsilon_matrix

    numeric_grad = np.array([a_numeric_grad(plus_matrix[i], minus_matrix[i], regularized) for i in range(len(theta))])

    analytic_grad = regularized_gradient(theta, X, y) if regularized else gradient(theta, X, y)

    diff = np.linalg.norm(numeric_grad - analytic_grad) / np.linalg.norm(numeric_grad + analytic_grad)

    print('If your backpropagation implementation is correct,\nthe relative difference will be smaller than 10e-9 (assume epsilon=0.0001).\nRelative Difference: {}\n'.format(diff))

def expand_array(arr) :
    return np.array(np.matrix(np.ones(arr.shape[0])).T @ np.matrix(arr))

#gradient_checking(theta, X, y, epsilon= 0.0001)   #这个运行很慢，谨慎运行
import numpy as np
import sklearn
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
import pickle
import random

# y = 4*(a) + 5*(b) + c + d + np.random.random() * 10 + ab + cd + abc

train_data = [] 
val_data = []
test_data = []
x_train = []
y_train = []
x_test = []
y_test = []

n_weights = 11
actual_params = np.array([4, 5 , 6, 5, 7 ,8, 5, 4, 3, 7, 8])

for i in range(0, 20):
    inputs = [np.random.random() * np.random.choice([100]) for _ in range(n_weights)]
    # y = 4*(a) + 5*(b) + c + d + np.random.random() * 10 + ab + cd + abc
    y = np.dot(inputs, np.transpose(actual_params)) + np.random.uniform(-100, 100) 
    x_test.append(inputs)
    y_test.append(y)

    test_data.append((inputs, y))


for i in range(0 , 20):
    inputs = [np.random.random()*np.random.choice([100]) for _ in range(n_weights)]
    u = random.random()
    y = np.dot(inputs, np.transpose(actual_params)) + np.random.uniform(-100, 100)
    x_train.append(inputs)
    y_train.append(y)

    train_data.append((inputs, y))


#poly = PolynomialFeatures(degree = 2)
#x_train = poly.fit_transform(x_train)
model = LinearRegression().fit(x_train , y_train)

#x_test = poly.fit_transform(x_test)
#y_preds = model.predict(x_test)
y_preds = np.dot(model.coef_ , np.transpose(x_test))
print('test MSE, {:.10e}'.format(mean_squared_error(y_test, y_preds)))
y_preds = np.dot(model.coef_ , np.transpose(x_train))
print('train, {:.10e}'.format(mean_squared_error(y_train, y_preds)))

filehandler = open('train.pkl', 'wb')
pickle.dump(train_data, filehandler)
filehandler = open('validation.pkl', 'wb')
pickle.dump(test_data, filehandler)
filehandler = open('weights.pkl', 'wb')
pickle.dump(model.coef_, filehandler)
print(model.coef_)

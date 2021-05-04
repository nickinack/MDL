import numpy as np
import sklearn
from sklearn.metrics import mean_squared_error
import pickle

#eqn = 1+x+x^2+x^3+x^4+x^5+x^6+x^7+x^8+x^9+x^1

def open_file(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list


overfitted_weights = open_file('weights.pkl')
training_data = open_file("train.pkl")
validation_data = open_file("validation.pkl")


def func(weights, datapoints):
    # return np.array([sum([weight * x for weight, x in zip(weights, data_point)]) for data_point in training_data]).reshape(-1,1)
    return np.array([np.dot(weights, np.transpose(x_datapoint)) for x_datapoint in datapoints]).reshape(-1,1)


def get_errors(weights):
    x_train = [a for (a,_) in training_data]
    y_train = [a for _, a in training_data]

    x_val = [a for a,_ in validation_data]
    y_val = [a for _, a in validation_data]

    # print('func:')
    # print(func(actual_params, x_train))
    # print('diff')
    # print(func(actual_params, x_train) - np.array(y_train).reshape(-1,1))
    return (mean_squared_error(y_train, func(weights, x_train)) ,
            mean_squared_error(y_val, func(weights, x_val)))

#5.09105412,  6.03164266,  4.60452684,  4.29597461,  7.27389267, 10.06737126,  6.05470855,  3.47088757,  0.90297505,  7.51947767,7.14156404
## 4, 5 , 6, 5, 7 ,8, 5, 4, 3, 7, 8

print(get_errors(overfitted_weights))

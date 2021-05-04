import numpy as np
import sklearn
from sklearn.metrics import mean_squared_error
import pickle

def train_data(n_samples):
    sample_data = []
    for i in range(0 , n_samples):
        a = np.random.random()*10
        res = 1+a+a**2+a**3+a**4+a**5+a**6+a**7+a**8+a**9+a**10
        sample_data.append((a , res))
    return sample_data


training_data = train_data(1000)
validation_data = train_data(100)

fname = "train.pkl"
open_file = open(fname, "wb")
pickle.dump(training_data, open_file)

fname = "validation.pkl"
open_file = open(fname, "wb")
pickle.dump(validation_data, open_file)

open_file.close()

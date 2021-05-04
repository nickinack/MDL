import matplotlib.pyplot as plt
import numpy as np
import pickle


def open_file(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list


verbose = open_file('verbose2021-03-02 23:38:04.736191.pkl')

val_err = []
corr_train_err = []
gens = []
cnt = 0

for diction in verbose:
    minind = 0
    for i in range(len(diction['population'])):
        if diction['val_error'][minind] > diction['val_error'][i]:
            minind = i
    gens.append(cnt)
    cnt += 1

    val_err.append(diction['val_error'][minind])
    corr_train_err.append(diction['train_error'][minind])

plt.plot(gens, val_err, label='val_err')
plt.plot(gens, corr_train_err, label='train_err')
plt.legend(loc="upper left")
plt.savefig('err_iteration.png')

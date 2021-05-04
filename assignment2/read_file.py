import pickle
import matplotlib.pyplot as plt

def open_file(file_name):
    open_file = open(file_name, "rb")
    loaded_list = pickle.load(open_file)
    open_file.close()
    return loaded_list

verbose = open_file('verbose2021-03-14 20:42:10.593234.pkl')
min_train_errors = []
min_val_errors = []
generations = []

for diction in verbose:
    min_ind = 0
    for i in range(len(diction['population'])):
        if diction['val_error'][i] < diction['val_error'][min_ind]:
            min_ind = i
    
    print(diction['pop_verbose'][min_ind])
    print("tra err: {:.10e}".format(diction['train_error'][min_ind]))
    print("weights: ", diction['population'][min_ind])
    print("gen", diction['generation'])
    print()


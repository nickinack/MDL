import pickle
import numpy as np

files = [
   'verbose2021-02-28 22:08:58.765868.pkl',   'verbose2021-03-04 22:55:26.866649.pkl',   'verbose2021-03-11 10:50:13.182247.pkl',
   'verbose2021-03-01 08:19:52.093950.pkl',   'verbose2021-03-05 14:23:43.923639.pkl',   'verbose2021-03-11 10:52:07.981073.pkl',
   'verbose2021-03-01 08:21:42.816057.pkl',   'verbose2021-03-07 21:51:49.784525.pkl',   'verbose2021-03-12 11:06:23.414689.pkl',
   'verbose2021-03-02 12:53:36.779693.pkl',   'verbose2021-03-08 19:18:23.684430.pkl',   'verbose2021-03-12 11:11:07.205349.pkl',
'verbose2021-02-26 19:25:23.516915.pkl',   'verbose2021-03-02 12:57:35.012610.pkl',   'verbose2021-03-09 11:18:53.663378.pkl',   'verbose2021-03-12 11:21:58.177027.pkl',
'verbose2021-02-26 19:31:59.037816.pkl',   'verbose2021-03-02 23:38:04.736191.pkl',   'verbose2021-03-09 11:33:59.385062.pkl',   'verbose2021-03-12 11:25:47.864122.pkl',
'verbose2021-02-27 18:32:43.045343.pkl',   'verbose2021-03-04 19:28:18.586155.pkl',   'verbose2021-03-09 11:37:58.691918.pkl',   'verbose2021-03-12 23:07:18.994050.pkl',
'verbose2021-02-27 18:43:09.939504.pkl',   'verbose2021-03-04 19:29:53.521385.pkl',   'verbose2021-03-09 11:53:50.398383.pkl',   'verbose2021-03-14 20:42:10.593234.pkl',
'verbose2021-02-27 18:47:09.501368.pkl',   'verbose2021-03-04 19:32:03.221329.pkl',   'verbose2021-03-11 10:28:16.901184.pkl',
'verbose2021-02-28 21:44:36.452384.pkl',   'verbose2021-03-04 19:47:23.643194.pkl',   'verbose2021-03-11 10:50:02.413605.pkl',
]

files = ['verbose2021-02-28 22:08:58.765868.pkl']

for curr in files:
    verbose = pickle.load(open(curr, 'rb'))
    print('==================')
    print('curr:', curr)
    for diction in verbose:
        closest_ind = []
        for i in range(len(diction['population'])):
            if diction['val_error'][i] <= 8e15:
                closest_ind.append(i)
        for i in list(sorted(closest_ind, key=lambda x: abs(diction['val_error'][x] - diction['train_error'][x])))[:3]:
            print('val error: {:.10e}'.format(diction['val_error'][i]))
            print('corr trai: {:.10e}'.format(diction['train_error'][i]))
            print('corr weig: ', diction['population'][i])
            print()
        print('-----')



# print('xxxxxxxxxxxxxx fitness xxxxxxxxxxxxxxx')
# for curr in files:
#     verbose = pickle.load(open(curr, 'rb'))
#     print('==================')
#     print('curr:', curr)

#     for diction in verbose:
#         indices = list(range(len(diction['population'])))
#         for i in list(sorted(indices, key=lambda x: 1/diction['fitness'][x]))[:3]:
#             print('val error: {:.10e}'.format(diction['val_error'][i]))
#             print('corr trai: {:.10e}'.format(diction['train_error'][i]))
#             print('fitness v: {:.10e}'.format(diction['fitness'][i]))
#             print('corr weig: ', diction['population'][i])
#             print()
#         print('-----')


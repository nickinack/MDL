import json
data = [
#10 best vectors in decreasing order of your preference
# [1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [2.1,1.1,1.1,2.1,3.3,1.1,11e-7,1,1,1,1],
# [3.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [4.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [5.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [6.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [7.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [8.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [9.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1],
# [1.1,1.1,1.1,2.1,3.3,1.1,10e-7,1,1,1,1]
]


with open('TeamNumber.json','w') as outfile:
	json.dump(data,outfile)
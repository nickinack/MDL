import json

avi = open('part_3_output_avi.json',)
avi_output = json.load(avi)

ak = open('part_3_output.json',)
ak_output = json.load(ak)

avi_output = avi_output['policy']
ak_output = ak_output['policy']

# print(avi_output)
# print('XXXXXXXXXXXXXXXXXXXXXX')
# print(ak_output)

def get_ours(req):
    for entry in ak_output:
        st = entry[0]
        if st == req:
            return entry[1]

for entry in avi_output:
    # print(entry[1], get_ours(entry[0]))
    if entry[1] != get_ours(entry[0]):
        print('avi:', entry)
        print('ours:', get_ours(entry[0]))
        print('------------')

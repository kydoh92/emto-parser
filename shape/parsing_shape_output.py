import sys
import utils as ut
import json
import re

# read a file
filename = "lat_bcc.prn"
with open(filename) as f:
    lines = f.readlines()
# convert file to compact list
clist = ut.Cleaning(lines)

# extract info.
values = list()
values.append(FHNDLR(clist))
[NSR, LMAX, NFI, IVEF] = INPUT(clist)
values.append([NSR, LMAX, NFI, IVEF])
values.append(TRNSFM(clist))
site_info = SITES_INFO(clist)

# define keys and units of info.
categories = ['FHNDLR', 'INPUT', 'TRNSFM', 'SITES_INFO']

keys = list()
keys.append(['timestamp', 'FOR001', 'EMTO', 'branch', 'hash_key', 'compile_one', 'OS', 'CPU', 'compiler', 'library'])
keys.append(['NSR', 'LMAX', 'NFI', 'IVEF'])
keys.append(['slope_matrices', 'KW2'])

units =list()
units.append(['sec', None, None, None, None, None, None, None, None, None])
units.append([None, None, None, None])
units.append([None, None])

# add unit to info.
value_unit = list()
for i, j in enumerate(categories):
    if j is 'SITES_INFO':
        pass
    else:
        value_unit.append([[value,unit] for value, unit in zip(values[i],units[i])])
# add key to info.
name_value_unit = list()
for i, j in enumerate(categories):
    if j is 'SITES_INFO':
        pass
    else:
        name_value_unit.append({key:value for key, value in zip(keys[i],value_unit[i])})
name_value_unit.append(site_info)
        
# combine all
shape_dict = {key:value for key, value in zip(categories,name_value_unit)}

# save as a json file
with open(filename+'_out.json', 'w') as f:
    json.dump(shape_dict, f, indent=2)
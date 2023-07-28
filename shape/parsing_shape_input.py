#!/home/tjsrb2507/anaconda3/envs/pyemto/bin/python
import sys
import utils as ut
import json
import re
import os
from shape import DAT
    
# Read the file and parse a text
filename="lat_bcc.dat"
with open(filename) as f:
    lines = f.readlines()

# cleaning & get list type [line, line, ...]
clist = ut.Cleaning(lines)

# extract info.
DAT_values = DAT(clist)
print(DAT_values)

# define names and units of info.
DAT_keys = ['JOBNAME', 'MSGL', 'FOR001', 'NPRN', 'Lmax', 'NSR', 'NFI', 'IVEF']
DAT_units = [None, None, None, None, None, None, None, None]

# add unit ot info.
DAT_vu = [[value, unit] for value, unit in zip(DAT_values, DAT_units)]

# add name to info. and divide info. into sub-classes
Meta_dict = {key:value for key, value in zip(DAT_keys[0:4], DAT_vu[0:4])}
Approximation_dict = {key:value for key, value in zip(DAT_keys[4:], DAT_vu[4:])}

# combine all
DAT_dict = {'Meta':Meta_dict, 'Approximation':Approximation_dict}

# save as json file
with open(filename+'_in.json', 'w') as f:
    json.dump(DAT_dict, f, indent=2)

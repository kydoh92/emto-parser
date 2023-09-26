#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from kgrn import MLTPM1, MLTPM2, OPTPOT
import json

'''
# read a file
filepath = sys.argv[1]
filename = filepath.split('/')[-1]
with open(filepath,'r') as f:
    lines = f.readlines()
# convert file to compact list
clist = ut.Cleaning(lines)

with open('clean_'+filename,'w') as f:
    f.write(''.join(clist))
'''
filepath = sys.argv[1]
with open(filepath,'r') as f:
    lines = f.readlines()

clist = lines

# testing parameters
ns = 2
nq = 8

# extract info.
values = list()
values.append(MLTPM1(clist,ns,nq))
for iq in range(nq):
	MLTPM2(clist)
values.append(OPTPOT(clist,ns))
print(values)
print(clist[0])
print(ut.category_cognition(clist[0]))

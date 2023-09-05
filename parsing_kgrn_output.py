#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from kgrn import MLTPM1, MLTPM2
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

# extract info.
values = list()
values.append(MLTPM1(clist,spin=2,nq=8))
for iq in range(8):
	MLTPM2(clist)

print(clist[0])
print(ut.category_cognition(clist[0]))

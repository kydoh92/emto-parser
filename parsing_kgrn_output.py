#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from kgrn import CALL_CATEGORY
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

hp_type = 'Al'

# testing parameters
if hp_type is 'Fe':
	ns = 2
	nq = 1
	afm = 'F'
	ntnta = [['Fe','Ni']]
	zmsh = 'C'
elif hp_type is 'Al':
	ns = 2
	nq = 8
	afm = 'F'
	ntnta = [['Al'],['Co'],['Co'],['Co'],['Co'],['Co'],['Co'],['Al']]
	zmsh = 'C'

# extract info.
values = list()

while clist != []:
	a = len(clist)
	value = [CALL_CATEGORY(clist, nq, afm, ns, ntnta, zmsh)]
	if value[0] is not None:
		values.append(value[0])
	b = len(clist)
	print(values[-1][0][0],a-b)

for v in values:
	print(v)


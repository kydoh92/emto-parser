#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from kgrn import MLTPM1, MLTPM2, OPTPOT
from kgrn import KGRN1
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

# testing parameters
ns = 2
nq = 1
afm = 'F'

# extract info.
values = list()
#values.append(MLTPM1(clist,ns,nq))
#for iq in range(nq):
#	MLTPM2(clist)
#values.append(OPTPOT(clist,ns))
#values.append(KGRN1(clist,afm))

while clist != []:
	a = len(clist)
	values.append([CALL_CATEGORY(clist, nq, afm, ns)])
	b = len(clist)
	print(values[-1][0][0],a-b)
	if values[-1][0][0] == 'EBTOP':
		break # 뒷 부분 category 처리 함수가 작성 중


print(values)
#print(clist[0])
#print(ut.category_cognition(clist[0]))

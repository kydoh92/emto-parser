#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
#from bmdl import FHNDLR, PRIMV, PRIMKR, SET3D, BMDL, LATT3M, BMDL2
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



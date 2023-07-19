#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from bmdl import FHNDLR, PRIMV, PRIMKR, SET3D, BMDL, LATT3M, BMDL2
import json

# read a file
filename = sys.argv[1]
with open(filename,'r') as f:
    lines = f.readlines()
# convert file to compact list
clist = ut.Cleaning(lines)

#with open('clean_'+filename,'w') as f:
#    f.write(''.join(clines))

# extract info.
values = list()
values.append(FHNDLR(clist))
values.append(PRIMV(clist))
values.append(PRIMKR(clist))
SET3D(clist)
values.append(BMDL(clist))
values.append(LATT3M(clist))
values.append(BMDL2(clist))

# define keys and units of info.
categories = ['FHNDLR','PRIMV','PRIMKR','BMDL','LATT3M']

keys = list()
keys.append(['time','JOB','EMTO','branch','hash_key','compile_on','OS','CPU','compiler','library'])
keys.append(['A','B','C','ALPHA','BETA','GAMMA','Lattice','Basis'])
keys.append(['WS_radius','VOL','reciprocal'])
keys.append(['NPRN','NL','NQ','NLM','NLMQ','MSGL','AMAX','BMAX','ALAMDA','RMAX','GMAX'])
keys.append(['R1','RA','G1','GA','NUMR','NUMG','NUMVR','NUMVG'])
keys.append(['CMDL'])

units = list()
units.append(['sec',None,None,None,None,None,None,None,None,None])
units.append([None,None,None,None,None,None,None,None])
units.append([None,None,None])
units.append([None,None,None,None,None,None,None,None,None,None,None])
units.append([None,None,None,None,None,None,None,None])
units.append([None])

# add unit to info.
value_unit = list()
for i,_ in enumerate(categories):
	value_unit.append([ [value,unit] for value, unit in zip(values[i],units[i]) ])

# add key to info.
name_value_unit = list()
for i,_ in enumerate(categories):
	name_value_unit.append({ key:value for key, value in zip(keys[i],value_unit[i]) })

# combine all
bmdl_dict = { key:value for key, value in zip(categories,name_value_unit) }

# Save as a json file
with open(JOB+'_out.json', 'w') as f:
	json.dump(bmdl_dict, f, indent=2)



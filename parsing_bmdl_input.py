#!/usr/local/anaconda3/bin/python
import sys
#import utils as ut
from bmdl import DAT
import json
#### MAIN ####

# read a file
filename=sys.argv[1]
with open(filename,'r') as f:
	lines = f.readlines()
'''
# convert a file to a compact list
clist = ut.Cleaning(lines)
'''
# extract info.
DAT_values = DAT(lines)

# define names and units of info.
DAT_keys = ['JOBNAM','MSGL','NPRN','dir_mdl','dir_prn','NL','LAMDA','AMAX','BMAX','NQ','LAT','IPRIM','NQR2','Lattice','Basis']
DAT_units= [None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]

# add unit to info.
DAT_vu = [[value,unit] for value, unit in zip(DAT_values,DAT_units)]

# add name to info. and divide info. into sub-classes
Meta_dict          = { key:value for key, value in zip(DAT_keys[0:3],DAT_vu[0:3]) }
Approximation_dict = { key:value for key, value in zip(DAT_keys[3:7],DAT_vu[3:7]) }
Structure_dict     = { key:value for key, value in zip(DAT_keys[7: ],DAT_vu[7: ]) }

# combine all
DAT_dict = { 'Meta':Meta_dict, 'Approximation':Approximation_dict, 'Structure':Structure_dict }

# Save as a json file
with open(JOBNAM+'_in.json', 'w') as f:
	json.dump(DAT_dict, f, indent=2)


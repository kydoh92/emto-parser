#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from utils import tokenizer
import json
import re

#### MAIN ####

# Read and parse a text
filename = sys.argv[1]
with open(filename,'r') as f:
    lines = f.readlines()

# cleaning & get list type
clines = ut.Cleaning(lines)

MSGL = tokenizer(clines.pop(0), even=0)[1]

JOBNAM = tokenizer(clines.pop(0))[0]
STRNAM = tokenizer(clines.pop(0))[0]

del clines[0:5]
 
Lmaxs, NTH, NFI, FPOT = tokenizer(clines.pop(0))
OVCOR, UBG, NPRN = tokenizer(clines.pop(0))

# Combine entities
Input = {
	'Meta' : {
		'JOBNAM'  : [JOBNAM ,'str'],
        'STRNAM'  : [STRNAM ,'str']
	},
	'Approximation' : {
        'MSGL'    : [MSGL   ,'int'],
        'Lmaxs'   : [Lmaxs  ,'int'],
        'NTH'     : [NTH    ,'int'],
        'NFI'     : [NFI    ,'int'],
        'FPOT'    : [FPOT   ,'int'],
        'OVCOR'   : [OVCOR  ,'int'],
        'UBG'     : [UBG    ,'int'],
        'NPRN'    : [NPRN   ,'int']
    }
}

#print(Input)
# Save as a json file
output_path = './output_file/'
with open(output_path+JOBNAM+'_kfcd'+'_in.json', 'w') as f:
    json.dump(Input, f, indent=2)
#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from utils import tokenizer
import json
import re

def get_lattice(clines, IPRIM, A, B, C):
    if IPRIM == 1:
        ALPHA, BETA, GAMMA = ut.e3f(clines.pop(0))
        # convert unit degree to radian
        alpha,beta,gamma = map(ut.DtoR, [ALPHA,BETA,GAMMA])
        # convert angles to lattice vectors
        Lattice =  ut.AtoV(A, B, C, alpha, beta, gamma)
    elif IPRIM == 0:
        Lattice = list(map(lambda x: list(ut.e3f(clines.pop(0))),range(3)))
        # convert lattice vectors to angles
        alpha, beta, gamma = ut.VtoA(Lattice)
        # convert unit radian to degree
        ALPHA, BETA, GAMMA = map(ut.RtoD, [alpha,beta,gamma])
        return Lattice , ALPHA, BETA, GAMMA 

def get_basis(clines, NQ):
	Basis = list(map(lambda x: list(ut.e3f(clines.pop(0))),range(NQ)))
	return Basis

def get_aw(clines, NQ):
	AW = list(map(lambda x: list(tokenizer(clines.pop(0), even=0)),range(NQ)))
	return AW

#### MAIN ####

# Read and parse a text
filename = sys.argv[1]
with open(filename,'r') as f:
    lines = f.readlines()

# cleaning & get list type
clines = ut.Cleaning(lines)

i = 1
while clines:
    if i in [1,3,4,5]:
        clines.pop(0)
        pass
    elif i == 2:
        JOBNAM, MSGL, MODE, STORE, HIGH = tokenizer(clines.pop(0))
        MSGL = int(MSGL)
    elif i == 6:
        NL, NLH, NLW, NDER, ITRANS, NPRN = list(map(int, tokenizer(clines.pop(0))))
    elif i == 7:
        KAPPA, DMAX, RWATS = list(map(float, tokenizer(clines.pop(0))))
    elif i == 8:
        NQ, LAT, IPRIM, NGHBP, NQR2 = list(map(int, tokenizer(clines.pop(0))))
    elif i == 9:
        A, B, C = ut.e3f(clines.pop(0))
        Lattice, ALPHA, BETA, GAMMA = get_lattice(clines, IPRIM, A, B, C)
    elif i == 10:
        Basis = get_basis(clines, NQ)
    elif i == 11:
        AW = get_aw(clines, NQ)
    elif i == 12:
        LAMDA, AMAX, BMAX = list(map(float, tokenizer(clines.pop(0))))
    else:
        print("clines exist")
        clines.pop(0)

    i += 1

# Combine entities
Input = {
	'Meta' : {
		'JOBNAM'  : [JOBNAM ,'str'],
		'MSGL'    : [MSGL   ,'int_bool'],
        'MODE'    : [MODE   ,'str'],
        'STORE'   : [STORE  ,'str_bool'],
		'HIGH'    : [HIGH   ,'str_bool']
	},
	'Approximation' : {
        'NL'      : [NL     ,'int'],
        'NLH'     : [NLH    ,'int'],
        'NLW'     : [NLW    ,'int'],
        'NDER'    : [NDER   ,'int'],
        'ITRANS'  : [ITRANS ,'int'],
        'NPRN'    : [NPRN   ,'int'],
        'KAPPA'   : [KAPPA  ,'float'],
        'DMAX'    : [DMAX   ,'float'],
        'RWATS'   : [RWATS  ,'float'],
        'AW'      : [AW     ,'float_list'],
        'LAMDA'   : [LAMDA  ,'float'],
        'AMAX'    : [AMAX   ,'float'],
        'BMAX'    : [BMAX   ,'float']

	},
	'Structure' : {
		'NQ'      : [NQ     ,'int'],
		'LAT'     : [LAT    ,'int'],
		'IPRIM'   : [IPRIM  ,'int'],
		'NQR2'    : [NQR2   ,'int'],
		'A'       : [A      ,'float'],
		'B'       : [B      ,'float'],
		'C'       : [C      ,'float'],
		'ALPHA'   : [ALPHA  ,'float'],
		'BETA'    : [BETA   ,'float'],
		'GAMMA'   : [GAMMA  ,'float'],
		'Lattice' : [Lattice,'float_list'],
		'Basis'   : [Basis  ,'float_list']
	}
}
#print(Input)
# Save as a json file
output_path = './output_file/'
with open(output_path+JOBNAM+'_kstr'+'_in.json', 'w') as f:
    json.dump(Input, f, indent=2)
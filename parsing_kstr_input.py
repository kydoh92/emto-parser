#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
from utils import flush
import json
import re

def tokenizer(f, even=1):
    string = f.readline().replace('=',' ').replace('\n','')
    rr = re.sub(' +', ' ', string).split(' ')
    if even == 1:
        return rr[1::2]
    if even == 0:
        return rr[1:]

def L7(f):
	string = f.readline()
	NQ =    int(string[ 7:10])
	LAT =   int(string[18:20])
	IPRIM = int(string[28:30])
	NQR2 =  int(string[38:40])
	return NQ, LAT, IPRIM, NQR2

def L9(f, IPRIM, A, B, C):
    if IPRIM == 1:
        ALPHA, BETA, GAMMA = ut.e3f(f)
        # convert unit degree to radian
        alpha,beta,gamma = map(ut.DtoR, [ALPHA,BETA,GAMMA])
        # convert angles to lattice vectors
        Lattice =  ut.AtoV(A, B, C, alpha, beta, gamma)
    elif IPRIM == 0:
        Lattice = list(map(lambda x: list(ut.e3f(f)),range(3)))
        # convert lattice vectors to angles
        alpha, beta, gamma = ut.VtoA(Lattice)
        # convert unit radian to degree
        ALPHA, BETA, GAMMA = map(ut.RtoD, [alpha,beta,gamma])
        return Lattice , ALPHA, BETA, GAMMA 

def L10(f, NQ):
	Basis = list(map(lambda x: list(ut.e3f(f)),range(NQ)))
	return Basis

def L14(f, NQ):
	AW = list(map(lambda x: list(tokenizer(f, even=0)),range(NQ)))
	return AW

#### MAIN ####

# Read and parse a text
filename=sys.argv[1]
f = open(filename,'r')

flush(f,1)
l2 = tokenizer(f)
JOBNAM, MSGL, MODE, STORE, HIGH = l2
MSGL = int(MSGL)

flush(f,3)

l6  = tokenizer(f)
NL, NLH, NLW, NDER, ITRANS, NPRN = list(map(int, l6))
l7  = tokenizer(f)
KAPPA, DMAX, RWATS = list(map(float, l7))

l8  = tokenizer(f)
NQ, LAT, IPRIM, NGHBP, NQR2 = list(map(int, l8))

A, B, C = ut.e3f(f)
Lattice, ALPHA, BETA, GAMMA = L9(f, IPRIM, A, B, C)
Basis = L10(f,NQ)

AW = L14(f, NQ)

l15 = tokenizer(f)
LAMDA, AMAX, BMAX = list(map(float, l15))

f.close()

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
with open(JOBNAM+'_kstr'+'_in.json', 'w') as f:
    json.dump(Input, f, indent=2)
#!/home/tjsrb2507/anaconda3/envs/pyemto/bin/python
import sys
import utils as ut
from utils import flush
import json

def L2(f):
	string = f.readline()
	JOBNAM = string[10:20].strip()
	MSGL =  int(string[27:30])
	NPRN =  int(string[37:40])
	return JOBNAM, MSGL, NPRN

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
		Lattice = list(map(lambda x: ut.e3f(f),range(3)))
		# convert lattice vectors to angles
		alpha, beta, gamma = ut.VtoA(Lattice)
		# convert unit radian to degree
		ALPHA,BETA,GAMMA = map(ut.RtoD, [alpha,beta,gamma])
	return Lattice, ALPHA, BETA, GAMMA 

def L10(f, NQ):
	Basis = list(map(lambda x: list(ut.e3f(f)),range(NQ)))
	return Basis

#### MAIN ####

# Read and parse a text
filename=sys.argv[1]
f = open(filename,'r')

flush(f)
JOBNAM, MSGL, NPRN = L2(f)
#print(JOBNAM, MSGL, NPRN)
flush(f,3)
NL = ut.e1i(f) 
#print(NL)
LAMDA, AMAX, BMAX = ut.e3f(f)
#print(LAMDA, AMAX, BMAX)
NQ, LAT, IPRIM, NQR2 = L7(f)
#print(NQ, LAT, IPRIM, NQR2)
A, B, C = ut.e3f(f)
#print(A, B, C)
Lattice, ALPHA, BETA, GAMMA = L9(f,IPRIM, A, B, C)
#print(Lattice, ALPHA, BETA, GAMMA)
Basis = L10(f,NQ)
#print(Basis)

f.close()

# Combine entities
Input = {
	'Meta' : {
		'JOBNAM'  : [JOBNAM ,None],
		'MSGL'    : [MSGL   ,None],
		'NPRN'    : [NPRN   ,None]
	},
	'Approximation' : {
		'NL'      : [NL     ,None],
		'LAMDA'   : [LAMDA  ,None],
		'AMAX'    : [AMAX   ,None],
		'BMAX'    : [BMAX   ,None]
	},
	'Structure' : {
		'NQ'      : [NQ     ,None],
		'LAT'     : [LAT    ,None],
		'IPRIM'   : [IPRIM  ,None],
		'NQR2'    : [NQR2   ,None],
		'A'       : [A      ,None],
		'B'       : [B      ,None],
		'C'       : [C      ,None],
		'ALPHA'   : [ALPHA  ,None],
		'BETA'    : [BETA   ,None],
		'GAMMA'   : [GAMMA  ,None],
		'Lattice' : [Lattice,None],
		'Basis'   : [Basis  ,None]
	}
}
#print(Input)
# Save as a json file
with open(JOBNAM+'_in.json', 'w') as f:
	json.dump(Input, f, indent=2)



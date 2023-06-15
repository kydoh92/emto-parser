#!/usr/local/anaconda3/bin/python
import sys
import numpy as np
import utils as ut
from utils import flush
import json

def FHNDLR1(f):
	# read time
	timestamp = ut.head_timestamp(f)
	# flush 1 line
	flush(f)
	return timestamp

def FHNDLR2(f):
	# read JOB
	JOB = ut.css(f)
	# flush 3 lines
	flush(f,3)
	return JOB

def FHNDLR3(f):
	# read information
	EMTO        = ut.css(f)
	branch      = ut.css(f)
	hash_key    = ut.css(f)
	compile_on  = ut.css(f)
	OS          = ut.css(f)
	CPU         = ut.css(f)
	compiler    = ut.css(f)
	library     = ut.css(f)
	# flush a line
	flush(f)
	return EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library

def PRIMV(f):
	# flush 2 lines
	flush(f,2)
	# read lengthes and angles
	A,B,C = ut.e3f(f)
	ALPHA,BETA,GAMMA = ut.e3f(f)
	# flush 4 lines
	flush(f,4)
	# read lattice vectors
	Lattice = list(map(lambda x: ut.v3(f),range(3)))
	# flush a line
	flush(f)
	# read NQ3
	temp = f.readline().split('=')
	NQ3 = int(temp[1])
	# flush a line
	flush(f)
	# read Basis for NQ3 times
	Basis = list(map(lambda x: ut.v3(f),range(NQ3)))
	# flush 2 lines
	flush(f,2)
	return A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis

def PRIMKR(f):
	# read WS_radius and VOL
	temp = f.readline().split(':')[2].split('=')
	WS_radius, VOL = map(lambda x : float(x[:10]),temp)
	# flush 5 lines
	flush(f,5)
	# read reciprocal lattice
	reciprocal = list(map(lambda x: ut.v3(f),range(3)))
	# flush a line
	flush(f)
	return WS_radius, VOL, reciprocal

def BMDL(f):
	NPRN = ut.e1i(f)
	NL,NQ,NLM,NLMQ = ut.e4i(f)
	MSGL = ut.e1i(f)
	flush(f)
	AMAX,BMAX,ALAMDA = ut.e3f(f)
	RMAX,GMAX = ut.e2f(f)
	flush(f)
	return NPRN,NL,NQ,NLM,NLMQ,MSGL,AMAX,BMAX,ALAMDA,RMAX,GMAX

def LATT3D(f):
	R1, RA, G1 = ut.e3f(f)
	GA = ut.e1f(f)
	flush(f)
	NUMR, NUMG, NUMVR, NUMVG = ut.e4i(f)
	flush(f)
	return R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG

#### MAIN ####

# Read and parse a text
filename=sys.argv[1]
f = open(filename,'r')

#FHNDLR
time_start = FHNDLR1(f) # There isn't a timestamp for the end
JOB = FHNDLR2(f)
EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library = FHNDLR3(f)
print(time_start,JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library) # time_start and 9 entities

#PRIMV
A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis = PRIMV(f)
print(A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis) # 8 entities

#PRIMKR
WS_radius, VOL, reciprocal = PRIMKR(f)
print(WS_radius, VOL, reciprocal) # 3 entities

#SET3D
flush(f,2)

#BMDL
NPRN, NL, NQ, NLM, NLMQ, MSGL, AMAX, BMAX, ALAMDA, RMAX, GMAX = BMDL(f)
print(NPRN, NL, NQ, NLM, NLMQ, MSGL, AMAX, BMAX, ALAMDA, RMAX, GMAX) # 11 entities

#LATT3M
R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG = LATT3D(f)
print(R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG) # 8 entities

#END
CMDL = ut.e1f(f)
print("CMDL: {}",CMDL) # 1 entity

f.close()


# Combine entities
Entities = {
	'FHNDLR' : {
		'JOB'     : [JOB     ,None],
		'EMTO'    : [EMTO    ,None],
		'branch'  : [branch  ,None],
		'hash_key': [hash_key,None],
		'compile_': [compile_on,None],
		'OS'      : [OS      ,None],
		'CPU'     : [CPU     ,None],
		'compiler': [compiler,None],
		'library' : [library ,None]
	},
	'PRIMV'  : {
		'A'       : [A      ,None],
		'B'       : [B      ,None],
		'C'       : [C      ,None],
		'ALPHA'   : [ALPHA  ,None],
		'BETA'    : [BETA   ,None],
		'GAMMA'   : [GAMMA  ,None],
		'Lattice' : [Lattice,None],
		'Basis'   : [Basis  ,None]
	},
	'PRIMKR' : {
		'WS_r'    : [WS_radius,None],
		'VOL'     : [VOL     ,None],
		'reciproc': [reciprocal,None]
	},
	'BMDL'   : {
		'NPRN'    : [NPRN   ,None],
		'NL'      : [NL     ,None],
		'NQ'      : [NQ     ,None],
		'NLM'     : [NLM    ,None],
		'NLMQ'    : [NLMQ   ,None],
		'MSGL'    : [MSGL   ,None],
		'AMAX'    : [AMAX   ,None],
		'BMAX'    : [BMAX   ,None],
		'ALAMDA'  : [ALAMDA ,None],
		'RMAX'    : [RMAX   ,None],
		'GMAX'    : [GMAX   ,None]
	},
	'LATT3M' : {
		'R1'      : [R1     ,None],
		'RA'      : [RA     ,None],
		'G1'      : [G1     ,None],
		'GA'      : [GA     ,None],
		'NUMR'    : [NUMR   ,None],
		'NUMG'    : [NUMG   ,None],
		'NUMVR'   : [NUMVR  ,None],
		'NUMVG'   : [NUMVG  ,None]
	},
	'END'    : {
		'CMDL'    : [CMDL   ,None]
	}
}
#print(Entities)
# Save as a json file
with open(JOB+'_out.json', 'w') as f:
	json.dump(Entities, f, indent=2)



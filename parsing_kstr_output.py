#!/usr/local/anaconda3/bin/python
import sys
import numpy as np
import utils as ut
from utils import flush
import json
import re

def check_keywd(f, keywd):
	string = f.read(11).strip()
	key = string.split(':')[0]
	if key != keywd:
		print(" ### Error : keyword mismatch; keyword = "+keywd+", input = "+key+"\n"); sys.exit()
	return string

def FHNDLR1(f):
	check_keywd(f, 'FHNDLR')
	# read time
	timestamp = ut.head_timestamp(f)
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
	return EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library

def INPUT(f):
	check_keywd(f, 'INPUT')
	MODE , STORE , NPRN = tokenizer(f)
	NL, NLH, NLW, NDER  = tokenizer(f)
	DMAX , DWATS        = tokenizer(f)
	KAPPA, ITRANS       = tokenizer(f)
	return MODE, STORE, NPRN, NL, NLH, NLW, NDER, DMAX, DWATS, KAPPA, ITRANS

def PRIMV(f):
	check_keywd(f, 'PRIMV')
	flush(f,1)
	# read lengthes and angles
	A,B,C = ut.e3f(f)
	ALPHA,BETA,GAMMA = ut.e3f(f)
	flush(f,2)
	# read lattice vectors
	Lattice = list(map(lambda x: ut.v3(f),range(3)))
	# read NQ3
	temp = f.readline().split('=')
	NQ3 = int(temp[1])
	# read Basis for NQ3 times
	Basis = list(map(lambda x: ut.v3(f),range(NQ3)))
	return A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis, NQ3

def PRIMKR(f):
	check_keywd(f, 'PRIMKR')
	# read WS_radius and VOL
	temp = f.readline().split(':')[1].split('=')
	WS_radius, VOL = map(lambda x : float(x[:10]),temp)
	flush(f,2)
	# read reciprocal lattice
	reciprocal = list(map(lambda x: ut.v3(f),range(3)))
	return WS_radius, VOL, reciprocal

def LATT3D(f):
	R1, RA, G1 = ut.e3f(f)
	GA = ut.e1f(f)
	flush(f)
	NUMR, NUMG, NUMVR, NUMVG = ut.e4i(f)
	flush(f)
	return R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG

#### MAIN ####

input_path = './input_file/'
filename = '2_sample_out.dat'

# Read and parse a text
f = open('temp_'+filename,'r')

#FHNDLR
time_start = FHNDLR1(f) # There isn't a timestamp for the end
JOB = FHNDLR2(f)
EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library = FHNDLR3(f)

#INPUT
MODE, STORE, NPRN, NL, NLH, NLW, NDER, DMAX, DWATS, KAPPA, ITRANS = INPUT(f)

#PRIMV
A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis,NQ = PRIMV(f)

#PRIMKR
WS_radius, VOL, reciprocal = PRIMKR(f)

#SET3D
flush(f,1)

#LATT3D
flush(f,NQ+1)

#BLATTS
flush(f,(NQ+1)*2)

#SCREEN
flush(f,NQ+2)

#MGAUNT
flush(f,1)

#LATT3M
flush(f,4)

#MADL3D
flush(f,NQ+4)

#STORES
flush(f,NQ*2)

#END
flush(f,1)

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



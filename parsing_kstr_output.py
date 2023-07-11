#!/usr/local/anaconda3/bin/python
import sys
import numpy as np
import utils as ut
from utils import tokenizer
import json
import re

def check_keywd(string, keywd):
	key = string[0:11].strip().split(':')[0]
	if key != keywd:
		print(" ### Error : keyword mismatch; keyword = "+keywd+", input = "+key+"\n"); sys.exit()
	return string[11:]

def FHNDLR1(clines):
	str0 = check_keywd(clines.pop(0), 'FHNDLR')
	# read time
	timestamp = ut.lat_headtime(str0, clines.pop(0))
	return timestamp

def FHNDLR2(clines):
	# read information
	JOB         = ut.css(clines.pop(0))
	del clines[0:3]
	EMTO        = ut.css(clines.pop(0))
	branch      = ut.css(clines.pop(0))
	hash_key    = ut.css(clines.pop(0))
	compile_on  = ut.css(clines.pop(0))
	OS          = ut.css(clines.pop(0))
	CPU         = ut.css(clines.pop(0))
	compiler    = ut.css(clines.pop(0))
	library     = ut.css(clines.pop(0))
	return JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library

def INPUT(clines):
	str0 = check_keywd(clines.pop(0), 'INPUT')
	MODE , STORE , NPRN = tokenizer(str0)
	NL, NLH, NLW, NDER  = tokenizer(clines.pop(0))
	DMAX , DWATS        = tokenizer(clines.pop(0))
	KAPPA, ITRANS       = tokenizer(clines.pop(0))
	return MODE, STORE, NPRN, NL, NLH, NLW, NDER, DMAX, DWATS, KAPPA, ITRANS

def PRIMV(clines):
	check_keywd(clines.pop(0), 'PRIMV')
	# read lengthes and angles
	A,B,C = ut.e3f(clines.pop(0))
	ALPHA,BETA,GAMMA = ut.e3f(clines.pop(0))
	del clines[0:2]
	# read lattice vectors
	Lattice = list(map(lambda x: ut.v3(clines.pop(0)),range(3)))
	# read NQ3
	tmp = clines.pop(0).split('=')
	NQ3 = int(tmp[1])
	# read Basis for NQ3 times
	Basis = list(map(lambda x: ut.v3(clines.pop(0)),range(NQ3)))
	return A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis, NQ3

def PRIMKR(clines):
	str0 = check_keywd(clines.pop(0), 'PRIMKR')
	# read WS_radius and VOL
	temp = str0.split(':')[1].split('=')
	WS_radius, VOL = map(lambda x : float(x[:10]),temp)
	del clines[0:2]
	# read reciprocal lattice
	reciprocal = list(map(lambda x: ut.v3(clines.pop(0)),range(3)))
	return WS_radius, VOL, reciprocal

def LATT3D(clines, NQ):
	str0 = check_keywd(clines.pop(0), 'LATT3D')
	NGHBP = ut.e1f(str0)
	vectors = list(map(lambda x: tokenizer(clines.pop(0), even=0, spl='.')[3::4],range(NQ)))
	return NGHBP, vectors

def BLATTS(clines, NQ):
	arr = np.empty((NQ, 8))
	for i in range(NQ):
		str0 = check_keywd(clines.pop(0), 'BLATTS')
		arr[i,:4] = tokenizer(str0)[1:]
		arr[i,4:] = tokenizer(clines.pop(0))

	tmp = clines[0][0:11].strip().split(':')
	key = tmp[0]
	star = tmp[1].strip()
	if (key == 'BLATTS') and (star == '**'):
		del clines[0:2]

	return list(map(lambda x: arr[:,x].tolist() ,range(8)))

def SCREEN(clines, NQ, NL):
	check_keywd(clines.pop(0), 'SCREEN')
	del clines[0:1]
	AWR = list(map(lambda x: tokenizer(clines.pop(0), even=0)[1:],range(NQ)))
	return AWR

def MGAUNT(clines):
	str0 = check_keywd(clines.pop(0), 'MGAUNT')
	NGAUNT, NGAUNTW = tokenizer(str0)
	return NGAUNT, NGAUNTW

def LATT3M(clines):
	str0 = check_keywd(clines.pop(0), 'LATT3M')
	R1, RA, G1 = tokenizer(str0)
	GA = tokenizer(clines.pop(0))[0]
	NUMR, NUMG, NUMVR, NUMVG = tokenizer(clines.pop(0))
	return R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG

def MADL3D(clines, NQ):
	check_keywd(clines.pop(0), 'MADL3D')
	CMDL = tokenizer(clines.pop(0))[0]
	del clines[0:1]
	POT = list(map(lambda x: tokenizer(clines.pop(0), even=0),range(NQ)))
	return CMDL, POT

def STORESH(clines, NQ):
	for i in range(NQ):
		check_keywd(clines.pop(0), 'STORES')
		check_keywd(clines.pop(0), 'STOREH')
	return 0

def END(clines):
	if len(clines) > 1:
		print(" ### Error : Too many lines left \n"); sys.exit()
	check_keywd(clines.pop(0), 'KSTR')
	return 0
#### MAIN ####

filename = sys.argv[1]
with open(filename,'r') as f:
    lines = f.readlines()

# cleaning & get list type
clines = ut.Cleaning(lines)

#FHNDLR
time_start = FHNDLR1(clines)
JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library = FHNDLR2(clines)

#INPUT
MODE, STORE, NPRN, NL, NLH, NLW, NDER, DMAX, DWATS, KAPPA, ITRANS = INPUT(clines)

#PRIMV
A, B, C, ALPHA, BETA, GAMMA, Lattice, Basis, NQ = PRIMV(clines)

#PRIMKR
WS_radius, VOL, reciprocal = PRIMKR(clines)

#SET3D
del clines[0]

#LATT3D
NGHBP, vectors = LATT3D(clines, NQ)

#BLATTS
NSC, NVN, Vt, Va, Si, Sc, WST, WSTWSR = BLATTS(clines, NQ)

#SCREEN
AWR = SCREEN(clines, NQ, NL)

#MGAUNT
NGAUNT, NGAUNTW = MGAUNT(clines)

#LATT3M
R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG = LATT3M(clines)

#MADL3D
CMDL, POT = MADL3D(clines, NQ)

#STORE
STORESH(clines, NQ)

#END
END(clines)

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
	'KSTR' : {
		'MODE'    : [MODE     ,None],
		'STORE'   : [STORE    ,None],
		'NPRN'    : [NPRN     ,None],
		'NQ'      : [NQ       ,None],
		'NL'      : [NL       ,None],
		'NLH'     : [NLH      ,None],
		'NLW'     : [NLW      ,None],
		'NDER'    : [NDER     ,None],
		'DMAX'    : [DMAX     ,None],
		'KAPPA'   : [KAPPA    ,None],
		'ITRANS'  : [ITRANS   ,None]
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
		'VOL'     : [VOL    ,None],
		'reciproc': [reciprocal,None]
	},
	'LATT3D' : {
		'NGHBP'   : [NGHBP  ,None],
		'vectors' : [vectors,None]
	},
	'BLATTS' : {
		'NSC'     : [NSC    ,None],
		'NVN'     : [NVN    ,None],
		'Vt'      : [Vt     ,None],
		'Va'      : [Va     ,None],
		'Si'      : [Si     ,None],
		'Sc'      : [Sc     ,None],
		'WST'     : [WST    ,None],
		'WSTWSR'  : [WSTWSR ,None]
	},
	'SCREEN' : {
		'AWR'     : [AWR    ,None],
	},
	'MGAUNT' : {
		'NGAUNT'  : [NGAUNT ,None],
		'NGAUNTW' : [NGAUNTW,None]
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
	'MADL3D' : {
		'CMDL'    : [CMDL   ,None],
		'POT'     : [POT    ,None]
	}
}

# Save as a json file
with open('./output_file/'+JOB+'_out.json', 'w') as f:
	json.dump(Entities, f, indent=2)
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
time, JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library = FHNDLR(clist)
A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis = PRIMV(clist)
WS_radius, VOL, reciprocal = PRIMKR(clist)
SET3D(clist)
NPRN, NL, NQ, NLM, NLMQ, MSGL, AMAX, BMAX, ALAMDA, RMAX, GMAX = BMDL(clist)
R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG = LATT3M(clist)
CMDL = BMDL2(clist)

# Combine entities
Entities = {
	'FHNDLR' : {
		'time'    : [time    ,'sec'],
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



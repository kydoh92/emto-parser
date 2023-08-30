#!/usr/local/anaconda3/bin/python
import utils as ut
from utils import tokenizer, check_category, check_dat


def DAT(clist):
	# check file
	check_dat(clist.pop(0),'BMDL')
	# read info.
	JOBNAM, MSGL, NPRN = tokenizer(clist.pop(0))
	dir_mdl = tokenizer(clist.pop(0))
	dir_prn = tokenizer(clist.pop(0))
	del(clist[0])
	NL = tokenizer(clist.pop(0))
	LAMDA, AMAX, BMAX = tokenizer(clist.pop(0))
	NQ, LAT, IPRIM, NQR2 = ut.e4i(clist.pop(0))
	A, B, C = ut.e3f(clist.pop(0))
	if IPRIM == 1:
		ALPHA, BETA, GAMMA = ut.e3f(clist.pop(0))
		# convert unit degree to radian
		alpha,beta,gamma = map(ut.DtoR, [ALPHA,BETA,GAMMA])
		# convert angles to lattice vectors
		Lattice =  ut.AtoV(A, B, C, alpha, beta, gamma)
	elif IPRIM == 0:
		Lattice = list(map(lambda x: ut.e3f(clist.pop(0),range(3))))
		# convert lattice vectors to angles
		alpha, beta, gamma = ut.VtoA(Lattice)
		# convert unit radian to degree
		ALPHA,BETA,GAMMA = map(ut.RtoD, [alpha,beta,gamma])
	Basis = list(map(lambda x: list(ut.e3f(clist.pop(0))),range(NQ)))
	return [JOBNAM, MSGL, NPRN, dir_mdl, dir_prn, NL, LAMDA, AMAX, BMAX, NQ, LAT, IPRIM, NQR2, Lattice, Basis]

def FHNDLR(clist):
	check_category(clist[0], 'FHNDLR')
	# read time
	timestamp = ut.lat_headtime(clist.pop(0), clist.pop(0))
	# read info.
	JOB = ut.css(clist.pop(0))
	del clist[0:2]
	EMTO        = ut.css(clist.pop(0))
	branch      = ut.css(clist.pop(0))
	hash_key    = ut.css(clist.pop(0))
	compile_on  = ut.css(clist.pop(0))
	OS          = ut.css(clist.pop(0))
	CPU         = ut.css(clist.pop(0))
	compiler    = ut.css(clist.pop(0))
	library     = ut.css(clist.pop(0))
	return [timestamp, JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library]

def PRIMV(clist):
	# check category
	check_category(clist.pop(0), 'PRIMV')
	# read info.
	A,B,C = tokenizer(clist.pop(0))
	ALPHA,BETA,GAMMA = tokenizer(clist.pop(0))
	del clist[0:2]
	Lattice = list(map(lambda x: ut.v3(clist.pop(0)),range(3)))
	NQ3 = int(clist.pop(0).split('=')[1])
	Basis = list(map(lambda x: ut.v3(clist.pop(0)),range(NQ3)))
	# return info.
	return [A,B,C,ALPHA,BETA,GAMMA,Lattice,Basis]

def PRIMKR(clist):
	# check category
	str0 = check_category(clist.pop(0), 'PRIMKR')
	# read info.
	temp = str0.split(':')[1].split('=')
	WS_radius, VOL = map(lambda x : float(x[:10]),temp)
	del clist[0:2]
	reciprocal = list(map(lambda x: ut.v3(clist.pop(0)),range(3)))
	# return info.
	return [WS_radius, VOL, reciprocal]

def SET3D(clist):
	check_category(clist.pop(0), 'SET3D')

def BMDL(clist):
	# check category
	str0 = check_category(clist.pop(0), 'BMDL')
	# read info.
	NPRN = tokenizer(str0)
	NL,NQ,NLM,NLMQ = tokenizer(clist.pop(0))
	MSGL = tokenizer(clist.pop(0))
	AMAX,BMAX,ALAMDA = tokenizer(clist.pop(0))
	RMAX,GMAX = tokenizer(clist.pop(0))
	# return info.
	return [NPRN,NL,NQ,NLM,NLMQ,MSGL,AMAX,BMAX,ALAMDA,RMAX,GMAX]

def LATT3M(clist):
	# check category
	str0 = check_category(clist.pop(0), 'LATT3M')
	# read info.
	R1, RA, G1 = tokenizer(str0)
	GA = tokenizer(clist.pop(0))
	NUMR, NUMG, NUMVR, NUMVG = tokenizer(clist.pop(0))
	# return info.
	return [R1, RA, G1, GA, NUMR, NUMG, NUMVR, NUMVG]

def BMDL2(clist):
	# check category
	str0 = check_category(clist.pop(0), 'BMDL')
	# read info.
	CMDL = tokenizer(str0)
	# return info.
	return [CMDL]


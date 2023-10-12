#!/usr/local/anaconda3/bin/python
import utils as ut
from utils import tokenizer, tokenizer2, check_category, check_dat
from utils import category_cognition, category_classify

def CALL_CATEGORY(clist, nq, afm, ns):
	while category_cognition(clist[0]) is 0:
		del(clist[0])
	target = category_classify(clist[0])
	#print(target)
	if target == 'MLTPM1':
		return target, MLTPM1(clist, ns, nq)
	elif target == 'MLTPM2':
		return target, MLTPM2(clist)
	elif target == 'OPTPOT':
		return target, OPTPOT(clist, ns)
	elif target == 'KGRN1':
		return target, KGRN1(clist, afm)
	elif target == 'KGRN2':
		return target, KGRN2(clist)
	elif target == 'KGRN3':
		return target, KGRN2(clist)
	elif target == 'KGRN4':
		return target, KGRN2(clist)
	elif target == 'PATHOP':
		return target, MLTPM2(clist)
	elif target == 'EBTOP':
		return target, EBTOP(clist)
	elif target == 'FESPTH':
		return target, FESPTH(clist)
	elif target == 'ZMESH':
		return target, ZMESH(clist)
	elif target == 'DOSPTH':
		return target, DOSPTH(clist)
	elif target == 'PRNPRM':
		return target, PRNPRM(clist, ntnta, zmsh)
	else:
		raise KeyError(f'{target} is Not implemented yet!')

def PRNPRM(clist, ntnta, zmsh, lmax):
	if lmax > 3:
		raise KeyError(f'{lmax} > 3 is Not implemented yet!')
	
	if zmsh is 'M' or zmsh is 'm' or zmsh if 'f':
		np = 2
	else:
		np = 1
	

	PRNPRM1 = list()
	for nta in ntnta:
		it_list = list()
		for ita in nta:
			ita_list = list()
			for ip in range(np):
				ip_list = list()
				del(clist[0:3]) # del lines of Atom, Exch, and Panel
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # E-nu
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # D-nu    
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Dnud    
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Omega-  
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # S+Phisq-
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Phi-/Phi+     
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Mu      
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Tau     
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # A       
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # C       
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # B       
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # V       
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # D(Ef)     
				ip_list.append(tokenizer2(clist.pop(0), even=0)[2:]) # Bot, Top
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # V-Madelung
				ip_list.append(tokenizer2(clist.pop(0), even=0)[2:]) # V(S) Up,Dwn
				ip_list.append(tokenizer2(clist.pop(0), even=0)[2:]) # V(W) Up,Dwn
				ita_list.append(ip_list)
			it_list.append(ita_list)
		PRNPRM1.append(it_list)
	
	PRNPRM2 = list()
	PRNPRM2.append(tokenizer2(clist.pop(0), even=0)[1:])
	PRNPRM2.append(tokenizer2(clist.pop(0), even=0)[1:])

	PRNPRM3 = list()
	for nta in ntnta:
		it_list = list()
		for ita in nta:
			ita_list = list()
			for ip in range(np):
				ip_list = list()
				del(clist[0:2]) # del lines of Atom and Panel
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Nos(Ef)
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Nos(Ef)-sum
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Dos(Ef)
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Dos(Ef)-sum
				ip_list.append(tokenizer2(clist.pop(0), even=0)[2:]) # Magn. mom.
				ip_list.append(tokenizer2(clist.pop(0), even=0)[1:]) # Stoner-I
				ip_list.append(tokenizer2(clist.pop(0), even=1)) # Hopfield
				ip_list.append(tokenizer2(clist.pop(0), even=1)) # HopField
				ita_list.append(ip_list)
			it_list.append(ita_list)
		PRNPRM3.append(it_list)
	


def DOSPTH(clist):
	del(clist[0])

def ZMESH(clist):
	del(clist[0])
	while clist[0][1] == ' ':
		del(clist[0])

def FESPTH(clist):
	del(clist[0])

def EBTOP(clist):
	del(clist[0])
	bot,top = tokenizer2(clist.pop(0), even=0)
	return [bot,top]

def MLTPM1(clist, spin, nq):   #Multipole
	del(clist[0:3])
	list_mltpm = list()
	if spin is 1:
		for iq in range(nq):
			list_mltpm.append(tokenizer2(clist.pop(0), even=0, spl1='-', spl2=' -'))
			list_mltpm[iq].insert(2, '0.0000') # add Spin 0
	else:
		for iq in range(nq):
			list_mltpm.append(tokenizer2(clist.pop(0), even=0, spl1='-', spl2=' -'))
	Tot = tokenizer(clist.pop(0))
	return [list_mltpm, Tot]

def MLTPM2(clist):    #Non vanishing #PATHOP
	del(clist[0])
	while category_cognition(clist[0]) is 0:
		del(clist[0])

def OPTPOT(clist, spin):
	# parse Fbar, g, VolI for spins
	optpot = list()
	for x in range(spin):
		_,_,Fbar,_,g,_,VolI = tokenizer2(clist.pop(0),even=0)
		optpot.append([Fbar,g,VolI])
	# parse VMTZ up and down
	_,up,dn = tokenizer2(clist.pop(0), even=0)
	VMTZ = [up,dn]
	# delete Local muffin-tin zero for IT
	while category_cognition(clist[0]) is 0:
		del(clist[0])
	return [optpot,VMTZ]

def KGRN1(clist, afm):   #Iteration
	_,_,_,Iteration,_,Etot,_,erren = tokenizer2(clist.pop(0), even=0)
	if afm is not 'P':
		_,_,Magmom = tokenizer2(clist.pop(0), even=0)
	else:
		Magmom = 0
	_,_,Dysonloops,_,EF,_,erref = tokenizer2(clist.pop(0), even=0)
	return [Iteration,Etot,erren,Magmom,Dysonloops,EF,erref]

def KGRN2(clist): #QTR #QSCA #QCPA
	category = category_classify(clist[0])
	qtr = list()
	qtr.append(tokenizer2(clist.pop(0), even=0)[2:])
	while category_classify(clist[0]) is category:
		qtr.append(tokenizer2(clist.pop(0), even=0)[2:])
	return [qtr]

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



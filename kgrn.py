#!/usr/local/anaconda3/bin/python
import utils as ut
from utils import tokenizer, tokenizer2, check_category
from utils import category_cognition, category_classify

def CALL_CATEGORY(clist, nq, afm, ns, ntnta, zmsh):
	# pre-processing
	while category_cognition(clist[0]) is 0:
		del(clist[0])
	target = category_classify(clist[0])
	# parsing categories
	if target == 'MLTPM1':
		return target, MLTPM1(clist, ns, nq)
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
	elif target == 'EBTOP':
		return target, EBTOP(clist)
	elif target == 'PRNPRM':
		return target, PRNPRM(clist, ntnta, zmsh)
	# flushing categories
	elif target == 'MLTPM2': 
		return FLUSH(clist)
	elif target == 'PATHOP': 
		return FLUSH(clist)
	elif target == 'FESPTH':
		return FLUSH(clist)
	elif target == 'ZMESH':
		return FLUSH(clist)
	elif target == 'ZMESHwarning': 
		return FLUSH(clist)
	elif target == 'DOSPTH':
		return FLUSH(clist)
	elif target == 'FCDPTH':
		return FLUSH(clist)
	elif target == 'KKRFCD':
		return FLUSH(clist)
	elif target == 'MGAUN':
		return FLUSH(clist)
	elif target == 'MGAUNT':
		return FLUSH(clist)
	elif target == 'GRNFCD':
		return FLUSH(clist)
	elif target == 'ROTCHD':
		return FLUSH(clist)
	elif target == 'ELDENS':
		return FLUSH(clist)
# For NOT implemented categories
	else:
		raise KeyError(f'{target} is Not implemented yet!')

###########################################################
#                                                         #
#                   CATEGORY FUNCTIONS                    #
#                                                         #
###########################################################

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

def OPTPOT(clist, spin):
	# parse Fbar, g, VolI for spins
	optpot = list()
	for x in range(spin):
		_,_,Fbar,_,g,_,VolI = tokenizer2(clist.pop(0),even=0)
		optpot.append([Fbar,g,VolI])
	# parse VMTZ up and down
	if spin == 2:
		_,up,dn = tokenizer2(clist.pop(0), even=0)
	elif spin == 1:
		_,up = tokenizer2(clist.pop(0), even=0)
		dn = up
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

def EBTOP(clist):
	del(clist[0])
	bot,top = tokenizer2(clist.pop(0), even=0)
	return [bot,top]

def PRNPRM(clist, ntnta, zmsh, lmax=3):
	if lmax > 3:
		raise KeyError(f'{lmax} > 3 is Not implemented yet!')
	
	if zmsh is 'M' or zmsh is 'm' or zmsh is 'f':
		np = 2
	else:
		np = 1
	

	PRNPRM1 = list() # potential parameters
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
	
	PRNPRM2 = list() # Fermi level & muffin-tin potential
	PRNPRM2.append(tokenizer2(clist.pop(0), even=0)[1:])
	PRNPRM2.append(tokenizer2(clist.pop(0), even=0)[1:])

	PRNPRM3 = list() # moments
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
	
	PRNPRM4 = list() # PRNPRM
	for nta in ntnta:
		it_list = list()
		for ita in nta:
			ita_list = list()
			ita_list.append(tokenizer2(clist.pop(0)[9:])) # EONE, VINT, EKIN
			ita_list.append(tokenizer2(clist.pop(0))) # ECOR, ENUC, EMADL
			ita_list.append(tokenizer2(clist.pop(0))) # EVAL, EXCT, EXCC 
			ita_list.append(tokenizer2(clist.pop(0))) # ETOT, OKAE, E[n] 
			ita_list.append(tokenizer2(clist.pop(0))) # T*S , E-TS       
			it_list.append(ita_list)
		PRNPRM4.append(it_list)
	
	PRNPRM5 = list() # energy
	del(clist[0:2])
	for nta in ntnta:
		it_list = list()
		for ita in nta:
			ita_list = list()
			ita_list.append(tokenizer2(clist.pop(0), even=0)[2]) # Kinetic energy
			ita_list.append(tokenizer2(clist.pop(0), even=0)[2]) # Madelung energy
			ita_list.append(tokenizer2(clist.pop(0), even=0)[2]) # El-ion energy
			ita_list.append(tokenizer2(clist.pop(0), even=0)[2]) # El-el energy
			ita_list.append(tokenizer2(clist.pop(0), even=0)[2]) # Exc energy
			del(clist[0])
			ita_list.append(tokenizer2(clist.pop(0), even=0)[1]) # Total     
			ita_list.append(tokenizer2(clist.pop(0), even=0)[1]) # Total+OKAE
			ita_list.append(tokenizer2(clist.pop(0), even=0)[1::4]) # Total+Ewald, 4pi SS n(S)
	
	PRNPRM6 = list()
	N = 0
	for nta in ntnta:
		for ita in nta:
			N = N + 1
	if N > 1:
		PRNPRM6.append(tokenizer2(clist.pop(0), even=0)[2]) # Total energy
		PRNPRM6.append(tokenizer2(clist.pop(0), even=0)[2]) # Total energy+OKA
		PRNPRM6.append(tokenizer2(clist.pop(0), even=0)[1]) # Total+Ewald
	else:
		PRNPRM6.append(PRNPRM5[0][5])
		PRNPRM6.append(PRNPRM5[0][6])
		PRNPRM6.append(PRNPRM5[0][7][0])
	
	# PRNPRM7 은 특수한 중복정보 이므로 생략함.
	return [PRNPRM1,PRNPRM2,PRNPRM3,PRNPRM4,PRNPRM5,PRNPRM6]

def FLUSH(clist):
	del(clist[0])
	while category_cognition(clist[0]) is 0:
		del(clist[0])
		if len(clist) == 0:
			break
	return None


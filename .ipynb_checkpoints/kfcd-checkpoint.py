import utils as ut
from utils import tokenizer, check_category
import sys
import numpy as np

def kfcd_comp(elines):
    n_comp = {}
    for i, line in enumerate(elines):
        iq, ita, NS = list(ut.e3i(line))
        n_comp[iq] = ita
    return n_comp, NS

def FHNDLR(clines):
	str0 = check_category(clines.pop(0), 'FHNDLR')
	# read time
	timestamp = ut.lat_headtime(str0, clines.pop(0))
	# read info.
	JOB         = ut.css(clines.pop(0))
    del clines[0:5]
	EMTO        = ut.css(clines.pop(0))
	branch      = ut.css(clines.pop(0))
	hash_key    = ut.css(clines.pop(0))
	compile_on  = ut.css(clines.pop(0))
	OS          = ut.css(clines.pop(0))
	CPU         = ut.css(clines.pop(0))
	compiler    = ut.css(clines.pop(0))
	library     = ut.css(clines.pop(0))
	return timestamp, JOB, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library

def STRINP(clines, n_comp):
    NQ = len(n_comp)
    check_category(clines.pop(0), 'STRINP')
    del clines[0:1]
    WI = []
    WC = []
    WS = []
    WSA = []
    for i in range(NQ):
        wi, wc, ws, wsa = tokenizer(clines.pop(0), even=0)[1:]
        WI.append(wi)
        WC.append(wc)
        WS.append(ws)
        WSA.append(WSA)
    return WI, WC, WS, WSA

def CHDINP(clines, n_comp):
	NQ = len(n_comp)
	check_category(clines.pop(0),'CHDINP')
    
	# Get lattice and basis
	Lattice = list(map(lambda x: list(ut.e3f(clines.pop(0))),range(3)))
	alpha, beta, gamma = ut.VtoA(Lattice)
	ALPHA, BETA, GAMMA = map(ut.RtoD, [alpha,beta,gamma])
	Basis = list(map(lambda x: list(ut.e3f(clines.pop(0))),range(NQ)))
    
	Site_info = []
	del clines[0:1]
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			Site_info.append(tokenizer(clines.pop(0), even=0))
    
	ASA_info = []
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			del clines[0:1]
			tmp = []
			tmp = tmp + tokenizer(clines.pop(0))
			tmp = tmp + tokenizer(clines.pop(0))
			tmp = tmp + tokenizer(clines.pop(0))
			tmp = tmp + tokenizer(clines.pop(0))
			ASA_info.append(tmp)
		del clines[0:1]
	del clines[0:5]

	return Site_info, ASA_info

def INPUT(clines):
	str0 = check_category(clines.pop(0), 'INPUT')
	Lmax_shape = ut.colonspacestring(str0)
	Lmax_charg = ut.colonspacestring(clines.pop(0))
	return Lmax_shape, Lmax_charg

def SHPINP(clines, n_comp):
	check_category(clines.pop(0), 'SHPINP')
	J_term = []
	S_term = []
	l_nint = {}
	for iq in n_comp:
		del clines[0:1]
		for ita in range(n_comp[iq]):
			J_term.append(tokenizer(clines.pop(0)))
			S_term.append(tokenizer(clines.pop(0)))
		# SHPINP:** 부분 처리하기

		del clines[0:1]
		for ita in range(n_comp[iq]):
			NINT = ut.e1i(clines.pop(0), s=5)
			l_nint[str(iq)+','+str(ita)] = NINT
			del clines[0:1]
			for i in range(NINT):
				del clines[0:1]
		del clines[0:1]
			
	return l_nint

def OVRLPS(clines, n_comp):
	NQ = len(n_comp)
	over_mat = np.zeros((NQ,NQ,4))
	for nq in n_comp:
		for ita in range(n_comp[nq]):
			check_category(clines.pop(0), 'OVRLPS')
			NOV = ut.e1i(clines.pop(0), s=5)
			del clines[0:1]
			if ita == 0:
				for nov in range(NOV):
					tmp = tokenizer(clines.pop(0),even=0)
					iq = nq - 1
					jq = int(tmp[0]) - 1
					over_mat[iq,jq,0] += 1
					over_mat[iq,jq,1:] = list(map(float, tmp[4:7]))
			else:
				del clines[0:NOV]
			del clines[0:1]
	return over_mat

def SETMADL(clines):
	str0 = check_category(clines.pop(0), 'SETMADL')
	lmax = ut.e1i(str0, s=5)
	del clines[0:1]
	return lmax

def SETGAUSS(clines):
	str0 = check_category(clines.pop(0), 'SETGAUSS')
	NTH, NFI = ut.e2i(str0, s=5)
	return NTH, NFI

def ASACHD(clines, n_comp):
	check_category(clines.pop(0), 'ASACHD')
	check_key = 1
	while(check_key):
		if tokenizer(clines.pop(0), even=0)[0] == 'IS':
			check_key = 0

	for iq in n_comp:
		for ita in range(n_comp[iq]):
			for i in range(2):
				del clines[0:1]

	force = list(ut.e2f(clines.pop(0), s=12))[0]

	return force

def SETXCP(clines):
	str0 = check_category(clines.pop(0), 'SETXCP')
	IXC, TXCH = tokenizer(str0)
	return IXC, TXCH

def RENORM(clines, n_comp, NS, l_nint):
	check_category(clines.pop(0), 'RENORM')
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			for IS in range(NS):
				del clines[0:1]
				key = str(iq)+','+str(ita)
				for nint in range(l_nint[key]):
					del clines[0:1]
				del clines[0:1]
	del clines[0:1]

	return 0

def FCDCHD(clines):
	check_category(clines.pop(0), 'FCDCHD')
	return 0

def FCDREN(clines):
	check_category(clines.pop(0), 'FCDREN')
	del clines[0:2]
	mag = tokenizer(clines.pop(0), even=0)[6]
	return mag

def ENCOMP(clines):
	check_category(clines.pop(0), 'ENCOMP')
	# Hartree
	del clines[0:1]
	ENUC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EHAR = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Coul = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Hartree = [ENUC, EHAR, Coul]
	# LDA
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	LDA = [Exc_nL, EXC]
	# PBE
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	PBE = [Exc_nL, EXC]
	# P07
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	P07 = [Exc_nL, EXC]
	# AM5
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	AM5 = [Exc_nL, EXC]
	# LAG
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	LAG = [Exc_nL, EXC]
	# Kinetic
	del clines[0:1]
	EKIN = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	OKAE = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Ekin = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Kinetic = [EKIN, OKAE, Ekin]
	return Hartree, LDA, PBE, P07, AM5, LAG, Kinetic

def FCDEN(clines, n_comp):
	mag = []
	energy = []
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			FCDCHD(clines)
			mag.append(FCDREN(clines))
			energy.append(ENCOMP(clines))
	tot_mag = tokenizer(clines.pop(0), spl=' ')[3] 
	return mag, tot_mag, energy

def LITTLB(clines):
	str0 = check_category(clines.pop(0), 'LITTLB')
	l_opt = tokenizer(str0)
	return l_opt

def OVCORR(clines, n_comp):
	# overlap correction setting
	for iq in n_comp:
		check_category(clines.pop(0), 'OVCORR')
		del clines[0:2]
	
	# Madelung correction
	del clines[0:1]
	for iq in n_comp:
		del clines[0:2]

	# overlap correction calculation
	for iq in n_comp:
		check_category(clines.pop(0), 'OVCORR')
		tmp = LITTLB(clines)
	return 0

def FCDMAD(clines, n_comp):
	str0 = check_category(clines.pop(0), 'FCDMAD')
	lmax = ut.e1i(str0, s=5)
	ovcor = (clines[0][0:11].strip().split(':')[0] == 'OVCORR')
	if ovcor:
		OVCORR(clines, n_comp)

	# IQ, ITA, ASA, EMM, ENR, ER, EMADL
	del clines[0:1]

	for iq in n_comp:
		for ita in range(n_comp[iq]):
			del clines[0:1]

	return lmax

def STRESS(clines):
	return 0

def TOTALE(clines, n_comp):
	check_category(clines.pop(0), '*TOTALE')
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			IQ, ITA, CONC = tokenizer(clines.pop(0))[0:3]
			del clines[0:1]
			# Ts
			Ts = tokenizer(clines.pop(0), spl=' ')[1]
			# Kinetic
			Kinetic = tokenizer(clines.pop(0), spl=' ')[1]
			# Hartree
			Hartree = tokenizer(clines.pop(0), spl=' ')[1]
			# LDA
			LDA = tokenizer(clines.pop(0), spl=' ')[1]
			# PBE
			PBE = tokenizer(clines.pop(0), spl=' ')[1]
			# P07
			P07 = tokenizer(clines.pop(0), spl=' ')[1]
			# AM5
			AM5 = tokenizer(clines.pop(0), spl=' ')[1]
			# LAG
			LAG = tokenizer(clines.pop(0), spl=' ')[1]
			# Tot LDA
			Tot_LDA = tokenizer(clines.pop(0), spl=' ')[1]
			del clines[0:1]
			# Tot PBE
			Tot_PBE = tokenizer(clines.pop(0), spl=' ')[1]
			del clines[0:1]
			# Tot P07
			Tot_P07 = tokenizer(clines.pop(0), spl=' ')[1]
			del clines[0:1]
			# Tot AM5
			Tot_AM5 = tokenizer(clines.pop(0), spl=' ')[1]
			del clines[0:1]
			# Tot LAG
			Tot_LAG = tokenizer(clines.pop(0), spl=' ')[1]
			del clines[0:1]
	
	total_sum = (clines[0].strip().split(':')[0] == '*Total energy')
	del clines[0:1]
	if total_sum:
		# Tot LDA
		Tot_LDA = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot PBE
		Tot_PBE = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot P07
		Tot_P07 = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot AM5
		Tot_AM5 = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot LAG
		Tot_LAG = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]

	sigma_opt = (clines[0][0:15].strip().split(':')[0] == 'STRESS')
	if sigma_opt:
		STRESS(clines)
	return 0

def END(clines):
	if len(clines) > 1:
		print(" ### Error : Too many lines left \n"); sys.exit()
	check_category(clines.pop(0), 'KFCD')
	print(" Parsing END")
	return 0


	
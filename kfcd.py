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
	STRUC       = ut.css(clines.pop(0)).split('/')[-1].split('.')[0]
	del clines[0:4]
	EMTO        = ut.css(clines.pop(0))
	branch      = ut.css(clines.pop(0))
	hash_key    = ut.css(clines.pop(0))
	compile_on  = ut.css(clines.pop(0))
	OS          = ut.css(clines.pop(0))
	CPU         = ut.css(clines.pop(0))
	compiler    = ut.css(clines.pop(0))
	library     = ut.css(clines.pop(0))
	return timestamp, JOB, STRUC, EMTO, branch, hash_key, compile_on, OS, CPU, compiler, library

def STRINP(clines, n_comp):
    NQ = len(n_comp)
    check_category(clines.pop(0), 'STRINP')
    del clines[0:1]
    WI, WC, WS, WSA = zip(*[list(map(float, tokenizer(clines.pop(0), even=0)[1:])) for i in range(NQ)])
    return WI, WC, WS, WSA

def CHDINP(clines, n_comp):
	NQ = len(n_comp)
	check_category(clines.pop(0),'CHDINP')
    
	# Get lattice and basis

	# lattice
	del clines[0:3]
	# basis
	del clines[0:NQ]
	
	# Site info.
	del clines[0:1]
	WS, JWS, JRI, JRC, ION, Z, ELN, XQTR, CONC = zip(*[list(map(float, tokenizer(clines.pop(0), even=0)[2:])) for iq in n_comp for ita in range(n_comp[iq])])
	
	# ASA info.
	Data = []
	for iq in n_comp:
		tmp, data = zip(*[[clines.pop(0)] + [tokenizer(clines.pop(0)) + tokenizer(clines.pop(0)) + tokenizer(clines.pop(0)) + tokenizer(clines.pop(0))] for ita in range(n_comp[iq])])
		Data.append(data)
		del clines[0:1]
	del clines[0:5]
	
	EONE, VINT, EKIN, ECOR, ENUC, EMADL, EVAL, EXCT, EXCC, ETOT = zip(*[list(map(float, Data[iq-1][ita])) for iq in n_comp for ita in range(n_comp[iq])])
	return JWS, JRI, JRC, ION, Z, ELN, XQTR, CONC, EONE, VINT, EKIN, ECOR, ENUC, EMADL, EVAL, EXCT, EXCC, ETOT

def INPUT(clines):
	str0 = check_category(clines.pop(0), 'INPUT')
	Lmax_shape = int(ut.colonspacestring(str0))
	Lmax_charg = int(ut.colonspacestring(clines.pop(0)))
	return Lmax_shape, Lmax_charg

def SHPINP(clines, n_comp):
	check_category(clines.pop(0), 'SHPINP')
	JRIN, JWS, JRIC = [], [], []
	l_nint = {}
	for iq in n_comp:
		del clines[0:1]
		for ita in range(n_comp[iq]):
			jrin, jws, jric = list(map(float, tokenizer(clines.pop(0))))
			JRIN.append(jrin)
			JWS.append(jws)
			JRIC.append(jric)
			del clines[0:1]
		# SHPINP:** 부분 처리하기

		del clines[0:1]
		for ita in range(n_comp[iq]):
			NINT = ut.e1i(clines.pop(0), s=5)
			l_nint[str(iq)+'_'+str(ita)] = NINT
			del clines[0:1]
			for i in range(NINT):
				del clines[0:1]
		del clines[0:1]

	return l_nint, JRIN, JWS, JRIC

def OVRLPS(clines, n_comp):
	NQ = len(n_comp)
	over_mat = np.zeros((NQ,NQ,7))
	MTD = []
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
					over_mat[iq,jq,1:] = list(map(float, tmp[1:7]))
			else:
				del clines[0:NOV]
			mtd = list(map(float, tokenizer(clines.pop(0), even=0, spl=':')[-2:]))
			MTD.append(mtd)
	return over_mat.tolist(), MTD

def SETMADL(clines):
	str0 = check_category(clines.pop(0), 'SETMADL')
	Lmax_struc = ut.e1i(str0, s=5)
	del clines[0:1]
	return [Lmax_struc]

def SETGAUSS(clines):
	str0 = check_category(clines.pop(0), 'SETGAUSS')
	NTH, NFI = ut.e2i(str0, s=5)
	return NTH, NFI

def ASACHD(clines, n_comp, NS):
	check_category(clines.pop(0), 'ASACHD')
	check_key = 1
	while(check_key):
		if tokenizer(clines.pop(0), even=0)[0] == 'IS':
			check_key = 0

	QMM, QSPIN = zip(*[list(map(float, tokenizer(clines.pop(0), even=0)[3:5])) for iq in n_comp for ita in range(n_comp[iq]) for ns in range(NS)])

	# force
	del clines[0:1]

	return QMM, QSPIN

def SETXCP(clines):
	str0 = check_category(clines.pop(0), 'SETXCP')
	IXC, TXCH = tokenizer(str0)
	return int(IXC), TXCH

def RENORM(clines, n_comp, NS, l_nint):
	check_category(clines.pop(0), 'RENORM')
	RS, QR, nSi, nSc = [],[],[],[]
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			key = str(iq)+'_'+str(ita)
			tmp = []
			for ns in range(NS):
				del clines[0:1]
				rs, qr = zip(*[ut.e2f(clines.pop(0)) for nint in range(l_nint[key])])
				nsi, nsc = list(ut.e3f(clines.pop(0)))[0::2]
				tmp.append([rs, qr, nsi, nsc])
			rs_ns, qr_ns, nsi_ns,nsc_ns = zip(*[tmp[ns] for ns in range(NS)])
			RS.append(rs_ns)
			QR.append(qr_ns)
			nSi.append(nsi_ns)
			nSc.append(nsc_ns)

	Cal_ELN = list(map(float, tokenizer(clines.pop(0))))

	return RS, QR, nSi, nSc, Cal_ELN

def FCDCHD(clines):
	check_category(clines.pop(0), 'FCDCHD')
	return 0

def FCDREN(clines, NS):
	check_category(clines.pop(0), 'FCDREN')
	nel_fcd = []
	for ns in range(NS):
		nel_fcd.append(list(ut.e2f(clines.pop(0)))[1])
	mag = tokenizer(clines.pop(0), even=0)[6]
	return nel_fcd, float(mag)

def ENCOMP(clines):
	check_category(clines.pop(0), 'ENCOMP')
	# Hartree
	del clines[0:1]
	ENUC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EHAR = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Coul = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	hartree = [ENUC, EHAR, Coul]
	# LDA
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	lda = [Exc_nL, EXC]
	# PBE
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	pbe = [Exc_nL, EXC]
	# P07
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	p07 = [Exc_nL, EXC]
	# AM5
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	am5 = [Exc_nL, EXC]
	# LAG
	del clines[0:1]
	Exc_nL = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	EXC = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	lag = [Exc_nL, EXC]
	# Kinetic
	del clines[0:1]
	EKIN = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	OKAE = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	Ekin = list(ut.equalfloat(clines.pop(0), N=2, s=17))[1]
	kinetic = [EKIN, OKAE, Ekin]
	return hartree,lda, pbe, p07, am5,lag, kinetic

def FCDEN(clines, n_comp, NS):
	NEL_FCD, Local_Mag, ENERGY = [],[],[]
	HARTREE, LDA, PBE, P07, AM5, LAG, Kinetic = [],[],[],[],[],[],[]
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			FCDCHD(clines)
			nel_fcd, mag = FCDREN(clines, NS)
			NEL_FCD.append(nel_fcd)
			Local_Mag.append(mag)

			hartree,lda, pbe, p07, am5,lag, kinetic = ENCOMP(clines)
			HARTREE.append(hartree)
			LDA.append(lda)
			PBE.append(pbe)
			P07.append(p07)
			AM5.append(am5)
			LAG.append(lag)
			Kinetic.append(kinetic)
			
	Tot_Mag = float(tokenizer(clines.pop(0), spl=' ')[3])
	return NEL_FCD, Local_Mag, LDA, PBE, P07, AM5, LAG, Kinetic, Tot_Mag

def LITTLB(clines):
	str0 = check_category(clines.pop(0), 'LITTLB')
	lmax_corr, lmaxo, lmaxi = list(map(int, tokenizer(str0)))
	return lmax_corr, lmaxo, lmaxi

def OVCORR(clines, n_comp):
	# overlap correction setting
	for iq in n_comp:
		check_category(clines.pop(0), 'OVCORR')
		del clines[0:2]
	
	# Madelung correction
	Lmax_struc_corr = ut.e1i(clines.pop(0), s=5)
	for iq in n_comp:
		del clines[0:2]

	# overlap correction calculation
	Lmax_corr,Lmaxo,Lmaxi = [],[],[]
	for iq in n_comp:
		check_category(clines.pop(0), 'OVCORR')
		lmax_corr, lmaxo, lmaxi = LITTLB(clines)
		Lmax_corr.append(lmax_corr)
		Lmaxo.append(lmaxo)
		Lmaxi.append(lmaxi)
	return Lmax_struc_corr, Lmax_corr, Lmaxo, Lmaxi

def FCDMAD(clines, n_comp):
	str0 = check_category(clines.pop(0), 'FCDMAD')
	lmax = ut.e1i(str0, s=5)
	ovcor = (clines[0][0:11].strip().split(':')[0] == 'OVCORR')
	Lmax_corr, Lmaxo, Lmaxi = [],[],[]
	if ovcor:
		Lmax_struc_corr, Lmax_corr, Lmaxo, Lmaxi = OVCORR(clines, n_comp)

	# IQ, ITA, ASA, EMM, ENR, ER, EMADL
	del clines[0:1]
	ASA, EMM, ENR, ER, EMADL = zip(*[list(map(float, tokenizer(clines.pop(0), even=0)[2:])) for iq in n_comp for ita in range(n_comp[iq])])


	return lmax, Lmax_struc_corr, Lmax_corr, Lmaxo, Lmaxi, ASA, EMM, ENR, ER, EMADL

def STRESS(clines):
	return 0

def TOTALE(clines, n_comp):
	check_category(clines.pop(0), '*TOTALE')
	Comp_info, Ts, Kinetic, Hartree, LDA, PBE, P07, AM5, LAG, Tot_LDA, Tot_PBE, Tot_P07, Tot_AM5, Tot_LAG = [],[],[],[],[],[],[],[],[],[],[],[],[],[]
	for iq in n_comp:
		for ita in range(n_comp[iq]):
			Comp_info.append(list(map(float, tokenizer(clines.pop(0))[0:3])))
			del clines[0:1]
			# Ts
			Ts.append(float(tokenizer(clines.pop(0))[0]))
			# Kinetic
			Kinetic.append(float(tokenizer(clines.pop(0))[0]))
			# Hartree
			Hartree.append(float(tokenizer(clines.pop(0))[0]))
			# LDA
			LDA.append(float(tokenizer(clines.pop(0))[0]))
			# PBE
			PBE.append(float(tokenizer(clines.pop(0))[0]))
			# P07
			P07.append(float(tokenizer(clines.pop(0))[0]))
			# AM5
			AM5.append(float(tokenizer(clines.pop(0))[0]))
			# LAG
			LAG.append(float(tokenizer(clines.pop(0))[0]))
			# Tot LDA
			Tot_LDA.append(float(tokenizer(clines.pop(0), spl='Tot')[0]))
			del clines[0:1]
			# Tot PBE
			Tot_PBE.append(float(tokenizer(clines.pop(0), spl='Tot')[0]))
			del clines[0:1]
			# Tot P07
			Tot_P07.append(float(tokenizer(clines.pop(0), spl='Tot')[0]))
			del clines[0:1]
			# Tot AM5
			Tot_AM5.append(float(tokenizer(clines.pop(0), spl='Tot')[0]))
			del clines[0:1]
			# Tot LAG
			Tot_LAG.append(float(tokenizer(clines.pop(0), spl='Tot')[0]))
			del clines[0:1]
	
	total_sum = (clines[0].strip().split(':')[0] == '*Total energy')
	Tot_Energy = []
	if total_sum:
		del clines[0:1]
		# Tot LDA
		Sys_LDA = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot PBE
		Sys_PBE = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot P07
		Sys_P07 = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot AM5
		Sys_AM5 = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]
		# Tot LAG
		Sys_LAG = tokenizer(clines.pop(0), spl=' ')[1]
		del clines[0:1]

		Tot_Energy = list(map(float ,[Sys_LDA, Sys_PBE, Sys_P07, Sys_AM5, Sys_LAG]))

	sigma_opt = (clines[0][0:15].strip().split(':')[0] == 'STRESS')
	if sigma_opt:
		STRESS(clines)
	return Comp_info, Ts, Kinetic, Hartree, LDA, PBE, P07, AM5, LAG, Tot_LDA, Tot_PBE, Tot_P07, Tot_AM5, Tot_LAG, Tot_Energy

def END(clines):
	if len(clines) > 1:
		print(" ### Error : Too many lines left \n"); sys.exit()
	check_category(clines.pop(0), 'KFCD')
	print(" Parsing END")
	return 0


	
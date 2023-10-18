#!/usr/local/anaconda3/bin/python
import sys
import re
import numpy as np
from numpy import sin, cos, sqrt
from time import strptime, mktime
from math import pi, acos
#test

### general functions ###
def tokenizer(string, even=1, spl='='):
    tmp = string.replace(spl,' ').replace('\n','').strip()
    token = re.sub(' +', ' ', tmp).split(' ')
    if even == 1:
        return token[1::2]
    if even == 0:
        return token
    
def tokenizer2(string, even=1, spl1='=', spl2=' '):
    tmp = string.replace(spl1,spl2).replace('\n','').strip()
    token = re.sub(' +', ' ', tmp).split(' ')
    if even == 1:
        return token[1::2]
    if even == 0:
        return token
    
def category_cognition(string):
	tmp = string[:11].strip()
	if tmp is '':
		return 0
	token = re.sub(' +', ' ', tmp).split(' ')
	try:
		token[0].index(':')
		return 1
	except:
		return 0

def category_classify(string):
	token = tokenizer2(string, even=0)
	if token[0] == 'KGRN:':
		if token[1] == 'Iteration':
			return 'KGRN1'
		elif token[1] == 'QTR':
			return 'KGRN2'
		elif token[1] == 'QSCA':
			return 'KGRN3'
		elif token[1] == 'QCPA':
			return 'KGRN4'
		else:
			raise KeyError(f'Something worng! {token[0]} {token[1]}')
	elif token[0] == 'OPTPOT:':
		return 'OPTPOT'
	elif token[0] == 'MLTPM:':
		if token[1] == 'Multipole':
			return 'MLTPM1'
		elif token[1] == 'Non':
			return 'MLTPM2'
		else:
			raise KeyError(f'Something worng! {token[0]} {token[1]}')
	elif token[0] == 'PATHOP:':
		return 'PATHOP'
	elif token[0] == 'EBTOP:':
		return 'EBTOP'
	elif token[0] == 'FESPTH:':
		return 'FESPTH'
	elif token[0] == 'DOSPTH:':
		return 'DOSPTH'
	elif token[0] == 'ZMESH:':
		return 'ZMESH'
	elif token[0] == 'ZMESH:**':
		return 'ZMESHwarning'
	elif token[0][:5] == 'Atom:':
		return 'PRNPRM'
	elif token[0] == 'FCDPTH:':
		return 'FCDPTH'
	elif token[0] == 'KKRFCD:':
		return 'KKRFCD'
	else:
		raise KeyError(f'{token[0]} is Not implemented!')

def check_category(string, keywd):
	key = string[0:11].strip().split(':')[0]
	if key != keywd:
		print(" ### Error : keyword mismatch; keyword = "+keywd+", input = "+key+"\n"); sys.exit()
	return string[11:]

def check_dat(string, keywd):
	key = string[0:5].strip()
	if key != keywd:
		print(" ### Error : keyword mismatch; keyword = "+keywd+", input = "+key+"\n"); sys.exit()
	return string[5:]

'''
def flush(f,N=1):
	for i in range(N):
		f.readline()
'''
def equalfloat(string,N=3,s=10):
	token = string.split('=')[1:N+1]
	if N == 1:
		return float(token[0][:s])
	return map(lambda x:float(x[:s]),token)

def equalint(string,N=4,s=3):
	token = string.split('=')[1:N+1]
	if N == 1:
		return int(token[0][:s])
	return map(lambda x:int(x[:s]),token)

def equalmix(string):
	return map(lambda x: x.split()[0],map(lambda x: x.strip(),string.split('=')[1:]))

def bracomfloat(string,N=3,s=10):
	token = string.lstrip().lstrip('(').split(',')[:N]
	if N == 1:
		return list(float(token[0][:s]))
	return list(map(lambda x:float(x[:s]),token))

def colonspacestring(string):
	token = string.split(': ')
	return token[1].strip()

def namestr(obj, namespace):
	print('something')
	print(obj)
	print(namespace)
	get_name=[name for name in namespace if namespace[name] is obj]
	print(get_name)
	return get_name[0]

def getint(string): # for parsing shape output files
    int_list = [int(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", string)]
    return int_list

def getfloat(string): # for parsing shape output files
    float_list = [float(s) for s in re.findall(r"[-+]?\d*\.\d+|\d+", string)]
    return float_list

def getstring_withoutequal(string): # for parsing shape output files
    str_list = [s for s in string.split() if not re.match(r"[-+]?\d*\.\d+|\d+", s)]
    str_list_2 = [s for s in str_list if s != '=' and s != ':']
    str_list_3 = [s.replace('=','') for s in str_list_2]
    return str_list_3

def Cleaning(list_data):
	list_clean = []
	for line in list_data:
		stripline = line.strip()
		if line.lstrip() == '':
			pass
		elif 'Hard test' in line:
			pass
		elif 'WARNING: ' in line:
			pass
		elif 'Atomic ch' in line:
			pass
		elif 'Potential' in line:
			pass
		elif 'Linear lo' in line:
			pass
		else:
			list_clean.append(line)
	return list_clean

### special functions ###

def lat_headtime(string0,string1):
	# read time
	s_HM = string0[74:].rstrip()
	s_dby = string1[70:].rstrip()
	# convert string to time object
	time_object = strptime(s_HM+s_dby, "%H:%M%d-%b-%y")
	timestamp = mktime(time_object)
	return timestamp

def kgrn_headtime(string):
	# read time
	s_HM_dby = string[61:].rstrip()
	# convert string to time object
	time_object = strptime(s_HM_dby, "%H:%M / %d-%b-%y")
	timestamp = mktime(time_object)
	return timestamp

### transform functions ###

def deg2rad(degree):
    return degree/180*pi

def rad2deg(radian):
    return radian*180/pi

def angle2vector(A, B, C, alpha, beta, gamma):
    ax = 1.
    ay = 0.
    az = 0.
    bx = round0(B/A*cos(gamma))
    by = round0(B/A*sin(gamma))
    bz = 0.
    cx = round0(C/A*cos(beta))
    cy = round0(C/A*(cos(alpha)-cos(beta)*cos(gamma))/sin(gamma))
    cz = round0(C/A*sqrt(sin(beta)**2-((cos(alpha)-cos(beta)*cos(gamma))/sin(gamma))**2))
    return [[ax,ay,az],[bx,by,bz],[cx,cy,cz]]

def vector2angle(L):
    aa = L[0][0]*L[0][0] + L[0][1]*L[0][1] + L[0][2]*L[0][2]
    bb = L[1][0]*L[1][0] + L[1][1]*L[1][1] + L[1][2]*L[1][2]
    cc = L[2][0]*L[2][0] + L[2][1]*L[2][1] + L[2][2]*L[2][2]
    ab = L[0][0]*L[1][0] + L[0][1]*L[1][1] + L[0][2]*L[1][2]
    ac = L[0][0]*L[2][0] + L[0][1]*L[2][1] + L[0][2]*L[2][2]
    bc = L[1][0]*L[2][0] + L[1][1]*L[2][1] + L[1][2]*L[2][2]
    alpha = acos(bc/sqrt(bb*cc))
    beta  = acos(ac/sqrt(aa*cc))
    gamma = acos(ab/sqrt(aa*bb))
    return alpha, beta, gamma

### micellaneous ###

def round0(v):
    return round(v,10)

### alias ###

def em(f):
	return equalmix(f)

def e3f(f,s=10):
	return equalfloat(f,3,s)

def e2f(f,s=10):
	return equalfloat(f,2,s)

def e1f(f,s=10):
	return equalfloat(f,1,s)

def e5i(f,s=3):
	return equalint(f,5,s)

def e4i(f,s=3):
	return equalint(f,4,s)

def e3i(f,s=3):
	return equalint(f,3,s)

def e2i(f,s=3):
	return equalint(f,2,s)

def e1i(f,s=3):
	return equalint(f,1,s)

def v3(f,s=10):
	return bracomfloat(f,3,s)

def css(f):
	return colonspacestring(f)

def DtoR(v):
	return deg2rad(v)

def RtoD(v):
	return rad2deg(v)

def AtoV(A,B,C,a,b,c):
	return angle2vector(A,B,C,a,b,c)

def VtoA(L):
	return vector2angle(L)

def r0(v):
	return round0(v)

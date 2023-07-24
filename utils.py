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

def Cleaning(list_data, opt='default'):
	list_clean = []
	if opt == 'kfcd':
		list_comp = []
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
		elif '***' in line:
			pass
		else:
			list_clean.append(line)
		if opt == 'kfcd' and 'ASA total energy' in line:
			list_comp.append(line)
	if opt == 'default':
		return list_clean
	else:
		return list_clean, list_comp

### special functions ###

def lat_headtime(string0,string1):
	# read time
	s_HM = string0[62:].rstrip()
	s_dby = string1[69:].rstrip()
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

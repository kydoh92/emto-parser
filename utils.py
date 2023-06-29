#!/usr/local/anaconda3/bin/python
import sys
import numpy as np
from numpy import sin, cos, sqrt
from time import strptime, mktime
from math import pi, acos

### general functions ###

def flush(f,N=1):
	for i in range(N):
		f.readline()

def equalfloat(f,N=3,s=10):
	token = f.readline().split('=')[1:N+1]
	if N == 1:
		return float(token[0][:s])
	return list(map(lambda x:float(x[:s]),token))

def equalint(f,N=4,s=3):
	token = f.readline().split('=')[1:N+1]
	if N == 1:
		return int(token[0][:s])
	return list(map(lambda x:int(x[:s]),token))

def bracomfloat(f,N=3,s=10):
	token = f.readline().lstrip().lstrip('(').split(',')[:N]
	if N == 1:
		return list(float(token[0][:s]))
	return list(map(lambda x:float(x[:s]),token))

def colonspacestring(f):
	token = f.readline().split(': ')
	return token[1].strip()
	
### special functions ###

def head_timestamp(f):
	# read time
	s_HM = f.readline()[74:].rstrip()
	s_dby = f.readline()[70:].rstrip()
	# convert string to time object
	time_object = strptime(s_HM+s_dby, "%H:%M%d-%b-%y")
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

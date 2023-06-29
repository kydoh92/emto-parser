#!/home/tjsrb2507/anaconda3/envs/pyemto/bin/python
import sys
import numpy as np
import utils as ut
from utils import flush
import json

def L2(f):
    string = f.readline()
    JOBNAM = string[10:20].strip()
    MSGL =  int(string[27:30])
    return JOBNAM, MSGL
def L3(f):
    string = f.readline()
    FOR001 = string[7:].strip()
    return FOR001
def L6(f):
    string = f.readline()
    Lmax = int(string[7:11])
    NSR = int(string[17:21])
    NFI = int(string[27:30])
    return Lmax, NSR, NFI
def L7(f):
    string = f.readline()
    NPRN = int(string[7:11])
    IVEF = int(string[17:21])
    return NPRN, IVEF
    

filename="lat_bcc.dat"
with open(filename) as f:
    flush(f)
    JOBNAM, MSGL = L2(f)
    # print(JOBNAM, MSGL)
    FOR001 = L3(f)
    # print(FOR001)
    flush(f,2)
    Lmax, NSR, NFI = L6(f)
    NPRN, IVEF = L7(f)
    # print(Lmax, NSR, NFI, NPRN, IVEF)
    
# Combine entities
Input = {
    'Meta':{
        'JOBNAM': [JOBNAM, None],
        'MSGL': [MSGL, None],
        'FOR001': [FOR001, None],
        'NPRN': [NPRN, None],
    },
    'Approximation':{
        'Lmax': [Lmax, None],
        'NSR': [NSR, None],
        'NFI': [NFI, None],
        'IVEF': [IVEF, None]
    }
}
    


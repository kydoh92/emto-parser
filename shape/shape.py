import sys
import utils as ut
import json
import re

def DAT(clist):
    i = 1
    while clist:
        if i in [1, 4, 5]:
            clist.pop(0)
            pass
        elif i == 2:
            JOBNAME, MSGL = ut.tokenizer(clist.pop(0))
            MSGL = int(MSGL)
        elif i == 3:
            [FOR001] = ut.tokenizer(clist.pop(0))
        elif i == 6:
            Lmax, NSR, NFI = list(map(int, ut.tokenizer(clist.pop(0))))
        elif i == 7:
            NPRN, IVEF = list(map(int, ut.tokenizer(clist.pop(0))))
        else:
            print("clist exist")
            clist.pop(0)
        i+=1
    return [JOBNAME, MSGL, FOR001, NPRN, Lmax, NSR, NFI, IVEF]
import utils as ut
from utils import tokenizer, check_category
import sys
import numpy as np

def kfcd_comp(elines):
    n_comp = {}
    for i, line in enumerate(elines):
        iq, ita = list(ut.e2i(line))
        n_comp[iq] = ita
    return n_comp

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
    WS_radi = []
    for i in range(NQ):
         WS_radi.append(tokenizer(clines.pop(0), even=0)[1:])
    return WS_radi
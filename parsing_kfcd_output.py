#!/usr/local/anaconda3/bin/python
import sys
import utils as ut
import json
from kfcd import kfcd_comp, FHNDLR, STRINP, CHDINP, INPUT, SHPINP, OVRLPS, SETMADL, SETGAUSS, ASACHD, SETXCP, RENORM, FCDEN, FCDMAD, TOTALE, END

#### MAIN ####

# Read and parse a text
filename = sys.argv[1]
with open(filename,'r') as f:
    lines = f.readlines()

# cleaning & get list type
clines, elines = ut.Cleaning(lines, opt='kfcd')

n_comp, NS = kfcd_comp(elines)

# Value
values = list()
values.append(FHNDLR(clines))
values.append(STRINP(clines, n_comp))
values.append(CHDINP(clines, n_comp))
values.append(INPUT(clines))
shpinp_data = SHPINP(clines, n_comp)
l_nint = shpinp_data[0]
values.append(shpinp_data[1:])
values.append(OVRLPS(clines, n_comp))
values.append(SETMADL(clines))
values.append(SETGAUSS(clines))
values.append(ASACHD(clines, n_comp, NS))
values.append(SETXCP(clines))
values.append(RENORM(clines, n_comp, NS, l_nint))
values.append(FCDEN(clines, n_comp, NS))
values.append(FCDMAD(clines, n_comp))
values.append(TOTALE(clines, n_comp))
END(clines)

# Category
categories = ['FHNDLR','STRINP','CHDINP', 'INPUT', 'SHPINP', 'OVRLPS', 'SETMADL', 'SETGAUSS', 'ASACHD', 'SETXCP', 'RENORM', 'FCDEN', 'FCDMAD','TOTALE']

# Key
keys = list()
keys.append(['time','JOB','STRUC', 'EMTO','branch','hash_key','compile_on','OS','CPU','compiler','library'])
keys.append(['WI','WC','WS','WSA'])
keys.append(['JWS', 'JRI', 'JRC', 'ION', 'Z', 'ELN', 'XQTR', 'CONC', 'EONE', 'VINT', 'EKIN', 'ECOR', 'ENUC', 'EMADL', 'EVAL', 'EXCT', 'EXCC', 'ETOT'])
keys.append(['Lmax_shape', 'Lmax_charg'])
keys.append(['JRIN', 'JWS', 'JRIC'])
keys.append(['OVRLPS_matrix', 'MTD'])
keys.append(['Lmax_struc'])
keys.append(['NTH', 'NFI'])
keys.append(['QMM(ASA)', 'QSPIN(ASA)'])
keys.append(['IXC','TXCH'])
keys.append(['RS(Re)','QR(Re)','nSi(Re)','nSc(Re)','Cal_ELN'])
keys.append(['NEL_FCD','Local_Mag', 'LDA', 'PBE', 'P07', 'AM5', 'LAG', 'Kinetic', 'Tot_Mag'])
keys.append(['Lmax_intercell', 'Lmax_struc_corr', 'Lmax_corr', 'Lmaxo', 'Lmaxi', 'ASA_corr', 'EMM_corr', 'ENR_corr', 'ER_corr', 'EMADL_corr'])
keys.append(['Comp_info', 'Ts', 'Kinetic', 'Hartree', 'LDA', 'PBE', 'P07', 'AM5', 'LAG', 'Tot_LDA', 'Tot_PBE', 'Tot_P07', 'Tot_AM5', 'Tot_LAG', 'Tot_Energy'])

# add key to info.
value_key = list()
for i,_ in enumerate(categories):
    value_key.append({ key:value for key, value in zip(keys[i],values[i])})

kfcd_output_dict = {key:value for key, value in zip(categories, value_key)}

# Save as a json file
JOB = kfcd_output_dict['FHNDLR']['JOB']
with open('./output_file/'+JOB+'_out.json', 'w') as f:
	json.dump(kfcd_output_dict, f, indent=2)
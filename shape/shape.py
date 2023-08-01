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

### FHNDLR check
def FHNDLR(clist):
    ut.check_category(clist[0], 'FHNDLR')
    # read time
    timestamp = ut.lat_headtime(clist.pop(0), clist.pop(0))
    # read info.
    FOR001 = ut.css(clist.pop(0))
    del clist[0:2]
    EMTO = ut.css(clist.pop(0))
    branch = ut.css(clist.pop(0))
    hash_key = ut.css(clist.pop(0))
    compile_one = ut.css(clist.pop(0))
    OS = ut.css(clist.pop(0))
    CPU = ut.css(clist.pop(0))
    compiler = ut.css(clist.pop(0))
    library = ut.css(clist.pop(0))
    return [timestamp, FOR001, EMTO, branch, hash_key, compile_one, OS, CPU, compiler, library]
### INPUT
def INPUT(clist):
    # NSR, LMAX, NFI, IVEF
    NSR, LMAX, NFI, IVEF = ut.getint(clist.pop(0))
    return [NSR, LMAX, NFI, IVEF]
### TRNSFM
def TRNSFM(clist):
    # sllope_matrices, KW2
    string = clist.pop(0)
    slope_matrices = string[26:36].strip()
    KW2 = float(string[50:60])
    return [slope_matrices, KW2]
### BLATTS
def BLATTS(clist):
    # format {plane_num: 1, plane_info:[x,y,z,d], point_num: 6, point_info:[[x,y,z,d(상대값)],...]}
    site_info = []
    while 1:
        string = clist.pop(0)
        # strip first line
        if "V(tetra)" in string:
            site_info.append(plane_info)
            v_info = {}
            str_list = ut.getstring_withoutequal(string)
            float_list = ut.getfloat(string)
            v_info[str_list[0]] = float_list[0]
            v_info[str_list[1]] = float_list[1]
            site_info.append(v_info)
            break
        elif len(string.split()) == 6:
            try:
                site_info.append(plane_info)
            except:
                pass
            plane_info = {}
            point_info = []
            str_list = string.split()
            plane_info['plane_num'] = int(str_list[0])
            plane_info['plane_info'] = [float(str_list[1]), float(str_list[2]), float(str_list[3]), float(str_list[4])]
            plane_info['point_num'] = int(str_list[5])
        elif len(string.split()) == 4:
            point_info.append([float(string.split()[0]), float(string.split()[1]), float(string.split()[2]), float(string.split()[3])])
            plane_info['point_info'] = point_info
    return site_info
            
def RMESH(clist):
    # format {NINT: 4, RINT: [1,1,1,1], NSRI: [1,1,1], DSRI: [1,1,1]}
    rmesh_dict = {}
    rmesh_dict['NINT'] = ut.getint(clist.pop(0))[0]
    
    temp_list = []
    for i in range(rmesh_dict['NINT']):
        temp_list.append(ut.e1f(clist.pop(0)))
    rmesh_dict['RINT'] = temp_list
    
    temp_list1 = [] # for NSRI
    temp_list2 = [] # for DSRI
    for i in range(rmesh_dict['NINT']-1): ### Error 처리
        sri_list = ut.getfloat(clist.pop(0))
        temp_list1.append(int(sri_list[1]))
        temp_list2.append(sri_list[3])
    rmesh_dict['NSRI'] = temp_list1
    rmesh_dict['DSRI'] = temp_list2
    return rmesh_dict
    
def SETROT(clist):
    # format 2
    setrot = ut.getint(clist.pop(0))[0]
    return setrot

def UPDATE(clist): ## format [{l: 1, d(l): 1, D(l): 1, %: 1}, ...]
    del clist[0:2] ## remove line for "Test convergence and store" & " l    d(l)    D(l)     %"
    update_list = []
    for i in range(int(LMAX) + 1):
        temp_list = ut.getfloat(clist.pop(0))
        update_dict = {'l': int(temp_list[0]), 'd(l)': temp_list[1], 'D(l)': temp_list[2], '%': temp_list[3]}
        update_list.append(update_dict)
    return update_list

def SITES_INFO(clist):
    sites = []
    while 1:
        site_info = {}
        # site num
        try:
            site_num_line = clist.pop(0)
        except:
            print("No more site information")
            break
        if "Site number" not in site_num_line:
            print("No more site information")
            break
        
        token = site_num_line.split(': ')
        site_num = int(token[1].strip())
        
        # BLATTS
        Si, WSA, SC = ut.getfloat(clist.pop(0))
        NSC, NVN = ut.getint(clist.pop(0))
        blatts = BLATTS(clist)
        RSORT = ut.colonspacestring(clist.pop(0))
        rmesh = RMESH(clist)
        setrot = SETROT(clist)
        update = UPDATE(clist)
        NVSF = int(ut.css(clist.pop(0)))
        SIGMA_01 = ut.e1f(clist.pop(0))
        SIGMA_0NSR = ut.e1f(clist.pop(0))
        del clist[0] # Volume 지우기
        VOL_INSCRIBED = ut.getfloat(clist.pop(0))[0]
        VOL_INTEGRATED = ut.getfloat(clist.pop(0))[0]
        VOL_SUMMED = ut.getfloat(clist.pop(0))[0]
        VOL_EXACT = ut.getfloat(clist.pop(0))[0]
        ERROR = ut.getfloat(clist.pop(0))[0]
        
        # 데이터 dict에 넣기
        site_info['site_num'] = site_num
        site_info['Si'] = Si; site_info['WSA'] = WSA; site_info['SC'] = SC
        site_info['NSC'] = NSC; site_info['NVN'] = NVN
        site_info['BLATTS'] = blatts; site_info['RSORT'] = RSORT
        site_info['RMESH'] = rmesh; site_info['SETROT'] = setrot
        site_info['UPDATE'] = update; site_info['NVSF'] = NVSF
        site_info['SIGMA_01'] = SIGMA_01; site_info['SIGMA_0NSR'] = SIGMA_0NSR
        site_info['VOL_INSCRIBED'] = VOL_INSCRIBED; site_info['VOL_INTEGRATED'] = VOL_INTEGRATED
        site_info['VOL_SUMMED'] = VOL_SUMMED; site_info['VOL_EXACT'] = VOL_EXACT
        site_info['ERROR'] = ERROR
        sites.append(site_info)
        
    return sites    ### 내용 리스트 내보내기
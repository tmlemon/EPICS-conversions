#!/usr/bin/env python
'''
author:  Tyler Lemon
date:    2019-04-17
'''
import subprocess
import sys
import os
from datetime import datetime
import time
import epics

dev = True
size = 500

path = sys.argv[1]
if path[-1] != '/': path+'/'

if sys.argv[2] != 'LATEST':
    savFile = sys.argv[1]
else:
    fList = os.listdir(path)
    poss = []
    mostRecent = ['','']
    for item in fList:
        if item[-4:] == '.sav':
            check = '_'.join(item[:-4].split('_')[-2:])
            if check > mostRecent[0]:
                mostRecent = [check,item]
    savFile = mostRecent[1]
if not os.path.isfile(path+savFile) or savFile[-4:] != '.sav':
    if savFile == '':
        print('ERROR: No file to restore from found in current working \
directory.')
    else:
        print('ERROR: File to restore from must exist.')
    sys.exit(1)




props = ['V0Set','I0Set','SVMax','Rup','RDwn']

with open(path+savFile,'r') as f:
    restData = f.readlines()

count = 0
pvs,vals = [],[]
pvsHold,valsHold = [],[]
for line in restData:
    if line.strip()[0] not in ['#','']:
        line = line.strip().split('\t')
        chid,crate,slot,channel,group = line[:5]
        basePV = 'hchv'+crate+':'+slot.zfill(2)+':'+channel.zfill(3)+':'
        propSet = line[5:]
        for i,prop in enumerate(propSet):
            count += 1
            if dev:
                p = 'devIOC:ai'+str(count)
                v = str(count*2)
            else:
                p = basePV+props[i]
                v = float(prop)
            pvsHold.append(p)
            valsHold.append(v)
            if len(pvsHold) >= size:
                pvs.append(pvsHold)
                vals.append(valsHold)
                pvsHold,valsHold = [],[]
pvs.append(pvsHold)
vals.append(valsHold)

for q,grp in enumerate(pvs):
    epics.caput_many(grp,vals[q])


print('RESTORE FROM\n'+savFile+'\nCOMPLETE')

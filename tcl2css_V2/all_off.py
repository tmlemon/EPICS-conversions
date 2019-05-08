#!/usr/bin/env python

import org.csstudio.opibuilder.scriptUtil as SU
import socket

devList = ['dsg-c-linux1.jlab.org']
dev = socket.gethostname() in devList

go = SU.PVUtil.getDouble(pvs[0])
toShow = str(SU.PVUtil.getString(pvs[1]))
if go == 1:
    goState = 'OFF'
confirm = SU.GUIUtil.openConfirmDialog('Confirm turning all '+toShow+\
    ' HV channels '+goState)

if confirm: #POWER TOGGLE CONFIRMED CASE
    dirr = SU.FileUtil.workspacePathToSysPath('CSS')
    if dirr[-1] != '/': dirr += '/'

    configFile,groupFile = dirr+'HV.hvc',dirr+'HV.group'

    # Reads in groups file.
    groups = []
    with open(groupFile,'r') as f:
        for line in f.readlines():
            spectrometer = line.strip().split(' ')[1]
            groups.append([line.strip().split(' ')[0],\
                ' '.join(line.strip().split(' ')[1:])])


    # Reads in channel configuration file and splits up config file into groups.
    with open(configFile,'r') as f:
        configLines = f.readlines()
    for i,grp in enumerate(groups):
        for line in configLines:
            if line[0] != '#' and line[0] != '\n':
                group = line.strip().split(' ')[4]
                if group == grp[0]:
                    groups[int(i)].append(line.strip().split(' ')[:4])

    pwPVs = []
    for grp in groups:
        grpNum,grpName = grp[:2]
        channels = grp[2:]
        if grpName == toShow:
            count = 0
            for channel in channels:
                count += 1
                chID,cr,sl,ch = channel
                if dev: pv = 'devIOC:ai'+str(count)
                else: pv = 'hchv'+cr+':'+sl.zfill(2)+':'+ch.zfill(3)+':Pw'
                SU.PVUtil.writePV(pv,0)
#END POWER TOGGLE CONFIRMED CASE

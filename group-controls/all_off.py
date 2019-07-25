#!/usr/bin/env python3

import org.csstudio.opibuilder.scriptUtil as scriptUtil

screen = str(scriptUtil.PVUtil.getString(pvs[0]))

if scriptUtil.PVUtil.getDouble(pvs[1]) == 1:
    path =  scriptUtil.FileUtil.workspacePathToSysPath('CSS')
    if path[-1] != '/':	path += '/'
    inFile = path+screen+'-list.opi'
    with open(inFile,'r') as f:
        data = f.readlines()
    for line in data:
        line = line.strip()
        if '<pv_name>' in line and '</pv_name>' in line:
            pv = line.split('<pv_name>')[1].split('</pv_name>')[0]
            if 'Pw' in pv:
                scriptUtil.PVUtil.writePV(pv,0)

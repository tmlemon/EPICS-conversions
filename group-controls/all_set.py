#!/usr/bin/env python3

import org.csstudio.opibuilder.scriptUtil as scriptUtil

prop = str(pvs[1])[6:-3].split('_')[0][3:]

now = scriptUtil.PVUtil.getDouble(pvs[1])

try:
    chg =  now != last
except:
    chg = False

screen = str(scriptUtil.PVUtil.getString(pvs[0]))

if chg:
    path =  scriptUtil.FileUtil.workspacePathToSysPath('CSS')
    if path[-1] != '/':	path += '/'
    inFile = path+screen+'-list.opi'
    with open(inFile,'r') as f:
        data = f.readlines()
    count = 0
    for line in data:
        line = line.strip()
        if '<pv_name>' in line and '</pv_name>' in line:
            pv = line.split('<pv_name>')[1].split('</pv_name>')[0]
            if prop in pv:
                scriptUtil.PVUtil.writePV(pv,now)
last = now

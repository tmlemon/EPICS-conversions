#!/usr/bin/env python

from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil

#looks at host name to see if it development PC
import socket
devList = ['dsg-c-linux1.jlab.org']
dev = socket.gethostname() in devList


#screen = 'HMS-Hodo-1-X-list.opi'
screen = str(PVUtil.getString(pvs[0]))

if PVUtil.getDouble(pvs[1]) == 1:
    path = '/home/tlemon/CSS-Workspaces/dev/CSS/'
    inFile = path+screen+'-list.opi'

    with open(inFile,'r') as f:
        data = f.readlines()

    pwPVs = []
    count = 0
    for line in data:
        line = line.strip()
        if '<pv_name>' in line and '</pv_name>' in line:
            pv = line.split('<pv_name>')[1].split('</pv_name>')[0]
            if 'Pw' in pv:
                count += 1
                if dev:
                    PVUtil.writePV('devIOC:ai'+str(count),1)
                else:
                    PVUtil.writePV(pv,1)

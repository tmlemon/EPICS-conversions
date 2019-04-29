#!/usr/bin/env python

from org.csstudio.opibuilder.scriptUtil import PVUtil
from org.csstudio.opibuilder.scriptUtil import ConsoleUtil

dev = True

prop = str(pvs[1])[6:-3].split('_')[0][3:]

now = PVUtil.getDouble(pvs[1])

try:
    chg =  now != last
except:
    chg = False

#screen = 'HMS-Hodo-1-X-list.opi'
screen = str(PVUtil.getString(pvs[0]))

if chg:
    path = '/home/tlemon/CSS-Workspaces/dev/CSS/'
    inFile = path+screen+'-list.opi'

    with open(inFile,'r') as f:
        data = f.readlines()

    count = 0
    for line in data:
        line = line.strip()
        if '<pv_name>' in line and '</pv_name>' in line:
            pv = line.split('<pv_name>')[1].split('</pv_name>')[0]
            if prop in pv:
                count += 1
                if dev:
                    PVUtil.writePV('devIOC:ai'+str(count),now)
                else:
                    PVUtil.writePV(pv,now)

last = now

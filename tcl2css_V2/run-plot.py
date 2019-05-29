#!/usr/bin/env python
'''

author: Tyler Lemon
date:   2019-05-15

Program is attached to the voltage monitoring histogram on Hall C HV CSS screens
(Version 2). The program looks at what system the user is trying to plot,
pulls all voltage monitoring (VMon) and current monitoring (IMon) PVs for that
system from the HV.hvc configuration file, and writes the PVs' values to the
histograms on the screen.

THIS PROGRAM WILL NOT WORK OUTSIDE OF CSS.

'''



from org.csstudio.opibuilder.scriptUtil import PVUtil,FileUtil,ConsoleUtil,\
    WidgetUtil
from array import array
import subprocess
import socket

# Looks at what host that script is run from to use dev PVs
devhosts = ['dsg-c-linux1.jlab.org']
dev = socket.gethostname() in devhosts

# Path to config file locations
dirr = FileUtil.workspacePathToSysPath('CSS')
if dirr[-1] != '/': dirr += '/'

# PV telling script which system to show
toShow = PVUtil.getString(pvs[0])

# Configuration files for .tcl files.
# For this program version, these files are both HMS and SHMS tcl/tk config
# files combined into one.
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


# Show or hide shaded boxes on all channels histograms.
# Most likely a temporary inclusion since if channels change or systems are
# modifed, the box locations will be incorrect.
hmsBoxes = display.getWidget('HMS_boxes')
shmsBoxes = display.getWidget('SHMS_boxes')
if toShow == 'All HMS':
    hmsBoxes.setPropertyValue('visible',True)
else:
    hmsBoxes.setPropertyValue('visible',False)
if toShow == 'All SHMS':
    shmsBoxes.setPropertyValue('visible',True)
else:
    shmsBoxes.setPropertyValue('visible',False)

# Looks through all groups and pulls out channel information on the group
# selected by the user to display.
# Also creates a list of all HMS or SHMS VMon and IMon PVs to be able to
# display the all channels monitoring histogram.


'''
WORKING ON SPLITTING INTO GROUPS ON ALL PLOT
'''
vMonPVs,iMonPVs,vCmd = [],[],[]
for gNum,grp in enumerate(groups):
    grpID,grpName = grp[:2]
    channels = grp[2:]
    # Creates all channels VMon and IMon PV list
    if toShow.split(' ')[1] == grpName.split(' ')[0]:
        for channel in channels:
            chID,crate,slot,ch = channel
            if dev:
                vMonPVs.append('devIOC:counter')
                iMonPVs.append('devIOC:counter')
            else:
                pvBase = 'hchv'+crate+':'+slot.zfill(2)+':'+ch.zfill(3)+':'
                vMonPVs.append(pvBase+'VMon')
                iMonPVs.append(pvBase+'IMon')
    # Creates PV list of all PVs for the group selected by the user.
    if grpName == toShow:
        vCmd,iCmd = ['caget','-t'],['caget','-t']
        for channel in channels:
            chID,crate,slot,ch = channel
            if dev:
                vCmd.append('devIOC:counter')
                iCmd.append('devIOC:counter')
            else:
                pvBase = 'hchv'+crate+':'+slot.zfill(2)+':'+ch.zfill(3)+':'
                vCmd.append(pvBase+'VMon')
                iCmd.append(pvBase+'IMon')
# If user selects all channels, the array vCmd will be empty, prompting the
# program to use the all channels VMon and IMon PV lists from above.
if len(vCmd) == 0:
    vCmd,iCmd = ['caget','-t'],['caget','-t']
    for g,item in enumerate(vMonPVs):
        vCmd.append(item)
        iCmd.append(iMonPVs[g])

# formats the histrogram plot bars to make it so the bar size is correlated to
# the number of channels displayed
barWidth = int(650/(len(vCmd)-2))
vP = display.getWidget('v_plot')
iP = display.getWidget('i_plot')

vP.setPropertyValue('trace_0_line_width',barWidth)
iP.setPropertyValue('trace_0_line_width',barWidth)

# Uses subprocess to call caget to read PV values
vRes = subprocess.check_output(vCmd)
iRes = subprocess.check_output(iCmd)
# Splits caget results into a list and converts it to a list of floats.
vOutRes = [float(i) for i in vRes.strip().split('\n')]
iOutRes = [float(i) for i in iRes.strip().split('\n')]
# Adds an empty channel to voltage and current monitor array so first and
# last channel are not cut off by autoscaling of x-axis
vOutRes.append(0)
vOutRes = [0] + vOutRes
iOutRes.append(1)
iOutRes = [1] + iOutRes
# Converts list to a float array. Float arrays are needed by XY plot widget
# to be able to display data on the plot.
pvs[2].setValue(array('f',vOutRes))
pvs[3].setValue(array('f',iOutRes))

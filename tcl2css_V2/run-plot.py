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

# Function to convert lost of PVs into a list of PV values for plot.
def makePlotList(cmdIn):
    res = subprocess.check_output(cmdIn)
    resOut = [float(i) for i in res.strip().split('\n')]
    return resOut

def padPlot(lst,fill):
    lst.append(fill)
    lst = [fill] + lst
    return lst

#function to flatten a 2-D array to 1-D
def flatten(l):
    return [item for sublist in l for item in sublist]


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
        if line[0].strip() != '#':
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


# Looks through all groups and pulls out channel information on the group
# selected by the user to display.
# Also creates a list of all HMS or SHMS VMon and IMon PVs to be able to
# display the all channels monitoring histogram.

vMonPVs,iMonPVs,vCmd = [],[],[]
for grp in groups:
    grpID,grpName = grp[:2]
    channels = grp[2:]
    # Creates all channels VMon and IMon PV list
    if toShow.split(' ')[1] == grpName.split(' ')[0]:
        vMonPVsHold,iMonPVsHold = [],[]
        for channel in channels:
            chID,crate,slot,ch = channel
            if dev:
                vMonPVsHold.append('devIOC:counter')
                iMonPVsHold.append('devIOC:counter')
            else:
                pvBase = 'hchv'+crate+':'+slot.zfill(2)+':'+ch.zfill(3)+':'
                vMonPVsHold.append(pvBase+'VMon')
                iMonPVsHold.append(pvBase+'IMon')
        vMonPVs.append(vMonPVsHold)
        iMonPVs.append(iMonPVsHold)
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

# widget references for plots to be able to set properties with the script
vP = display.getWidget('v_plot')
iP = display.getWidget('i_plot')

# If user selects all channels, the array vCmd will be empty, prompting the
# program to use the all channels VMon and IMon PV lists from above.
if len(vCmd) == 0:
    vPVs,iPVs = [[],[]],[[],[]]
    for g,grp in enumerate(vMonPVs):
        if g%2 == 0:
            vPVs[0].append(makePlotList(['caget','-t']+grp))
            vPVs[1].append([0]*len(grp))
            iPVs[0].append(makePlotList(['caget','-t']+iMonPVs[g]))
            iPVs[1].append([1]*len(grp))
        elif g%2 == 1:
            vPVs[0].append([0]*len(grp))
            vPVs[1].append(makePlotList(['caget','-t']+grp))
            iPVs[0].append([1]*len(grp))
            iPVs[1].append(makePlotList(['caget','-t']+iMonPVs[g]))
    vRes0,vRes1 = padPlot(flatten(vPVs[0]),0),padPlot(flatten(vPVs[1]),0)
    iRes0,iRes1 = padPlot(flatten(iPVs[0]),1),padPlot(flatten(iPVs[1]),1)
    vP.setPropertyValue('trace_1_visible',True)
    iP.setPropertyValue('trace_1_visible',True)
else:
    vRes0 = padPlot(makePlotList(vCmd),0)
    iRes0 = padPlot(makePlotList(iCmd),1)
    vRes1,iRes1 = [],[]
    vP.setPropertyValue('trace_1_visible',False)
    iP.setPropertyValue('trace_1_visible',False)

# formats the histrogram plot bars to make it so the bar size is correlated to
# the number of channels displayed
barWidth = int(600/(len(vRes0)-2))


vP.setPropertyValue('trace_0_line_width',barWidth)
iP.setPropertyValue('trace_0_line_width',barWidth)
vP.setPropertyValue('trace_1_line_width',barWidth)
iP.setPropertyValue('trace_1_line_width',barWidth)



# Calls funciton to create array of PV values for plot
pvs[2].setValue(array('f',vRes0))
pvs[3].setValue(array('f',vRes1))
pvs[4].setValue(array('f',iRes0))
pvs[5].setValue(array('f',iRes1))

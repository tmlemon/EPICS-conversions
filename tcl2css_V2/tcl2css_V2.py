#!/usr/bin/env python

'''
@author: Tyler Lemon
Date:    2019-05-03

PROGRAM WILL ONLY WORK IF CALLED FROM A CSS .OPI FILE!

This program uses Control System Studio's scriptUtil package to create
controls/monitoring GUIs for Hall C HV system.

tcl2css_V2.py (this program) is different from tcl2css.py (previous version)
in that it is meant to be called directly in CSS from a blank .opi file.
The previous version generated "hard copies" of the .opi files where this
version programatically generates all controls, indicators, and labels when
the screen is opened.
'''

import sys #used to read in user arguements and exit program on errors.
import os # used to check files required for program.
from array import array
import org.csstudio.opibuilder.scriptUtil as SU

dirr = SU.FileUtil.workspacePathToSysPath('CSS')
if dirr[-1] != '/': dirr += '/'

toShow = SU.PVUtil.getString(pvs[0])




#configuration files for .tcl files.
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


# Intializes some constants to make the screen.
x0 = 25
y0 = 75
widgetWidth = 75
widgetHeight = 20
onGreen = SU.ColorFontUtil.getColorFromRGB(0,255,0)
blk = SU.ColorFontUtil.getColorFromRGB(0,0,0)
bkgColor = SU.ColorFontUtil.getColorFromRGB(77,77,77)
white = SU.ColorFontUtil.getColorFromRGB(255,255,255)
labelFont = SU.ColorFontUtil.getFont('Cantarell',11,1)
titleFont = SU.ColorFontUtil.getFont('Cantarell',16,1)
ltGrey = SU.ColorFontUtil.getColorFromRGB(191,191,191)

if toShow not in ['All HMS','All SHMS']:
    if SU.PVUtil.getDouble(pvs[2]) == 1:
        displayMode = 'plot'
    else:
        displayMode = 'list'
else:
    displayMode = 'plot'
    pvs[2].setValue(1)



# Makes sure that the screens are in and stay in compact mode.
compact = SU.PVUtil.getDouble(pvs[1])
if compact != 1:
    SU.GUIUtil.compactMode()
    SU.PVUtil.writePV('loc://compact',1)

# functino to create and place channel ID labels.
def putChLabel(x,y,text):
    w = SU.WidgetUtil.createWidgetModel\
        ("org.csstudio.opibuilder.widgets.Label")
    w.setPropertyValue('border_style',1);
    w.setPropertyValue('border_color',white)
    w.setPropertyValue('width',widgetWidth+25)
    w.setPropertyValue('height',widgetHeight)
    w.setPropertyValue('x',x)
    w.setPropertyValue('y',y)
    w.setPropertyValue('text',text)
    w.setPropertyValue('font',labelFont)
    w.setPropertyValue('foreground_color',white)
    widget.addChild(w)

# function to create and place power control button.
def putPowerButton(x,y,pv):
    w = SU.WidgetUtil.createWidgetModel\
            ("org.csstudio.opibuilder.widgets.BoolButton")
    w.setPropertyValue('border_style',1)
    w.setPropertyValue('border_color',white)
    w.setPropertyValue('width',widgetWidth)
    w.setPropertyValue('height',widgetHeight)
    w.setPropertyValue('x',x)
    w.setPropertyValue('y',y)
    w.setPropertyValue('pv_name',pv)
    w.setPropertyValue('show_led',False)
    w.setPropertyValue('square_button',True)
    w.setPropertyValue('toggle_button',True)
    w.setPropertyValue('show_boolean_label',True)
    w.setPropertyValue('off_label','OFF')
    w.setPropertyValue('on_label','ON')
    widget.addChild(w)

#function to create and place indicator widget
def putIndicator(x,y,pv):
    w = SU.WidgetUtil.createWidgetModel\
        ("org.csstudio.opibuilder.widgets.TextUpdate")
    w.setPropertyValue('border_style',1)
    w.setPropertyValue('border_color',white)
    w.setPropertyValue('background_color',ltGrey)
    w.setPropertyValue('width',widgetWidth)
    w.setPropertyValue('height',widgetHeight)
    w.setPropertyValue('x',x)
    w.setPropertyValue('y',y)
    w.setPropertyValue('pv_name',pv)
    widget.addChild(w)

# function to create and place control widget.
def putControl(x,y,pv):
    w = SU.WidgetUtil.createWidgetModel\
        ("org.csstudio.opibuilder.widgets.TextInput")
    w.setPropertyValue('border_style',1)
    w.setPropertyValue('border_color',white)
    w.setPropertyValue('width',widgetWidth)
    w.setPropertyValue('height',widgetHeight)
    w.setPropertyValue('x',x)
    w.setPropertyValue('y',y)
    w.setPropertyValue('pv_name',pv)
    widget.addChild(w)

def putPlot(x,y,plotType,barWidth):
    if plotType == 'nA': yAxLog = True
    else: yAxLog = False
    w = SU.WidgetUtil.createWidgetModel\
        ("org.csstudio.opibuilder.widgets.xyGraph")
    w.setPropertyValue('axis_0_axis_title','Channel')
    w.setPropertyValue('axis_1_axis_title',plotType)
    w.setPropertyValue('axis_1_log_scale',yAxLog)
    w.setPropertyValue('name','Plot-'+plotType)
    w.setPropertyValue('show_toolbar',False)
    w.setPropertyValue('show_legend',False)
    w.setPropertyValue('pv_name','loc://Plot-'+plotType)
    w.setPropertyValue('trace_0_buffer_size',400)
    w.setPropertyValue('trace_0_concatenate_data',False)
    w.setPropertyValue('trace_0_line_width',barWidth)
    w.setPropertyValue('trace_0_trace_type',3)
    w.setPropertyValue('trace_0_update_mode',0)
    w.setPropertyValue('height',300)
    w.setPropertyValue('width',775)
    w.setPropertyValue('x',x)
    w.setPropertyValue('y',y)
    widget.addChild(w)

# Odd logic sequence to make sure creation of screen isn't looped constantly
# and old info is erased from screen when switching system.
# NOTE: this probably can be done better.
try:
    if last == toShow and lastMode == displayMode:
        change = False
    else:
        change = True
except:
    change = True

# if the system to displace changes, erase all widgets and put header back on
# display screen. Header is saved in "hv-header.opi" and is a generic table
# header with group menu.
if change:
    widget.removeAllChildren()
    lc = SU.WidgetUtil.createWidgetModel\
        ("org.csstudio.opibuilder.widgets.linkingContainer")
    lc.setPropertyValue("opi_file","hv-header.opi")
    lc.setPropertyValue("auto_size",True)
    lc.setPropertyValue("zoom_to_fit",False)
    lc.setPropertyValue("border_style",0)
    lc.setPropertyValue('x',25)
    lc.setPropertyValue('y',12)
    lc.setPropertyValue('background_color',bkgColor)
    widget.addChild(lc)

    if displayMode == 'list':
        # pulls out group that matches toShow and creates table-format control
        # screen.
        for grp in groups:
            grpID,grpName = grp[:2]
            channels = grp[2:]
            display.setPropertyValue('height',len(channels)*25+2*x0)
            if grpName == toShow:
                #title label of screen
                w = SU.WidgetUtil.createWidgetModel\
                    ("org.csstudio.opibuilder.widgets.Label")
                w.setPropertyValue('border_style',0);
                w.setPropertyValue('border_color',blk)
                w.setPropertyValue('width',1150)
                w.setPropertyValue('height',widgetHeight*2)
                w.setPropertyValue('x',25)
                w.setPropertyValue('y',0)
                w.setPropertyValue('text',toShow+' HV Controls')
                w.setPropertyValue('font',titleFont)
                w.setPropertyValue('foreground_color',white)
                widget.addChild(w)
                x = x0
                y = y0
                for channel in channels:
                    chID,crate,slot,ch = channel
                    pvBase = 'hchv'+crate+':'+slot.zfill(2)+':'+ch.zfill(3)+':'
                    putChLabel(x,y,chID)
                    putPowerButton(x+25+widgetWidth,y,pvBase+'Pw')
                    putIndicator(x+25+2*widgetWidth,y,pvBase+'Status')
                    putIndicator(x+25+3*widgetWidth,y,pvBase+'VMon')
                    putIndicator(x+25+4*widgetWidth,y,pvBase+'IMon')
                    putIndicator(x+25+5*widgetWidth,y,pvBase+'V0Setr')
                    putControl(x+25+6*widgetWidth,y,pvBase+'V0Set')
                    putControl(x+25+7*widgetWidth,y,pvBase+'I0Setr')
                    putControl(x+25+8*widgetWidth,y,pvBase+'I0Set')
                    putControl(x+25+9*widgetWidth,y,pvBase+'SVMaxr')
                    putControl(x+25+10*widgetWidth,y,pvBase+'SVMax')
                    putControl(x+25+11*widgetWidth,y,pvBase+'RUpr')
                    putControl(x+25+12*widgetWidth,y,pvBase+'RUp')
                    putControl(x+25+13*widgetWidth,y,pvBase+'RDWnr')
                    putControl(x+25+14*widgetWidth,y,pvBase+'RDWn')
                    y += widgetHeight
        lc = SU.WidgetUtil.createWidgetModel\
            ("org.csstudio.opibuilder.widgets.linkingContainer")
        lc.setPropertyValue("opi_file","hv-footer.opi")
        lc.setPropertyValue("auto_size",True)
        lc.setPropertyValue("zoom_to_fit",False)
        lc.setPropertyValue("border_style",0)
        lc.setPropertyValue('x',25)
        lc.setPropertyValue('y',y)
        lc.setPropertyValue('background_color',bkgColor)
        widget.addChild(lc)


    if displayMode == 'plot':
        for grp in groups:
            grpID,grpName = grp[:2]
            channels = grp[2:]
            if grpName == toShow:
                #title label of screen
                w = SU.WidgetUtil.createWidgetModel\
                    ("org.csstudio.opibuilder.widgets.Label")
                w.setPropertyValue('border_style',0);
                w.setPropertyValue('border_color',blk)
                w.setPropertyValue('width',775)
                w.setPropertyValue('height',widgetHeight*2)
                w.setPropertyValue('x',25)
                w.setPropertyValue('y',0)
                w.setPropertyValue('text',toShow+' HV Monitoring')
                w.setPropertyValue('font',titleFont)
                w.setPropertyValue('foreground_color',white)
                widget.addChild(w)
                x = x0
                y = y0-25

                putPlot(x,y,'V',int(500/len(channels)))
                putPlot(x,y+300+5,'nA',int(500/len(channels)))


                lc = SU.WidgetUtil.createWidgetModel\
                    ("org.csstudio.opibuilder.widgets.linkingContainer")
                lc.setPropertyValue("opi_file","hv-footer.opi")
                lc.setPropertyValue("auto_size",True)
                lc.setPropertyValue("zoom_to_fit",False)
                lc.setPropertyValue("border_style",0)
                lc.setPropertyValue('x',25)
                lc.setPropertyValue('y',y+600+10)
                lc.setPropertyValue('background_color',bkgColor)
                widget.addChild(lc)


# saves toShow as last, used to check whether screen to display has changed on
# next loop of program.
last = toShow
lastMode = displayMode

'''
if displayMode == 'plot':
    vPlot,iPlot = 'loc://Plot-nA','loc://Plot-V'
    vMon,iMon = [],[]
    count = 1
    for channel in channels:
        chID,crate,slot,ch = channel
        pvBase = 'hchv'+crate+':'+slot.zfill(2)+':'+ch.zfill(3)+':'
        vPV = SU.PVUtil.createPV('devIOC:ai'+str(count),widget)
        v = SU.PVUtil.getDouble(vPV)
        vMon.append(v)
        #iMon.append(v)
        count += 1
    #SU.PVUtil.writePV(vPlot,vMon)
    #SU.PVUtil.writePV(iPlot,iMon)
    SU.ConsoleUtil.writeInfo('test')

NOTES FOR NEXT TIME:
Trying to get monitoring histograms to autopopulate with values using script.
So far its been unsuccessful getting the PVs to be read.
Best way would be to figure out how to configure an embedded script in the
XY plot widget and do the same thing as the previous version.
Haven't been able to figure that out yet though.

'''

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


# Tries to import scriptUtil java package used by CSS to make screens.
# If unsuccessful, this program assumes you are debugging and only prints out
# channel ID and crate/slot/channel info.
try:
    import org.csstudio.opibuilder.scriptUtil as SU
    dev = False
except:
    print("You must be running outside of CSS. That's okay. Here's dev mode.\n")
    dev = True

# If in dev mode use dev area for HV on dsg-c-linux1 and place holder system
# If running normally, use inputs from CSS script property of displace to get
# path where HV.hvc and HV.group files are and which detector tp display HV for.
if dev:
    dirr = '/home/tlemon/hv-css'
    toShow = 'HMS Hodo 1 X'
else:
    dirr = SU.PVUtil.getString(pvs[0])
    toShow = SU.PVUtil.getString(pvs[1])

#configuration files for .tcl files.
# For this program version, these files are both HMS and SHMS tcl/tk config
# files combined into one.
configFile,groupFile = dirr+'/HV.hvc',dirr+'/HV.group'

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
menuOptions = []
for i,grp in enumerate(groups):
    menuOptions.append([grp[1],grp[1].replace(' ','-')+'-list.opi'])
    for line in configLines:
        if line[0] != '#' and line[0] != '\n':
            group = line.strip().split(' ')[4]
            if group == grp[0]:
                groups[int(i)].append(line.strip().split(' ')[:4])

# if in dev mode, prints out channels groups and channel info.
# program stops at this point in dev mode.
if dev:
    for grp in groups:
        for item in grp:
            print(item)
        print(' ')
    sys.exit(0)


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

# Makes sure that the screens are in and stay in compact mode.
compact = SU.PVUtil.getDouble(pvs[2])
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

# Odd logic sequence to make sure creation of screen isn't looped constantly
# and old info is erased from screen when switching system.
# NOTE: this probably can be done better.
try:
    if last == toShow:
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

# pulls out group that matches toShow and creates table-format control screen.
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
        w.setPropertyValue('width',775)
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
            putChLabel(x,y,chID) # channel ID label
            putPowerButton(x+25+widgetWidth,y,pvBase+'Pw') #power button
            putIndicator(x+25+2*widgetWidth,y,pvBase+'Status') # status indic.
            putIndicator(x+25+3*widgetWidth,y,pvBase+'VMon')# voltage readback
            putIndicator(x+25+4*widgetWidth,y,pvBase+'IMon')# current readback
            putControl(x+25+5*widgetWidth,y,pvBase+'V0Set')# voltage set pt ctrl
            putControl(x+25+6*widgetWidth,y,pvBase+'I0Set')# current set pt ctrl
            putControl(x+25+7*widgetWidth,y,pvBase+'SVMax')# max voltage set pt
            putControl(x+25+8*widgetWidth,y,pvBase+'RUp')# ramp up rate ctrl
            putControl(x+25+9*widgetWidth,y,pvBase+'RDWn')# ramp down rate ctrl
            y += widgetHeight

# saves toShow as last, used to check whether screen to display has changed on
# next loop of progra,.
last = toShow

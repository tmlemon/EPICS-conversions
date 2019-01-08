#!/bin/env python

# 2018-12-18
# @author: Tyler Lemon
#
# Program uses HV.hvc and HV.group files to convert Hall C HV controls .tcl 
# screens to CS-Studio screens.
#
# SCRIPT REQUIRES "opiWidgets.py"  and "functions_tcl2css.py" IN SAME DIRECTORY
# AS SOURCE CODE TO RUN.

import sys
import os
import errno

# Tries to import opiWidgets.py. If file not found in same directory as source
# code for tcl2css.py, program prints error message and stops.
try:
	from opiWidgets import *
	from functions_tcl2css import *
except:
	print('\033[1m'+'\nERROR: opiWidgets.py not found in same directory as \
source code for tcl2css.py.'+'\033[0m')
	print('opiWidgets.py is required to run tcl2css.py.')
	print('Aborting execution of tcl2css.py.\n')
	sys.exit(0)

# Cases to check user's command line arguements.
if len(sys.argv)-1 == 1:
	dirr = checkForInput(sys.argv[1])
	outPath = ''
elif len(sys.argv)-1 == 2:
	dirr = checkForInput(sys.argv[1])
	outPath = sys.argv[2]
	if outPath[-1] != '/':
		outPath += '/'
	if not os.path.exists(outPath):
		try:
			os.makedirs(outPath)
		except OSError as err:
			if err.errno != errno.EEXIST:
				raise
else:
    print('\033[1m'+'\nINPUT ARGUEMENTS ERROR'+'\033[0m')
    print('\npython tcl2css.py dir [write]\n')
    print('dir\t- mandatory arguement for directory containing HV.hvc and ')
    print('\tHV.group used to make the CSS screens.\n')
    print('[write]\t- optional arguement for directory to write resulting ')
    print('\t.opi files to.\n')
    sys.exit(0)

#configuration files for .tcl files.
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


xSpacing = 10
ySpacing = 8
screenWidth = 850
labelHeight = buttonHeight = indicatorHeight = ledHeight = inputHeight = 20
labelWidth = 75
buttonWidth = ledWidth = 50
inputWidth = indicatorWidth = 68
horizDivLen = 760


channelProps = ['VMon','IMon','Status','V0Setr','Trip','SVMax','RUpr','RDWnr']
# Creates screens showing each group in table format.
vMon,iMon,allPVs = [],[],[]
for grp in groups:
	vMonHold,iMonHold,allPVsHold = [],[],[]
	grpNum,grpName,channels = grp[0],grp[1],grp[2:]
	fileName = grpName.replace(' ','-')
	x = y = 50
	x0,y0 = x,y
	#Fills out base screen properties.
	screen = []
	for line in screenTemplate:
		line = line.replace('OPI_NAME',fileName)
		line = line.replace('SCREEN_WIDTH',str(screenWidth))
		line = line.replace('SCREEN_HEIGHT',\
			str(2*y0+len(channels)*(labelHeight+ySpacing)))
		screen.append(line)
    #title label for table
	for line in label:
		line = line.replace('LABEL_HEIGHT',str(40))
		line = line.replace('LABEL_WIDTH',str(600))
		line = line.replace('LABEL_TEXT',grpName+' HV Controls')
		line = line.replace('LABEL_NAME',grpName+' HV Controls')
		line = line.replace('LABEL_Y_POS',str(5))
		line = line.replace('LABEL_X_POS',str((screenWidth/2)-300))
		line = line.replace('FONT_STYLE',str(1))
		line = line.replace('FONT_SIZE',str(14))
		screen.append(line)

	# Calls function to add dropdown menu to screen.
	screen =  makeMenu(menuOptions,grpName,spectrometer,screen)

	#Generates labels for table header.
	#For FONT_STYLE, 1 is bold, 0 regular
	headerContents = ['Ch ID','On/Off','Status','Vmon','Imon','Vset','Itrip',\
		'Vmax','RmpUp','RmpDwn']
	for part in headerContents:
		for line in label:
			line = line.replace('LABEL_HEIGHT',str(labelHeight))
			line = line.replace('LABEL_WIDTH',str(labelWidth))
			line = line.replace('LABEL_TEXT',part)
			line = line.replace('LABEL_NAME',part)
			line = line.replace('LABEL_Y_POS',str(y))
			line = line.replace('LABEL_X_POS',str(x))
			line = line.replace('FONT_STYLE',str(1))
			line = line.replace('FONT_SIZE',str(9))
			screen.append(line)
		x += labelWidth
	y += labelHeight+ySpacing
	#Places all widgets on the screens.
	for ch in channels:
		x = x0
		chID = ch[0]
		pvBase = 'hchv'+ch[1]+':'+ch[2].zfill(2)+':'+ch[3].zfill(3)+':'
		for prop in channelProps:
			allPVsHold.append(pvBase+prop)
		vMonHold.append(pvBase+'VMon')
		iMonHold.append(pvBase+'IMon')
		#Channel ID label
		for line in label:
			line = line.replace('LABEL_HEIGHT',str(labelHeight))
			line = line.replace('LABEL_WIDTH',str(labelWidth))
			line = line.replace('LABEL_TEXT',chID)
			line = line.replace('LABEL_NAME',chID)
			line = line.replace('LABEL_Y_POS',str(y))
			line = line.replace('LABEL_X_POS',str(x))
			line = line.replace('FONT_STYLE',str(0))
			line = line.replace('FONT_SIZE',str(9))
			screen.append(line)
		x += labelWidth
		#channel control button
		for	line in button:
			line = line.replace('BUTTON_HEIGHT',str(buttonHeight))
			line = line.replace('BUTTON_WIDTH',str(buttonWidth))
			line = line.replace('BUTTON_Y_POS',str(y))
			line = line.replace('BUTTON_X_POS',str(x+(labelWidth-\
				buttonWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'Status')
			screen.append(line)
		x += labelWidth
		#Channel on/off status indicator
		for	line in statusTextUpdate:
			line = line.replace('INDICATOR_HEIGHT',str(indicatorHeight))
			line = line.replace('INDICATOR_WIDTH',str(indicatorWidth))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',\
					str(x+(labelWidth-indicatorWidth)/2))
			line = line.replace('PV_NAME',pvBase+'Status')
			screen.append(line)
		x += labelWidth
		#Voltage readback
		for	line in textUpdate:
			line = line.replace('INDICATOR_HEIGHT',str(indicatorHeight))
			line = line.replace('INDICATOR_WIDTH',str(indicatorWidth))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',\
					str(x+(labelWidth-indicatorWidth)/2))
			line = line.replace('PV_NAME',pvBase+'VMon')
			screen.append(line)
		x += labelWidth
		#Current readback
		for	line in textUpdate:
			line = line.replace('INDICATOR_HEIGHT',str(indicatorHeight))
			line = line.replace('INDICATOR_WIDTH',str(indicatorWidth))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',\
					str(x+(labelWidth-indicatorWidth)/2))
			line = line.replace('PV_NAME',pvBase+'IMon')
			screen.append(line)
		x += labelWidth
		#Set voltage
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'V0Setr')
			screen.append(line)
		x += labelWidth
		#Current trip level
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'Trip')
			screen.append(line)
		x += labelWidth
		#Max allowable set voltage
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'SVMax')
			screen.append(line)
		x += labelWidth
		#Channel ramp up rate
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'RUpr')
			screen.append(line)
		x += labelWidth
		#channel ramp down rate
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME',pvBase)#+'RDWnr')
			screen.append(line)
		#horizontal divider line between channels.
		for line in lineFmt:
			line = line.replace('LINE_HEIGHT',str(1))
			line = line.replace('LINE_WIDTH',str(horizDivLen))
			line = line.replace('LINE_Y_POS',str(y-(ySpacing/2)))
			line = line.replace('LINE_X_POS',str(x0))
			line = line.replace('PT1_X',str(x0))
			line = line.replace('PT1_Y',str(y-(ySpacing/2)))
			line = line.replace('PT2_X',str(x0+horizDivLen))
			line = line.replace('PT2_Y',str(y-(ySpacing/2)))
			screen.append(line)
		y += labelHeight+ySpacing
	#appends group vMon and iMon PVs to overall list.
	vMon.append(vMonHold)	
	iMon.append(iMonHold)
	allPVs.append(allPVsHold)
	# Appends final line of OPI format and writes all lines to an OPI file with
	# the name of the group.
	screen.append(lastLine)
	writeFile(outPath,fileName+'-list.opi',screen)

for i,item in enumerate(menuOptions):
	screen = makeHistoPlot(item[0],vMon[i],iMon[i],menuOptions)
	writeFile(outPath,item[1][:-9]+'-plot.opi',screen)

screen = makeHistoPlot(spectrometer,flatten(vMon),flatten(iMon),menuOptions)
writeFile(outPath,spectrometer+'-plot.opi',screen)

import sys
import os
from opiWidgets import *

# Function to "flatten" a 2-D list of lists into a 1-D list.
flatten = lambda lst: [item for sublist in lst for item in sublist]


# Function checks user's first arguement for directory containing HV.hvc and 
# HV.group. If directory is invalid or does not contain HV.hvc and/or HV.group,
# an error message is printed and program stops.
def checkForInput(arg):
	try:
		files = os.listdir(arg)
	except:
		print('\033[1m'+'\n"'+arg+'" is not a valid directory.\n'+'\033[0m')
		sys.exit(0)
	if 'HV.hvc' not in files or 'HV.group' not in files:
		print('\n'+'\033[1m'+'HV.hvc and/or HV.group not found in "'+\
			arg+'"'+'\033[0m'+'\n')
		sys.exit(0)
		arg = ''
	return arg


#Makes dropdown menu
def makeMenu(menuOptions,grpName,spectrometer,screen):
	for line in menuStart:
		screen.append(line)
	for opt in menuOptions:
		if opt[0] == grpName:
			mode = '0'
		else:
			mode = '6'
		for line in menuOpt:
			line = line.replace('OPT_PATH',opt[1])
			line = line.replace('OPT_MODE',mode)
			line = line.replace('OPT_TITLE',opt[0])
			screen.append(line)
	for line in menuEnd:
		line = line.replace('SPCTRMTR',spectrometer)
		line = line.replace('X_POS',str(615))
		line = line.replace('Y_POS',str(10))
		screen.append(line)
	return screen


# Writes all lines of final file to a .OPI file
def makeScreen(outPath,fileName,screen):
	with open(outPath+fileName,'w') as f:
		for line in screen:
			f.write(line)
			f.write('\n')
	print(fileName+' created.')
	return 0


# Creates screen of Bar Plots for voltage and current monitoring
def makeHistoPlot(spectrometer,vMon,iMon,menuOptions):
	screen = []
	for line in screenTemplate:
		line = line.replace('OPI_NAME',spectrometer+'-HV-Monitor')
		line = line.replace('SCREEN_WIDTH',str(800))
		line = line.replace('SCREEN_HEIGHT',str(725))
		screen.append(line)
	#title label for plot screen
	for line in label:
		line = line.replace('LABEL_HEIGHT',str(40))
		line = line.replace('LABEL_WIDTH',str(600))
		line = line.replace('LABEL_TEXT',spectrometer+' HV Monitor')
		line = line.replace('LABEL_NAME',spectrometer+' HV Monitor')
		line = line.replace('LABEL_Y_POS',str(5))
		line = line.replace('LABEL_X_POS',str((800/2)-300))
		line = line.replace('FONT_STYLE',str(1))
		line = line.replace('FONT_SIZE',str(14))
		screen.append(line)
	#Creates bar plot for voltage monitoring
	for line in xyPlotStart:
		line = line.replace('Y_AXIS_LABEL','Volts')
		line = line.replace('HEIGHT',str(300))
		screen.append(line)
	for pv in vMon:
		screen.append(xyPlotChannelFmt.replace('INSERT_PV_HERE',pv))
	for line in xyPlotEnd:
		line = line.replace('NUMBER_OF_PVS',str(len(vMon)))
		line = line.replace('WIDTH',str(700))
		line = line.replace('X_POS',str(50))
		line = line.replace('Y_POS',str(75))
		screen.append(line)
	#Creates bar plot for current monitoring
	for line in xyPlotStart:
		line = line.replace('Y_AXIS_LABEL','nAmps')
		line = line.replace('HEIGHT',str(300))
		screen.append(line)
	for pv in iMon:
		screen.append(xyPlotChannelFmt.replace('INSERT_PV_HERE',pv))
	for line in xyPlotEnd:
		line = line.replace('NUMBER_OF_PVS',str(len(iMon)))
		line = line.replace('WIDTH',str(700))
		line = line.replace('X_POS',str(50))
		line = line.replace('Y_POS',str(400))
		screen.append(line)
	#Makes dropdown menu
	for line in menuStart:
		screen.append(line)
	for opt in menuOptions:
		for line in menuOpt:
			line = line.replace('OPT_PATH',opt[1])
			line = line.replace('OPT_MODE','6')
			line = line.replace('OPT_TITLE',opt[0])
			screen.append(line)
	for line in menuEnd:
		line = line.replace('SPCTRMTR',spectrometer)
		line = line.replace('X_POS',str(550))
		line = line.replace('Y_POS',str(10))
		screen.append(line)
	screen.append(lastLine)
	return screen

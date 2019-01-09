#!/bin/env python

import sys
import os.path

#Base properties for EDM screen.
edl = ['4 0 1','beginScreenProperties','major 4','minor 0',\
	'release 1','x 0','y 0','w WIDTH','h HEIGHT',\
	'font "helvetica-medium-r-18.0"','ctlFont "helvetica-medium-r-8.0"',\
	'btnFont "helvetica-medium-r-18.0"','fgColor index 14','bgColor index 4',\
	'textColor index 14','ctlFgColor1 index 30','ctlFgColor2 index 32',\
	'ctlBgColor1 index 34','ctlBgColor2 index 35','topShadowColor index 37',\
	'botShadowColor index 44','snapToGrid','gridSize 5','endScreenProperties\n']
#Static text (aka labels)
staticText = ['# (Static Text)','object activeXTextClass',\
	'beginObjectProperties','major 4','minor 1','release 1','x X_POS',\
	'y Y_POS','w WIDTH','h HEIGHT','font "helvetica-medium-r-FONT_SIZE"',\
	'fontAlign "ALIGN"','fgColor index 14','bgColor index 0','useDisplayBg',\
	'value {','  "LABEL_TEXT"','}','autoSize','endObjectProperties\n']
#Text monitor
textMonitor = ['# (Text Monitor)','object activeXTextDspClass:noedit',\
	'beginObjectProperties','major 4','minor 7','release 0','x X_POS',\
	'y Y_POS','w WIDTH','h HEIGHT','controlPv "PV_NAME"',\
	'font "helvetica-medium-r-FONT_SIZE"','fgColor index 14',\
	'bgColor index 51','topShadowColor index 50',\
	'botShadowColor index 10','useDisplayBg','autoHeight',\
	'limitsFromDb','nullColor index 14','useHexPrefix',\
	'newPos','objType "monitors"','endObjectProperties\n']
#Text update - the standard text indicator
textUpdate = ['# (Textupdate)','object TextupdateClass',\
	'beginObjectProperties','major 10','minor 0','release 0','x X_POS',\
	'y Y_POS','w WIDTH','h HEIGHT','controlPv "PV_NAME"',\
	'fgColor index 14','fgAlarm','bgColor index 51','fill',\
	'font "helvetica-medium-r-14.0"','endObjectProperties\n']

# function to check user's input arguement
def checkInput(arg):
	if os.path.isdir(arg):
		dirr = arg
		if arg[-1] != '/':
			dirr += '/'
		try:
			files = os.listdir(dirr)
		except:
			print('\033[1m'+'\n"'+arg+'" is not a valid directory.'+'\033[0m')
			print('First arguement must be a directory or file that exists')
			print('Use --help or -h option to print help info.\n')
			sys.exit(0)
	else:
		if os.path.isfile(arg) == False:
			print('\033[1m'+'\n"'+arg+'" is not a valid input.'+'\033[0m')
			print('First arguement must be a directory or file that exists')
			print('Use --help or -h option to print help info.\n')
			sys.exit(0)
		else:		
			dirr = ''
			files = [arg]
	return dirr,files

# Cases to check user's command line arguements.
if len(sys.argv)-1 == 1 and (sys.argv[1] != '--help' and sys.argv[1] != '-h'):
	dirr,files = checkInput(sys.argv[1])
	outPath = ''
elif len(sys.argv)-1 == 2:
	dirr,files = checkInput(sys.argv[1])
	outPath = sys.argv[2]
	if outPath == '.':
		outPath = os.getcwd()
	if outPath[-1] != '/':
		outPath += '/'
	if not os.path.exists(outPath):
		try:
			os.makedirs(outPath)
		except OSError as err:
			if err.errno != errno.EEXIST:
				raise
else:
	print('\033[1m'+'\nINPUT ARGUEMENTS HELP'+'\033[0m')
	print('\ncsv2edl in [write]\n')
	print('in\t- mandatory arguement for directory containing .csv')
	print('\tfiles or a .csv file to convert to EDM screen.')
	print('[write]\t- optional arguement for directory to write resulting ')
	print('\t.edl files to.\n')
	sys.exit(0)

# Removes any non-csv files from file list.
keep = []
for i,item in enumerate(files):
	if item[-4:] == '.csv':
		keep.append(item)
if len(keep) == 0:
	print('\033[1m'+'\nERROR: Input arguement is not a .csv file or is not a\
 directory\ncontaining .csv files.'+'\033[0m')
	print('As of this version, only conversion of .csv files are supported.\n')
	sys.exit(0)
files = keep


#prelimary constants for making .edl file
x = 20
y = 50
x0,y0 = x,y
xSpacing = 10
ySpacing = 5
labelIndicatorSpace = 5
labelWidth,labelHeight = 200,20
indicatorWidth, indicatorHeight = 100,20
unitsWidth,unitsHeight = 40,20

# Loops over all .csv files found as user's first input arguement.
for csv in files:
	#csv = sys.argv[1]
	edlFile = csv[:csv.find('.csv')]+'.edl'

	with open(dirr+csv,'r') as f:
		lines = f.readlines()

	final = []
	for prop in edl:
		prop = prop.replace('HEIGHT',str(2*y+len(lines)*(ySpacing+labelHeight)))
		prop = prop.replace('WIDTH',str(2*x+labelWidth+indicatorWidth+\
			unitsWidth+2*labelIndicatorSpace))
		final.append(prop)

	for line in lines:
		pv,label,units = line.strip().split(',')
		if '' in [pv,label,units]:
			y += (ySpacing + labelHeight)
		#pv label
		if label != '':
			for prop in staticText:
				prop = prop.replace('X_POS',str(x))
				prop = prop.replace('Y_POS',str(y))
				prop = prop.replace('WIDTH',str(labelWidth))
				prop = prop.replace('HEIGHT',str(labelHeight))
				prop = prop.replace('FONT_SIZE','14.0')
				prop = prop.replace('ALIGN',str('right'))
				prop = prop.replace('LABEL_TEXT',str(label))
				final.append(prop)
		#pv indicator
		if pv != '':
			for prop in textUpdate:
				prop = prop.replace('X_POS',str(x+labelWidth+labelIndicatorSpace))
				prop = prop.replace('Y_POS',str(y))
				prop = prop.replace('WIDTH',str(indicatorWidth))
				prop = prop.replace('HEIGHT',str(indicatorHeight))
				prop = prop.replace('FONT_SIZE','14.0')
				prop = prop.replace('PV_NAME',str(pv))
				final.append(prop)
		#units label
		if units != '':
			for prop in staticText:
				prop = prop.replace('X_POS',str(x+labelWidth+labelIndicatorSpace+\
					indicatorWidth+labelIndicatorSpace))
				prop = prop.replace('Y_POS',str(y))
				prop = prop.replace('WIDTH',str(unitsWidth))
				prop = prop.replace('HEIGHT',str(unitsHeight))
				prop = prop.replace('FONT_SIZE','14.0')
				prop = prop.replace('ALIGN',str('left'))
				prop = prop.replace('LABEL_TEXT',str(units))
				final.append(prop)
		y += (ySpacing + labelHeight)

	# Saves all resulting .edl files to user's output path arguement
	with open(outPath+edlFile,'w') as f:
		for line in final:
			f.write(line)
			f.write('\n')
	print(csv+' converted to '+edlFile)


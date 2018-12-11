#!/bin/env python

import sys
import os.path

wedmPath = '/cs/opshome/edm/hlc/spectrometers/'

#Base properties for EDM screen.
edl = ['4 0 1','beginScreenProperties','major 4','minor 0',\
	'release 1','x 0','y 0','w WIDTH','h HEIGHT',\
	'font "helvetica-medium-r-18.0"','ctlFont "helvetica-medium-r-8.0"',\
	'btnFont "helvetica-medium-r-18.0"','fgColor index 14','bgColor index 4',\
	'textColor index 14','ctlFgColor1 index 30','ctlFgColor2 index 32',\
	'ctlBgColor1 index 34','ctlBgColor2 index 35','topShadowColor index 37',\
	'botShadowColor index 44','snapToGrid','gridSize 5','endScreenProperties\n']

#Properties for EDM Graphics
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


if len(sys.argv) != 3:
	print('\nERROR\nEnter only one arguement for CSV file to convert to EDL.')
	print('python csv2edl.py <csv file / directory>\n')
	sys.exit(0)

if 'csv' not in sys.argv[1]:
	print('\nNon-CSV files entered into script.\n')
	sys.exit(0)

csv = sys.argv[1]
edlFile = csv[:csv.find('.csv')]+'.edl'

with open(csv,'r') as f:
	lines = f.readlines()

hold,groups = [],[]
for i,line in enumerate(lines):
	pv,label,units = line.strip().split(',')
	if label == '' and units == '':
		hold.append(i)

for i in range(1,len(hold)-1):
	groups.append(lines[hold[i-1]:hold[i]])

x = 20
y = 50
x0,y0 = x,y
xSpacing = 10
ySpacing = 5
labelIndicatorSpace = 5

labelWidth,labelHeight = 200,20
indicatorWidth, indicatorHeight = 100,20
unitsWidth,unitsHeight = 40,20

final = []
for prop in edl:
	prop = prop.replace('HEIGHT',str(2*y+len(lines)*(ySpacing+labelHeight)))
	prop = prop.replace('WIDTH',str(2*x+2*labelWidth+2*indicatorWidth+\
		2*unitsWidth+2*labelIndicatorSpace+xSpacing))
	final.append(prop)

for line in lines:
	pv,label,units = line.strip().split(',')
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

with open(edlFile,'w') as f:
	for line in final:
		f.write(line)
		f.write('\n')

print(csv+' converted to '+edlFile)


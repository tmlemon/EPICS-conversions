#!/bin/env python

import sys
import os
import math

#OPI text used to create text indicators and a label.
template = ['  <widget typeId="org.csstudio.opibuilder.widgets.Label" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <auto_size>false</auto_size>','    <background_color>',\
'      <color red="255" green="255" blue="255" />','    </background_color>',\
'    <border_color>','      <color red="0" green="128" blue="255" />',\
'    </border_color>','    <border_style>0</border_style>',\
'    <border_width>1</border_width>','    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="9" style="0" pixels="false" />',\
'    </font>', '    <foreground_color>',\
'      <color red="0" green="0" blue="0" />','    </foreground_color>',\
'    <height>20</height>','    <horizontal_alignment>2</horizontal_alignment>',\
'    <name>LABEL_NAME</name>','    <rules />','    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',
'      <keep_wh_ratio>false</keep_wh_ratio>','    </scale_options>',\
'    <scripts />','    <text>LABEL_TEXT</text>','    <tooltip></tooltip>',\
'    <transparent>true</transparent>',\
'    <vertical_alignment>1</vertical_alignment>','    <visible>true</visible>',\
'    <widget_type>Label</widget_type>','    <width>LABEL_WIDTH</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7737</wuid>','    <x>LABEL_X_POS</x>',\
'    <y>LABEL_Y_POS</y>','  </widget>',\
'  <widget typeId="org.csstudio.opibuilder.widgets.TextUpdate" version="1.0.0">',
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <auto_size>false</auto_size>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',
'    <background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </background_color>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>','      <color red="0" green="128" blue="255" />',\
'    </border_color>','    <border_style>0</border_style>',\
'    <border_width>1</border_width>','    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="10" style="0" pixels="false" />',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>','      <color red="0" green="0" blue="0" />',\
'    </foreground_color>','    <format_type>0</format_type>',\
'    <height>20</height>','    <horizontal_alignment>0</horizontal_alignment>',\
'    <name>INDICATOR_NAME</name>','    <precision>0</precision>',\
'    <precision_from_pv>true</precision_from_pv>',\
'    <pv_name>PV_NAME</pv_name>','    <pv_value />',\
'    <rotation_angle>0.0</rotation_angle>','    <rules />',\
'    <scale_options>','      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>','    <scripts />','    <show_units>true</show_units>',\
'    <text>######</text>','    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>','    <transparent>false</transparent>',\
'    <vertical_alignment>1</vertical_alignment>','    <visible>true</visible>',\
'    <widget_type>Text Update</widget_type>',\
'    <width>INDICATOR_WIDTH</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7711</wuid>','    <x>INDICATOR_X_POS</x>',\
'    <y>INDICATOR_Y_POS</y>', '  </widget>',
'  <widget typeId="org.csstudio.opibuilder.widgets.Label" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <auto_size>false</auto_size>','    <background_color>',\
'      <color red="255" green="255" blue="255" />','    </background_color>',\
'    <border_color>','      <color red="0" green="128" blue="255" />',\
'    </border_color>','    <border_style>0</border_style>',\
'    <border_width>1</border_width>','    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="9" style="0" pixels="false" />',\
'    </font>', '    <foreground_color>',\
'      <color red="0" green="0" blue="0" />','    </foreground_color>',\
'    <height>20</height>','    <horizontal_alignment>2</horizontal_alignment>',\
'    <name>UNITS</name>','    <rules />','    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',
'      <keep_wh_ratio>false</keep_wh_ratio>','    </scale_options>',\
'    <scripts />','    <text>UNITS</text>','    <tooltip></tooltip>',\
'    <transparent>true</transparent>',\
'    <vertical_alignment>1</vertical_alignment>','    <visible>true</visible>',\
'    <widget_type>Label</widget_type>','    <width>30</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7737</wuid>','    <x>UNITS_X_POS</x>',\
'    <y>UNITS_Y_POS</y>','  </widget>']

# Base formatting of an OPI in text. Each list element is a different line
# of the final OPI file.
base = ['<display typeId="org.csstudio.opibuilder.Display" version="1.0.0">',\
'  <actions hook="false" hook_all="false" />','  <auto_scale_widgets>',\
'    <auto_scale_widgets>false</auto_scale_widgets>',\
'    <min_width>-1</min_width>','    <min_height>-1</min_height>',\
'  </auto_scale_widgets>',\
'  <auto_zoom_to_fit_all>false</auto_zoom_to_fit_all>',\
'  <background_color>','    <color red="240" green="240" blue="240" />',\
'  </background_color>','  <boy_version>5.1.0.201707071649</boy_version>',\
'  <foreground_color>','    <color red="192" green="192" blue="192" />',\
'  </foreground_color>','  <grid_space>6</grid_space>',\
'  <height>600</height>','  <macros>',\
'    <include_parent_macros>true</include_parent_macros>','  </macros>',\
'  <name>OPI_NAME</name>','  <rules />','  <scripts />',\
'  <show_close_button>true</show_close_button>',\
'  <show_edit_range>true</show_edit_range>',\
'  <show_grid>true</show_grid>','  <show_ruler>true</show_ruler>',\
'  <snap_to_geometry>true</snap_to_geometry>',\
'  <widget_type>Display</widget_type>','  <width>800</width>',\
'  <wuid>54b97197:16750d3dd5b:-7755</wuid>','  <x>-1</x>','  <y>-1</y>']

#The last line of the text OPI needs to be this.
lastLine = '</display>'







# Checks users arguements and prints help message if needed.
if (('-h' in sys.argv) == True or ('--help' in sys.argv) == True):
	print('\nUsage: python make-base-opi.py <PV txt file or directory> \
<number of columns>')
	print('\nText file containing PVs should have each row with the format:')
	print('PV-name	Label-contents\n')
	sys.exit(0)
elif len(sys.argv) != 3:
	print('\nERROR: Only arguments needed:\n1. path and file name of PV \
list or directory containing lists.\n2. number of columns to arrange PVs in.')
	print('python make-base-opi.py <txt file or directory> \
<number of columns>\n')
	print('Use -h or --help for more help.\n')
	sys.exit(0)


files = []
if os.path.isdir(sys.argv[1]):
	for f in os.listdir(sys.argv[1]):
		if sys.argv[1].strip()[-1:] == '/':
			files.append(sys.argv[1]+f)
		else:
			files.append(sys.argv[1]+'/'+f)
else:
	files.append(sys.argv[1])

for txt in files:
	outFile = txt[txt.rfind('/')+1:txt.rfind('.')]+'.opi'

	# Sets name of OPI in its file to user input
	opi = []
	for line in base:
		line = line.replace('OPI_NAME',str(sys.argv[1]))
		opi.append(line)

	with open(txt,'r') as f:
		userInput = f.readlines()

	colNum = float(sys.argv[2])
	pvNum = len(userInput)
	pvPerCol = math.ceil(pvNum/colNum)
	
# Constants to allow easier changing of label and indicator width and spacing
# between widgets.
	LABEL_WIDTH = 175
	INDICATOR_WIDTH = 100

	x,y = 10,50
	xSpacing,ySpacing = 10,25
	labelIndicatorGap = 5

# Programatically generates OPI text file using data from text file that was
# user's first arguement.
	x0,y0 = x,y
	count = 0
	for pv in userInput:
		if count >= pvPerCol:
			x += x0+LABEL_WIDTH+labelIndicatorGap+INDICATOR_WIDTH+xSpacing
			y = y0
			count = 0
		count += 1
		PV_NAME,LABEL_TEXT,UNITS = pv.strip().split('\t')
		for line in template:
			line = line.replace('LABEL_X_POS',str(x))
			line = line.replace('LABEL_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',str(x+LABEL_WIDTH+\
					labelIndicatorGap))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('UNITS_X_POS',str(x+LABEL_WIDTH+\
					labelIndicatorGap+INDICATOR_WIDTH+labelIndicatorGap))
			line = line.replace('UNITS_Y_POS',str(y))
			line = line.replace('PV_NAME',str(PV_NAME))
			line = line.replace('LABEL_TEXT',str(LABEL_TEXT))
			line = line.replace('INDICATOR_NAME',str(PV_NAME))
			line = line.replace('LABEL_NAME',str(LABEL_TEXT))
			line = line.replace('LABEL_WIDTH',str(LABEL_WIDTH))
			line = line.replace('INDICATOR_WIDTH',str(INDICATOR_WIDTH))
			line = line.replace('UNITS',str(UNITS))
			opi.append(line)
		y += ySpacing
	opi.append(lastLine)


# Writes all lines programatically generated to an OPI file of the same name as
# the user's second argument.
	with open(outFile,'w') as f:
		for line in opi:
			f.write(line)
			f.write('\n')
# Prints message on completion stating file name of end result.
	print('OPI File Generated: '+outFile)
print('')


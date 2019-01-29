#!/bin/env python

###
### split out ability to generate alhConfig separately.
###

# 2018-12-18
# @author: Tyler Lemon
#
# Program uses HV.hvc and HV.group files to convert Hall C HV controls TCL/TK 
# screens to CS-Studio screens.
# Program also allows for user to generate group_map, channel_map and alhConfig
# files.

import sys #used to read in user arguements and exit program on errors.
import os # used to check files required for program.
import errno # used to catch potential error condition when creating parent 
	# directories for output file locations.
import array
from math import ceil
from datetime import datetime


# Base formatting of an OPI screen in text.
screenTemplate = [\
'<display typeId="org.csstudio.opibuilder.Display" version="1.0.0">',\
'  <actions hook="false" hook_all="false" />',\
'  <auto_scale_widgets>',\
'    <auto_scale_widgets>false</auto_scale_widgets>',\
'    <min_width>-1</min_width>',\
'    <min_height>-1</min_height>',\
'  </auto_scale_widgets>',\
'  <auto_zoom_to_fit_all>false</auto_zoom_to_fit_all>',\
'  <background_color>',\
'    <color red="240" green="240" blue="240" />',\
'  </background_color>',\
'  <boy_version>5.1.0.201707071649</boy_version>',\
'  <foreground_color>',\
'    <color red="192" green="192" blue="192" />',\
'  </foreground_color>',\
'  <grid_space>6</grid_space>',\
'  <height>SCREEN_HEIGHT</height>',\
'  <macros>',\
'    <include_parent_macros>true</include_parent_macros>',\
'  </macros>',\
'  <name>OPI_NAME</name>',\
'  <rules />',\
'  <scripts />',\
'  <show_close_button>true</show_close_button>',\
'  <show_edit_range>true</show_edit_range>',\
'  <show_grid>true</show_grid>',\
'  <show_ruler>true</show_ruler>',\
'  <snap_to_geometry>true</snap_to_geometry>',\
'  <widget_type>Display</widget_type>',\
'  <width>SCREEN_WIDTH</width>',\
'  <wuid>54b97197:16750d3dd5b:-7755</wuid>',\
'  <x>-1</x>',\
'  <y>-1</y>']

#The last line of the text OPI needs to be this.
lastLine = '</display>'

#OPI formatting for text updates
textUpdate = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.TextUpdate" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <auto_size>false</auto_size>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </background_color>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </border_color>',\
'    <border_style>1</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="10" style="0" pixels="false" />',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <format_type>0</format_type>',\
'    <height>INDICATOR_HEIGHT</height>',\
'    <horizontal_alignment>0</horizontal_alignment>',\
'    <name>INDICATOR_NAME</name>',\
'    <precision>0</precision>',\
'    <precision_from_pv>true</precision_from_pv>',\
'    <pv_name>PV_NAME</pv_name>',\
'    <pv_value />',\
'    <rotation_angle>0.0</rotation_angle>',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_units>true</show_units>',\
'    <text>######</text>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <transparent>false</transparent>',\
'    <vertical_alignment>1</vertical_alignment>',\
'    <visible>true</visible>',\
'    <widget_type>Text Update</widget_type>',\
'    <width>INDICATOR_WIDTH</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7711</wuid>',\
'    <x>INDICATOR_X_POS</x>',\
'    <y>INDICATOR_Y_POS</y>',\
'  </widget>']

#OPI formatting for text labels
label = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.Label" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <auto_size>false</auto_size>',\
'    <background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </background_color>',\
'    <border_color>',\
'      <color red="0" green="128" blue="255" />',\
'    </border_color>',\
'    <border_style>0</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="FONT_SIZE" style="FONT_STYLE" \
pixels="false" />',\
'    </font>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <height>LABEL_HEIGHT</height>',\
'    <horizontal_alignment>1</horizontal_alignment>',\
'    <name>LABEL_NAME</name>',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <text>LABEL_TEXT</text>',\
'    <tooltip></tooltip>',\
'    <transparent>true</transparent>',\
'    <vertical_alignment>1</vertical_alignment>',\
'    <visible>true</visible>',\
'    <widget_type>Label</widget_type>',\
'    <width>LABEL_WIDTH</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7737</wuid>',\
'    <x>LABEL_X_POS</x>',\
'    <y>LABEL_Y_POS</y>',\
'  </widget>']

#OPI format for a square LED indicator
led = [\
'<widget typeId="org.csstudio.opibuilder.widgets.LED" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="240" green="240" blue="240" />',\
'    </background_color>',\
'    <bit>-1</bit>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="128" blue="255" />',\
'    </border_color>',\
'    <border_style>0</border_style>',\
'    <border_width>1</border_width>',\
'    <bulb_border>3</bulb_border>',\
'    <bulb_border_color>',\
'      <color red="150" green="150" blue="150" />',\
'    </bulb_border_color>',\
'    <data_type>0</data_type>',\
'    <effect_3d>true</effect_3d>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <opifont.name> fontName="Cantarell" height="11" style="0",\
 pixels="false">Default</opifont.name>',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <height>LED_HEIGHT</height>',\
'    <name>LED</name>',\
'    <off_color>',\
'      <color name="Major" red="255" green="0" blue="0" />',\
'    </off_color>',\
'    <off_label>OFF</off_label>',\
'    <on_color>',\
'      <color red="0" green="255" blue="0" />',\
'    </on_color>',\
'    <on_label>ON</on_label>',\
'    <pv_name>PV_NAME</pv_name>',\
'    <pv_value />',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>true</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_boolean_label>true</show_boolean_label>',\
'    <square_led>true</square_led>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <visible>true</visible>',\
'    <widget_type>LED</widget_type>',\
'    <width>LED_WIDTH</width>',\
'    <wuid>7ef955a:167a9382857:-7e04</wuid>',\
'    <x>LED_X_POS</x>',\
'    <y>LED_Y_POS</y>',\
'  </widget>']

#OPI format for a Boolean button.
#Button has an attached rule to color it red when off and green when on.
button = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.BoolButton" \
version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="240" green="240" blue="240" />',\
'    </background_color>',\
'    <bit>-1</bit>',\
'    <border_alarm_sensitive>false</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </border_color>',\
'    <border_style>1</border_style>',\
'    <border_width>1</border_width>',\
'    <confirm_message>Are your sure you want to do this?</confirm_message>',\
'    <data_type>0</data_type>',\
'    <effect_3d>true</effect_3d>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="" height="7" style="1" pixels="false" />',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <height>BUTTON_HEIGHT</height>',\
'    <labels_from_pv>false</labels_from_pv>',\
'    <name>temp enable 1</name>',\
'    <off_color>',\
'      <color red="0" green="100" blue="0" />',\
'    </off_color>',\
'    <off_label>OFF</off_label>',\
'    <on_color>',\
'      <color red="0" green="255" blue="0" />',\
'    </on_color>',\
'    <on_label>ON</on_label>',\
'    <password></password>',\
'    <push_action_index>0</push_action_index>',\
'    <pv_name>PV_NAME</pv_name>',\
'    <pv_value />',\
'    <released_action_index>0</released_action_index>',\
'    <rules>',\
'      <rule name="color_toggle" prop_id="background_color" out_exp="false">',\
'        <exp bool_exp="PVUtil.getDouble(pvs[0]) == 0">',\
'          <value>',\
'            <color red="255" green="0" blue="0" />',\
'          </value>',\
'        </exp>',\
'        <exp bool_exp="PVUtil.getDouble(pvs[0]) == 1">',\
'          <value>',\
'            <color red="0" green="255" blue="0" />',\
'          </value>',\
'        </exp>',\
'        <pv trig="true">$(pv_name)</pv>',\
'      </rule>',\
'    </rules>',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_boolean_label>true</show_boolean_label>',\
'    <show_confirm_dialog>0</show_confirm_dialog>',\
'    <show_led>false</show_led>',\
'    <square_button>true</square_button>',\
'    <toggle_button>true</toggle_button>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <visible>true</visible>',\
'    <widget_type>Boolean Button</widget_type>',\
'    <width>BUTTON_WIDTH</width>',\
'    <wuid>7ef955a:167a9382857:-7b6b</wuid>',\
'    <x>BUTTON_X_POS</x>',\
'    <y>BUTTON_Y_POS</y>',\
'  </widget>']

#OPI format for a text input control
textInput = [\
'<widget typeId="org.csstudio.opibuilder.widgets.TextInput" version="2.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <auto_size>false</auto_size>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </background_color>',\
'    <border_alarm_sensitive>false</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </border_color>',\
'    <border_style>2</border_style>',\
'    <border_width>1</border_width>',\
'    <confirm_message></confirm_message>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\
 pixels="false">Default</opifont.name>',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <format_type>0</format_type>',\
'    <height>INPUT_HEIGHT</height>',\
'    <horizontal_alignment>0</horizontal_alignment>',\
'    <limits_from_pv>false</limits_from_pv>',\
'    <maximum>Infinity</maximum>',\
'    <minimum>-Infinity</minimum>',\
'    <multiline_input>false</multiline_input>',\
'    <name>Text Input</name>',\
'    <precision>0</precision>',\
'    <precision_from_pv>true</precision_from_pv>',\
'    <pv_name>PV_NAME</pv_name>',\
'    <pv_value />',\
'    <rotation_angle>0.0</rotation_angle>',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <selector_type>0</selector_type>',\
'    <show_units>true</show_units>',\
'    <style>0</style>',\
'    <text></text>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <transparent>false</transparent>',\
'    <visible>true</visible>',\
'    <widget_type>Text Input</widget_type>',\
'    <width>INPUT_WIDTH</width>',\
'    <wuid>7ef955a:167a9382857:-7b1c</wuid>',\
'    <x>INPUT_X_POS</x>',\
'    <y>INPUT_Y_POS</y>',\
'  </widget>']

#OPI format for line graphic used as divider between rows
lineFmt = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.polyline" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <alpha>255</alpha>',\
'    <anti_alias>true</anti_alias>',\
'    <arrow_length>20</arrow_length>',\
'    <arrows>0</arrows>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </background_color>',\
'    <border_alarm_sensitive>false</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="128" blue="255" />',\
'    </border_color>',\
'    <border_style>0</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <fill_arrow>true</fill_arrow>',\
'    <fill_level>0.0</fill_level>',\
'    <font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\
 pixels="false">Default</opifont.name>',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <height>1</height>',\
'    <horizontal_fill>true</horizontal_fill>',\
'    <line_style>0</line_style>',\
'    <line_width>1</line_width>',\
'    <name>Polyline</name>',\
'    <points>',\
'      <point x="PT1_X" y="PT1_Y" />',\
'      <point x="PT2_X" y="PT2_Y" />',\
'    </points>',\
'    <pv_name></pv_name>',\
'    <pv_value />',\
'    <rotation_angle>0.0</rotation_angle>',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>true</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <transparent>false</transparent>',\
'    <visible>true</visible>',\
'    <widget_type>Polyline</widget_type>',\
'    <width>LINE_WIDTH</width>',\
'    <wuid>783f697f:167ad6c54db:-72ed</wuid>',\
'    <x>LINE_X_POS</x>',\
'    <y>LINE_Y_POS</y>',\
'  </widget>']

# Start of OPI format for xy plot.
xyPlotStart = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.xyGraph" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <axis_0_auto_scale>true</axis_0_auto_scale>',\
'    <axis_0_auto_scale_threshold>0.0</axis_0_auto_scale_threshold>',\
'    <axis_0_axis_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </axis_0_axis_color>',\
'    <axis_0_axis_title>Channel</axis_0_axis_title>',\
'    <axis_0_dash_grid_line>true</axis_0_dash_grid_line>',\
'    <axis_0_grid_color>',\
'      <color red="200" green="200" blue="200" />',\
'    </axis_0_grid_color>',\
'    <axis_0_log_scale>false</axis_0_log_scale>',\
'    <axis_0_maximum>10.0</axis_0_maximum>',\
'    <axis_0_minimum>0.0</axis_0_minimum>',\
'    <axis_0_scale_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\
 pixels="false">Default</opifont.name>',\
'    </axis_0_scale_font>',\
'    <axis_0_scale_format></axis_0_scale_format>',\
'    <axis_0_show_grid>true</axis_0_show_grid>',\
'    <axis_0_time_format>0</axis_0_time_format>',\
'    <axis_0_title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1" pixels="false">Default Bold</opifont.name>',\
'    </axis_0_title_font>',\
'    <axis_0_visible>true</axis_0_visible>',\
'    <axis_1_auto_scale>false</axis_1_auto_scale>',\
'    <axis_1_auto_scale_threshold>0.0</axis_1_auto_scale_threshold>',\
'    <axis_1_axis_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </axis_1_axis_color>',\
'    <axis_1_axis_title>Y_AXIS_LABEL</axis_1_axis_title>',\
'    <axis_1_dash_grid_line>true</axis_1_dash_grid_line>',\
'    <axis_1_grid_color>',\
'      <color red="200" green="200" blue="200" />',\
'    </axis_1_grid_color>',\
'    <axis_1_log_scale>false</axis_1_log_scale>',\
'    <axis_1_maximum>2500.0</axis_1_maximum>',\
'    <axis_1_minimum>0.0</axis_1_minimum>',\
'    <axis_1_scale_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0" pixels="false">Default</opifont.name>',\
'    </axis_1_scale_font>',\
'    <axis_1_scale_format></axis_1_scale_format>',\
'    <axis_1_show_grid>true</axis_1_show_grid>',\
'    <axis_1_time_format>0</axis_1_time_format>',\
'    <axis_1_title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1" pixels="false">Default Bold</opifont.name>',\
'    </axis_1_title_font>',\
'    <axis_1_viIs hv_map.perl a script that is run independently from hv.tcl? Should the Python equivalent be able to be run without sible>true</axis_1_visible>',\
'    <axis_count>2</axis_count>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="240" green="240" blue="240" />',\
'    </background_color>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </border_color>',\
'    <border_style>1</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="255" />',\
'    </foreground_color>',\
'    <height>HEIGHT</height>',\
'    <name>XY Graph</name>',\
'    <plot_area_background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </plot_area_background_color>',\
'    <pv_name>loc://Plot</pv_name>',\
'    <pv_value />',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts>',\
'      <path pathString="EmbeddedPy" checkConnect="true" sfe="false" \
seoe="false">',\
'        <scriptName>build-array</scriptName>',\
'        <scriptText><![CDATA[from org.csstudio.opibuilder.scriptUtil \
import PVUtil',\
'from array import array',\
'arr = array("f")',\
'for pv in pvs[1:]:',\
'	try:',\
'		val = PVUtil.getDouble(pv)',\
'		if val != "":',\
'			arr.append(PVUtil.getDouble(pv))',\
'		else:',\
'			arr.append(0)',\
'	except:',\
'		arr.append(0)',\
'pvs[0].setValue(arr)]]></scriptText>',\
'        <pv trig="false">$(pv_name)</pv>']

# Line that is added to XY Plot Widget for every PV to be displayed.
xyPlotChannelFmt = '        <pv trig="true">INSERT_PV_HERE</pv>'

# End of OPI format for xy plot.
xyPlotEnd = [\
'      </path>',\
'    </scripts>',\
'    <show_legend>false</show_legend>',\
'    <show_plot_area_border>false</show_plot_area_border>',\
'    <show_toolbar>false</show_toolbar>',\
'    <title></title>',\
'    <title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1"\
 pixels="false">Default Bold</opifont.name>',\
'    </title_font>',\
'    <tooltip>$(trace_0_y_pv)',\
'$(trace_0_y_pv_value)</tooltip>',\
'    <trace_0_anti_alias>true</trace_0_anti_alias>',\
'    <trace_0_buffer_size>400</trace_0_buffer_size>',\
'    <trace_0_concatenate_data>false</trace_0_concatenate_data>',\
'    <trace_0_line_width>4</trace_0_line_width>',\
'    <trace_0_name>$(trace_0_y_pv)</trace_0_name>',\
'    <trace_0_plot_mode>0</trace_0_plot_mode>',\
'    <trace_0_point_size>4</trace_0_point_size>',\
'    <trace_0_point_style>0</trace_0_point_style>',\
'    <trace_0_trace_color>',\
'      <color red="21" green="21" blue="196" />',\
'    </trace_0_trace_color>',\
'    <trace_0_trace_type>3</trace_0_trace_type>',\
'    <trace_0_update_delay>100</trace_0_update_delay>',\
'    <trace_0_update_mode>0</trace_0_update_mode>',\
'    <trace_0_visible>true</trace_0_visible>',\
'    <trace_0_x_axis_index>0</trace_0_x_axis_index>,'\
'    <trace_0_x_pv></trace_0_x_pv>',\
'    <trace_0_x_pv_value />',\
'    <trace_0_y_axis_index>1</trace_0_y_axis_index>',\
'    <trace_0_y_pv>$(pv_name)</trace_0_y_pv>',\
'    <trace_0_y_pv_value />',\
'    <trace_count>1</trace_count>',\
'    <transparent>false</transparent>',\
'    <trigger_pv></trigger_pv>',\
'    <trigger_pv_value />',\
'    <visible>true</visible>',\
'    <widget_type>XY Graph</widget_type>',\
'    <width>WIDTH</width>',\
'    <wuid>1836fa4c:167bd64aba4:-7fdb</wuid>',\
'    <x>X_POS</x>',\
'    <y>Y_POS</y>',\
'  </widget>']

menuStart = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.MenuButton" \
version="1.0.0">',\
'    <actions hook="false" hook_all="false">']

menuOpt = [\
'      <action type="OPEN_DISPLAY">',\
'        <path>OPT_PATH</path>',\
'        <macros>',\
'          <include_parent_macros>true</include_parent_macros>',\
'        </macros>',\
'        <mode>OPT_MODE</mode>',\
'        <description>OPT_TITLE</description>',\
'      </action>']

menuEnd = [\
'    </actions>',\
'    <actions_from_pv>false</actions_from_pv>',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="240" green="240" blue="240" />',\
'    </background_color>',\
'    <border_alarm_sensitive>false</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="128" blue="255" />',\
'    </border_color>',\
'    <border_style>6</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\
 pixels="false">Default</opifont.name>',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <height>25</height>',\
'    <label>SPCTRMTR Detector HV Controls</label>',\
'    <name>Menu Button</name>',\
'    <pv_name></pv_name>',\
'    <pv_value />',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_down_arrow>true</show_down_arrow>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <transparent>false</transparent>',\
'    <visible>true</visible>',\
'    <widget_type>Menu Button</widget_type>',\
'    <width>225</width>',\
'    <wuid>-6af80d88:167c7f66d30:-6d81</wuid>',\
'    <x>X_POS</x>',\
'    <y>Y_POS</y>',\
'  </widget>']

#OPI formatting for text updates= for status readback
statusTextUpdate = [\
'  <widget typeId="org.csstudio.opibuilder.widgets.TextUpdate" version="1.0.0">',\
'    <actions hook="false" hook_all="false" />',\
'    <alarm_pulsing>false</alarm_pulsing>',\
'    <auto_size>false</auto_size>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </background_color>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </border_color>',\
'    <border_style>1</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <font>',\
'      <fontdata fontName="Sans" height="10" style="0" pixels="false" />',\
'    </font>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="0" />',\
'    </foreground_color>',\
'    <format_type>0</format_type>',\
'    <height>INDICATOR_HEIGHT</height>',\
'    <horizontal_alignment>0</horizontal_alignment>',\
'    <name>INDICATOR_NAME</name>',\
'    <precision>0</precision>',\
'    <precision_from_pv>true</precision_from_pv>',\
'    <pv_name>PV_NAME</pv_name>',\
'    <pv_value />',\
'    <rotation_angle>0.0</rotation_angle>',\
'    <rules>',\
'      <rule name="status-Rule" prop_id="background_color" out_exp="false">',\
'        <exp bool_exp="PVUtil.getString(pvs[0]) == &quot;ON&quot;">',\
'          <value>',\
'            <color red="0" green="255" blue="0" />',\
'          </value>',\
'        </exp>',\
'        <exp bool_exp="PVUtil.getString(pvs[0]) == &quot;OFF&quot;">',\
'          <value>',\
'            <color red="35" green="92" blue="35" />',\
'          </value>',\
'        </exp>',\
'        <exp bool_exp="PVUtil.getString(pvs[0]) == &quot;TRIPPED&quot;">',\
'          <value>',\
'            <color red="255" green="0" blue="0" />',\
'          </value>',\
'        </exp>',\
'        <pv trig="true">$(pv_name)</pv>',\
'      </rule>',\
'    </rules>',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_units>true</show_units>',\
'    <text>######</text>',\
'    <tooltip>$(pv_name)',\
'$(pv_value)</tooltip>',\
'    <transparent>false</transparent>',\
'    <vertical_alignment>1</vertical_alignment>',\
'    <visible>true</visible>',\
'    <widget_type>Text Update</widget_type>',\
'    <width>INDICATOR_WIDTH</width>',\
'    <wrap_words>false</wrap_words>',\
'    <wuid>54b97197:16750d3dd5b:-7711</wuid>',\
'    <x>INDICATOR_X_POS</x>',\
'    <y>INDICATOR_Y_POS</y>',\
'  </widget>']

# Function to "flatten" a 2-D list of lists into a 1-D list.
flatten = lambda lst: [item for sublist in lst for item in sublist]

# Function checks user's first arguement for directory containing HV.hvc and 
# HV.group. If directory is invalid or does not contain HV.hvc and/or HV.group,
# an error message is printed and program stops.
def checkForInput(arg):
	try:
		files = os.listdir(arg)
	except:
		print('\033[1m'+'\n"'+arg+'" is not a valid directory.'+'\033[0m')
		print('First arguement must be a directory that exists')
		print('Use --help or -h option to print help info.\n')
		sys.exit(0)
	if 'HV.hvc' not in files or 'HV.group' not in files:
		print('\n'+'\033[1m'+'HV.hvc and/or HV.group not found in "'+\
			arg+'"'+'\033[0m')
		print('First arguement must be directory that contains both \
HV.hvc and HV.group.')
		print('Use --help or -h option to print help info.\n')
		sys.exit(0)
		arg = ''
	return arg

# function makes dropdown menu for screens
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
def writeFile(outPath,fileName,screen):
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
		
prefix,spec = 'HV','Hall C'
mapOut = False
cssOut = True
alhOnly = False

if '-m' in sys.argv:
	mapOut = True
	if len(sys.argv)-2 == 1:
		dirr = checkForInput(sys.argv[2])
		outPath = ''
	elif len(sys.argv)-2 == 2:
		dirr = checkForInput(sys.argv[2])
		outPath = sys.argv[3]
		if outPath[-1] != '/':
			outPath += '/'
		if not os.path.exists(outPath):
			try:
				os.makedirs(outPath)
			except OSError as err:
				if err.errno != errno.EEXIST:
					raise
	elif len(sys.argv)-1 == 1:
		cssOut = False
		dirr,outPath = '',''
	else:
		print('\033[1m'+'\nINPUT ARGUEMENTS HELP'+'\033[0m')
		print('\npython tcl2css.py [-m] [-a] dir [write]\n')
		print('[-m]\t-optional argument to output channel_map, group_map, and') 
		print('\tHV.alhConfig.\n')
		print('[-a]\t-optional argument to output only HV.alhConfig.\n')
		print('dir\t- mandatory arguement for directory containing HV.hvc and ')
		print('\tHV.group used to make the CSS screens.\n')
		print('[write]\t- optional arguement for directory to write resulting ')
		print('\t.opi files to.\n')
		sys.exit(0)
elif '-a' in sys.argv and len(sys.argv)-1==1:
	alhOnly = True
	mapOut = True
	cssOut = False
	dirr,outPath = '',''
	print('HV.alhConfig generated.')
else:
	if len(sys.argv)-1 == 1 and ('--help' not in sys.argv and \
	'-h' not in sys.argv):
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
		print('\033[1m'+'\nINPUT ARGUEMENTS HELP'+'\033[0m')
		print('\npython tcl2css.py [-m] [-a] dir [write]\n')
		print('[-m]\t-optional argument to output channel_map, group_map, and') 
		print('\tHV.alhConfig.\n')
		print('[-a]\t-optional argument to output only HV.alhConfig.\n')
		print('dir\t- mandatory arguement for directory containing HV.hvc and ')
		print('\tHV.group used to make the CSS screens.\n')
		print('[write]\t- optional arguement for directory to write resulting ')
		print('\t.opi files to.\n')
		sys.exit(0)

#configuration files for .tcl files.
configFile,groupFile = dirr+'/HV.hvc',dirr+'/HV.group'

if cssOut == True:
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
	
	
	# Constants for widget placement on CSS screens.
	xSpacing = 10
	ySpacing = 8
	screenWidth = 850
	labelHeight = buttonHeight = indicatorHeight = ledHeight = inputHeight = 20
	labelWidth = 75
	buttonWidth = ledWidth = 50
	inputWidth = indicatorWidth = 68
	horizDivLen = 760


	channelProps = ['VMon','IMon','Status','V0Setr','Trip','SVMax',\
		'RUpr','RDWnr']
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
		headerContents = ['Ch ID','On/Off','Status','Vmon','Imon','Vset',\
			'Itrip','Vmax','RmpUp','RmpDwn']
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
				line = line.replace('INPUT_X_POS',str(x+(labelWidth-\
					inputWidth)/2))
				line = line.replace('PV_NAME',pvBase)#+'V0Setr')
				screen.append(line)
			x += labelWidth
			#Current trip level
			for	line in textInput:
				line = line.replace('INPUT_HEIGHT',str(inputHeight))
				line = line.replace('INPUT_WIDTH',str(inputWidth))
				line = line.replace('INPUT_Y_POS',str(y))
				line = line.replace('INPUT_X_POS',str(x+(labelWidth-\
					inputWidth)/2))
				line = line.replace('PV_NAME',pvBase)#+'Trip')
				screen.append(line)
			x += labelWidth
			#Max allowable set voltage
			for	line in textInput:
				line = line.replace('INPUT_HEIGHT',str(inputHeight))
				line = line.replace('INPUT_WIDTH',str(inputWidth))
				line = line.replace('INPUT_Y_POS',str(y))
				line = line.replace('INPUT_X_POS',str(x+(labelWidth-\
					inputWidth)/2))
				line = line.replace('PV_NAME',pvBase)#+'SVMax')
				screen.append(line)
			x += labelWidth
			#Channel ramp up rate
			for	line in textInput:
				line = line.replace('INPUT_HEIGHT',str(inputHeight))
				line = line.replace('INPUT_WIDTH',str(inputWidth))
				line = line.replace('INPUT_Y_POS',str(y))
				line = line.replace('INPUT_X_POS',str(x+(labelWidth-\
					inputWidth)/2))
				line = line.replace('PV_NAME',pvBase)#+'RUpr')
				screen.append(line)
			x += labelWidth
			#channel ramp down rate
			for	line in textInput:
				line = line.replace('INPUT_HEIGHT',str(inputHeight))
				line = line.replace('INPUT_WIDTH',str(inputWidth))
				line = line.replace('INPUT_Y_POS',str(y))
				line = line.replace('INPUT_X_POS',str(x+(labelWidth-\
					inputWidth)/2))
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
		# Appends final line of OPI format and writes all lines to an OPI file 	
		# with the name of the group.
		screen.append(lastLine)
		writeFile(outPath,fileName+'-list.opi',screen)

	#makes Histogram plots for individual detectors
	for i,item in enumerate(menuOptions):
		screen = makeHistoPlot(item[0],vMon[i],iMon[i],menuOptions)
		writeFile(outPath,item[1][:-9]+'-plot.opi',screen)
	
	# makes histogram plots for overall spectrometer
	screen = makeHistoPlot(spectrometer,flatten(vMon),flatten(iMon),menuOptions)
	writeFile(outPath,spectrometer+'-plot.opi',screen)

if mapOut:
	# Declares input configuration files and output file name
	hvConfig = prefix+'.hvc'
	groupFile = prefix+'.group'
	alhFile = prefix+'.alhConfig'

	# Tries to open .hvc file, gives warning and exits if cannot.
	try:
		with open(hvConfig,'r') as f:
			configLines = f.readlines()
	except:
		print('Cannot open config file: '+hvConfig+'.\n')
		sys.exit(0)

	# Reads in HV.hvc, prints crate numbers, checks channels for duplication.
	chs,used,prevCrate,groups,labels = [],[],[],array.array('i'),[]
	for line in configLines:
		if line[0] != '#' and line[0] != '\n':
			label,crate,slot,channel,group = line.strip().split()[:5]
			labels.append(label)
			chs.append([label,crate,slot,channel,group])
			groups.append(int(group))
			if crate not in prevCrate:
				prevCrate.append(crate)
				if not alhOnly:
					print('Found new crate... number '+crate)
			if [crate,slot,channel.zfill(2)] not in used:
				used.append([crate,slot,channel.zfill(2)])
			else:
				print('>>>'+'\033[1m'+'\tMultiply assigned HV channel!'+\
					'\033[0m'+'\n>>>\tCrate/Slot/Channel '+crate+'/'+\
					slot+'/'+channel+' already assigned to '+'\033[1m'+\
					chs[used.index([crate,slot,channel])][0]+'\033[0m'+\
					'.\n>>>\tAttempted assignment to '+'\033[1m'+label+\
					'\033[0m'+' has been ignored.\n>>>')

	# Reads in HV.group and prints each group with ID number and number of 
	# channels
	if (os.path.isfile(groupFile)):
		if not alhOnly:
			print('Opening group file '+groupFile)
		try:
			with open(groupFile,'r') as f:
				groupLines = f.readlines()
		except:
			print('Cannot open config file: '+groupFile+'.\n')
			sys.exit(0)
	if not alhOnly:
		print('Group Information:')
	grNames = []
	for line in groupLines:
		if line[0] != '#' and line[0] != '\n':
			grID = line.strip().split(' ')[0]
			grName = ' '.join(line.strip().split(' ')[1:])
			grNames.append([grID,grName])
			if not alhOnly:
				print('\tGroup '+grName+' (id '+grID+')'+' has '+\
					str(groups.count(int(grID)))+' channels')


	# Creates group_map file
	date = datetime.now().strftime('%X %a %b %d %Y')
	pgHeader = ('Group Contents Map Generated '+date).center(80)[:len((\
		'Group Contents Map Generated '+date).center(80))-len('Page:N')]+'Page:'

	groupLines.sort()

	mapping = []
	for group in groupLines:
		grID = group.strip().split(' ')[0]
		grName = ' '.join(group.strip().split(' ')[1:])
		if len(grName) > 18:
			hold = ['_'*19+'|',('Group '+grID).center(19)+'|',\
				grName[:18].center(19)+'|',grName[18:].center(19)+'|',\
				'_'*19+'|',' '*19+'|']
		else:
			hold = ['_'*19+'|',('Group '+grID).center(19)+'|',\
				grName.center(19)+'|',' '*19+'|','_'*19+'|',' '*19+'|']
		for ch in chs:
			chID,cr,sl,chn,gr = ch
			chn = chn.zfill(2)
			if gr == str(grID):
				spacing = 17-len(chID)-len(cr+'/'+sl+'/'+chn)
				line = ' '+chID+' '*spacing+cr+'/'+sl+'/'+chn+' |'
				if len(line) > 20:
					line = line[: -2]+'|'
				hold.append(line)
		hold.append(' '*19+'|')
		mapping.append(hold)

	numPgs = int(ceil(len(groupLines)/4.0))
	start,final = 0,[]
	for page in range(0,numPgs):
		pg = mapping[start*page:start*page+4]
		maxLen = 0
		for item in pg:
			if len(item) > maxLen:
				maxLen = len(item)
		for i,item in enumerate(pg):
			if len(item) < maxLen:
				diff = maxLen - len(item)
				for q in range(0,diff):
					pg[i].append(' '*19+'|')
		start += 4
		if page != 0:
			final.append('\f')
		final.append(pgHeader+str(page+1))
		for i in range(0,len(pg[0])):
			line = '|'	
			for grp in pg:
				line += grp[i]
			final.append(line)

	if not alhOnly:
		with open(outPath+'group_map','w') as f:
			for line in final:
				f.write(line)
				f.write('\n')


	# Creates channel_map file
	labels = [x for _,x in sorted(zip(used,labels))]
	used.sort()

	chMap = []
	maxSl = maxCh = 0
	for crate in prevCrate:
		hold = []
		for ch in used:
			if ch[0] == crate:
				hold.append(ch)
			if int(ch[2]) > maxCh:
				maxCh = int(ch[2])
			if int(ch[1]) > maxSl:
				maxSl = int(ch[1])
		chMap.append(hold)

	pgHeader = ('Channel Map Generated '+date).center(80)[:len((\
		'Channel Contents Map Generated '+date).center(80))-\
		len('Page:N')]+'Page:'
	crateMap = []
	for crNum,crate in enumerate(chMap):
		hold = ['_'*19+'|',('Crate '+str(crNum+1)).center(19)+'|','_'*19+'|',]
		for slot in range(0,maxSl+1):
			for ch in range(0,maxCh+1):
				chInfo = str(slot)+'/'+str(ch).zfill(2)
				try:
					chID = labels[used.index([str(crNum+1),str(slot),\
						str(ch).zfill(2)])]
					hold.append(' '+chInfo.ljust(6)+chID.center(12)+'|')
				except:
					hold.append((' '+chInfo).ljust(19)+'|')
		crateMap.append(hold)

	numPgs = int(ceil(len(crateMap)/4.0))
	start,final = 0,[]
	for page in range(0,numPgs):
		pg = crateMap[start*page:start*page+4]
		start += 4
		if page != 0:
			final.append('\f')
		final.append(pgHeader+str(page+1))
		for i in range(0,len(pg[0])):
			line = '|'	
			for grp in pg:
				line += grp[i]
			final.append(line)

	if not alhOnly:
		with open(outPath+'channel_map','w') as f:
			for line in final:
				f.write(line)
				f.write('\n')

	# Creates .alhConfig file
	specNoSpace = spec.replace(' ','_')
	final = 'GROUP    NULL'+' '*15+specNoSpace+'\n'+'$ALIAS '+spec+\
		' Detector High Voltage\n\n'
	for grp in groupLines:
		grID = grp.strip().split(' ')[0]
		name = ' '.join(grp.strip().split(' ')[1:])
		nameNoSpace = name.replace(' ','_')
		final += 'GROUP    '+specNoSpace+' '*15+nameNoSpace+'\n'+'$ALIAS '+\
			name+'\n\n'
		for ch in chs:
			if ch[4] == grID:
				pvBase = 'hchv'+ch[1]+':'+ch[2].zfill(2)+':'+ch[3].zfill(3)
				final+= 'CHANNEL  '+nameNoSpace+' '*18+pvBase+':VDiff\n'+\
					'$ALIAS '+ch[0]+' '+ch[1]+'/'+ch[2]+'/'+ch[3].zfill(2)+\
					'\n'+'$COMMAND  edm -noautomsg -eolc -x -m "sig='+\
					pvBase+',title='+ch[0]+',address='+ch[1]+'/'+ch[2]+'/'+\
					ch[3].zfill(2)+'" HV_alarm_set.edl >> /dev/null\n\n'

	with open(outPath+alhFile,'w') as f:
		f.write(final)

#!/bin/env python

# Base formatting of an OPI in text. Each list element is a different line
# of the final OPI file.
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

#start of OPI format for xy plot.
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
'    <axis_0_maximum>100.0</axis_0_maximum>',\
'    <axis_0_minimum>0.0</axis_0_minimum>',\
'    <axis_0_scale_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\',\
 pixels="false">Default</opifont.name>',\
'    </axis_0_scale_font>',\
'    <axis_0_scale_format></axis_0_scale_format>',\
'    <axis_0_show_grid>true</axis_0_show_grid>',\
'    <axis_0_time_format>0</axis_0_time_format>',\
'    <axis_0_title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1"\
 pixels="false">Default Bold</opifont.name>',\
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
'    <axis_1_log_scale>true</axis_1_log_scale>',\
'    <axis_1_maximum>1000.0</axis_1_maximum>',\
'    <axis_1_minimum>0.0</axis_1_minimum>',\
'    <axis_1_scale_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="0"\
 pixels="false">Default</opifont.name>',\
'    </axis_1_scale_font>',\
'    <axis_1_scale_format></axis_1_scale_format>',\
'    <axis_1_show_grid>true</axis_1_show_grid>',\
'    <axis_1_time_format>0</axis_1_time_format>',\
'    <axis_1_title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1"\
 pixels="false">Default Bold</opifont.name>',\
'    </axis_1_title_font>',\
'    <axis_1_visible>true</axis_1_visible>',\
'    <axis_count>2</axis_count>',\
'    <backcolor_alarm_sensitive>false</backcolor_alarm_sensitive>',\
'    <background_color>',\
'      <color red="240" green="240" blue="240" />',\
'    </background_color>',\
'    <border_alarm_sensitive>true</border_alarm_sensitive>',\
'    <border_color>',\
'      <color red="0" green="128" blue="255" />',\
'    </border_color>',\
'    <border_style>0</border_style>',\
'    <border_width>1</border_width>',\
'    <enabled>true</enabled>',\
'    <forecolor_alarm_sensitive>false</forecolor_alarm_sensitive>',\
'    <foreground_color>',\
'      <color red="0" green="0" blue="255" />',\
'    </foreground_color>',\
'    <height>HEIGHT</height>',\
'    <name>XY Graph_1</name>',\
'    <plot_area_background_color>',\
'      <color red="255" green="255" blue="255" />',\
'    </plot_area_background_color>',\
'    <pv_name>loc://PLOT_NAME(0)</pv_name>',\
'    <pv_value />',\
'    <rules />',\
'    <scale_options>',\
'      <width_scalable>true</width_scalable>',\
'      <height_scalable>true</height_scalable>',\
'      <keep_wh_ratio>false</keep_wh_ratio>',\
'    </scale_options>',\
'    <scripts />',\
'    <show_legend>false</show_legend>',\
'    <show_plot_area_border>false</show_plot_area_border>',\
'    <show_toolbar>false</show_toolbar>',\
'    <title></title>',\
'    <title_font>',\
'      <opifont.name fontName="Cantarell" height="11" style="1"\
 pixels="false">Default Bold</opifont.name>',\
'    </title_font>',\
'    <tooltip>$(trace_0_y_pv)',\
'$(trace_0_y_pv_value)</tooltip>']

# OPI format for channel of XY Plot.
# Each PV to add needs its own channel in plot.
xyPlotChannelFmt = [\
'    <trace_PV-NUM_anti_alias>true</trace_PV-NUM_anti_alias>',\
'    <trace_PV-NUM_buffer_size>3</trace_PV-NUM_buffer_size>',\
'    <trace_PV-NUM_concatenate_data>false</trace_PV-NUM_concatenate_data>',\
'    <trace_PV-NUM_line_width>10</trace_PV-NUM_line_width>',\
'    <trace_PV-NUM_name>$(trace_PV-NUM_y_pv)</trace_PV-NUM_name>',\
'    <trace_PV-NUM_plot_mode>0</trace_PV-NUM_plot_mode>',\
'    <trace_PV-NUM_point_size>4</trace_PV-NUM_point_size>',\
'    <trace_PV-NUM_point_style>0</trace_PV-NUM_point_style>',\
'    <trace_PV-NUM_trace_color>',\
'      <color red="21" green="21" blue="196" />',\
'    </trace_PV-NUM_trace_color>',\
'    <trace_PV-NUM_trace_type>3</trace_PV-NUM_trace_type>',\
'    <trace_PV-NUM_update_delay>100</trace_PV-NUM_update_delay>',\
'    <trace_PV-NUM_update_mode>0</trace_PV-NUM_update_mode>',\
'    <trace_PV-NUM_visible>true</trace_PV-NUM_visible>',\
'    <trace_PV-NUM_x_axis_index>0</trace_PV-NUM_x_axis_index>',\
'    <trace_PV-NUM_x_pv>loc://chPV-NUM(PV-NUM)</trace_PV-NUM_x_pv>',\
'    <trace_PV-NUM_x_pv_value />',\
'    <trace_PV-NUM_y_axis_index>1</trace_PV-NUM_y_axis_index>',\
'    <trace_PV-NUM_y_pv>PV_NAME</trace_PV-NUM_y_pv>',\
'    <trace_PV-NUM_y_pv_value />']

# OPI format for end of XY Plot widget.
xyPlotEnd = [\
'    <trace_count>NUMBER_OF_PVS</trace_count>',\
'    <transparent>false</transparent>',\
'    <trigger_pv></trigger_pv>',\
'    <trigger_pv_value />',\
'    <visible>true</visible>',\
'    <widget_type>XY Graph</widget_type>',\
'    <width>WIDTH</width>',\
'    <wuid>5c548784:167ade5fc14:-7ea6</wuid>',\
'    <x>X_POS</x>',\
'    <y>Y_POS</y>',\
'  </widget>']

# function to generate bar plot for list of PVs.
# pvs = list of PVs where PVs are in string format.
# yAxisLabel = string for y-axis label
# height = integer height of plot
# width = integer width of plot
def xyPlot(pvs,yAxisLabel,height,width):
	plot = []
	for line in xyPlotStart:
		line = line.replace('Y_AXIS_LABEL',yAxisLabel)
		line = line.replace('HEIGHT',str(height))
		plot.append(line)
	for chNum,pv in enumerate(pvs):
		for line in xyPlotChannelFmt:
			line = line.replace('PV-NUM',str(chNum))
			line = line.replace('PV_NAME',pv)
			plot.append(line)
	for line in xyPlotEnd:
		line = line.replace('NUMBER_OF_PVS',str(len(pvs)))
		line = line.replace('WIDTH',str(width))
		plot.append(line)
	return plot




pvFile = 'hv.tcl'
configFile = 'HV.hvc'
groupFile = 'HV.group'

# Reads in hv.tcl file that contains all PVs.
with open(pvFile,'r') as f:
	lines = f.readlines()

# For each channel, pulls out all PVs from hv.tcl.
props = ['VMon','Imon','Status','V0Setr','Trip','SVMaxr','RUpr','RDWnr']
chList,pvs,vMon,iMon = [],[],[],[]
for line in lines:
	if 'set {LABELS(' in line:
		hold = []
		chList.append(line.split(' ')[2].strip()[1: -1])
		hold.append(line.split(' ')[2].strip()[1: -1])
		for prop in props:
			p1,p2,p3 = line[12:17].split('_')
			hold.append('hchv'+p1+':'+p2.zfill(2)+':'+p3.zfill(3)+':'+prop)
			if prop == 'VMon':
				vMon.append('hchv'+p1+':'+p2.zfill(2)+':'+p3.zfill(3)+':'+prop)
			if prop == 'IMon':
				iMon.append('hchv'+p1+':'+p2.zfill(2)+':'+p3.zfill(3)+':'+prop)
		pvs.append(hold)


# Reads in channel configuration file.
with open(configFile,'r') as f:
	configLines = f.readlines()

# Reads in groups file.
groups = []
with open(groupFile,'r') as f:
	lines = f.readlines()
for line in lines:
	groups.append([line[0],line[1:].strip()])

# Splits up config file into groups.
for i,grp in enumerate(groups):
	hold = []
	for line in configLines:
		 if line[0] != '#':
			group = line.strip().split(' ')[4]
			if group == grp[0]:
				groups[int(i)].append([line.strip().split(' ')[0]])



#Below is development of making tables for each group.
xSpacing = 10
ySpacing = 8
screenWidth = 850
labelHeight = buttonHeight = indicatorHeight = ledHeight = inputHeight = 20
labelWidth = 75
buttonWidth = 50
ledWidth = 50
inputWidth = 68
indicatorWidth = 68
horizDivLen = 760



for grp in groups:
# Lists HV Controls for each group in table format.
	grpNum = grp[0]
	grpName = grp[1]
	channels = grp[2:]
	fileName = grpName.replace(' ','-')

	x = y = 50
	x0,y0 = x,y

	#Fills out opiname property of screen.
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
		line = line.replace('LABEL_WIDTH',str(300))
		line = line.replace('LABEL_TEXT',grpName+' HV')
		line = line.replace('LABEL_NAME',grpName+' HV')
		line = line.replace('LABEL_Y_POS',str(5))
		line = line.replace('LABEL_X_POS',str((screenWidth/2)-150))
		line = line.replace('FONT_STYLE',str(1))
		line = line.replace('FONT_SIZE',str(14))
		screen.append(line)


	#Generates labels for table header.
	#For FONT_STYLE, 1 is bold, 0 regular
	headerContents = ['Ch ID','On/Off','Status','Vmon','Imon','Vset','Itrip',\
		'Vmax','RmpUp','RmpDwn']
	columns = []
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
		columns.append(x)
		x += labelWidth#+xSpacing
	y += labelHeight+ySpacing


	for ch in channels:
		x = x0
		chID = ch[0]
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
		x += labelWidth#+xSpacing
		for	line in button:
			line = line.replace('BUTTON_HEIGHT',str(buttonHeight))
			line = line.replace('BUTTON_WIDTH',str(buttonWidth))
			line = line.replace('BUTTON_Y_POS',str(y))
			line = line.replace('BUTTON_X_POS',str(x+(labelWidth-\
				buttonWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in led:
			line = line.replace('LED_HEIGHT',str(ledHeight))
			line = line.replace('LED_WIDTH',str(ledWidth))
			line = line.replace('LED_Y_POS',str(y))
			line = line.replace('LED_X_POS',str(x+(labelWidth-ledWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textUpdate:
			line = line.replace('INDICATOR_HEIGHT',str(indicatorHeight))
			line = line.replace('INDICATOR_WIDTH',str(indicatorWidth))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',\
					str(x+(labelWidth-indicatorWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textUpdate:
			line = line.replace('INDICATOR_HEIGHT',str(indicatorHeight))
			line = line.replace('INDICATOR_WIDTH',str(indicatorWidth))
			line = line.replace('INDICATOR_Y_POS',str(y))
			line = line.replace('INDICATOR_X_POS',\
					str(x+(labelWidth-indicatorWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
		x += labelWidth#+xSpacing
		for	line in textInput:
			line = line.replace('INPUT_HEIGHT',str(inputHeight))
			line = line.replace('INPUT_WIDTH',str(inputWidth))
			line = line.replace('INPUT_Y_POS',str(y))
			line = line.replace('INPUT_X_POS',str(x+(labelWidth-inputWidth)/2))
			line = line.replace('PV_NAME','placeholder-pv')
			screen.append(line)
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

	screen.append(lastLine)
	with open(fileName+'-list.opi','w') as f:
		for line in screen:
			f.write(line)
			f.write('\n')

	print(fileName+'.opi created.')

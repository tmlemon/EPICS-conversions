# Base formatting of an OPI screen in text.
# Each list element is a different line of the final OPI file.
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
'    <axis_1_visible>true</axis_1_visible>',\
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


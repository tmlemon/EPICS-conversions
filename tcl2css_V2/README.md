# tcl2css_V2 Scripts
**Python script and CSS GUIs to convert EPICS formats and for Hall C HV Tcl/Tk-to-CSS conversion.**

*Development of these scripts are ongoing as of May 3, 2019.*

All items are developed to be run from CSS.

- backup-restore
  - subdirectory containing backup restore Python program and CSS GUIs for V2 of tcl2css

- HV.group
  - Tcl/Tk configuration file containing group ID numbers and names.
  - This version is both HMS and SHMS combined.

- HV.hvc
  - Tcl/Tk configuration files containing channel mapping (crate/slot/channel) and settings.
  - This version is both HMS and SHMS combined.

- all_off.py
  - group control script for turning all channels on a screen off.
 
- all_on.py
  - group control script for turning all channels on a screen on.
  
- all_set.py
  - group control for setting value to all channels on screen.

- hv-gui.opi
  - CSS .opi file that is used as the template to display list format controls/monitoring screen.
  
- hv-header.opi
  - List header and group menu that is put on every hv-gui.opi version.
  - Contents are placed into hv-gui.opi in a linked container.

- main-menu.opi
  - CSS menu with buttons to open/create screens for each detector system.

- tcl2css_V2.opi
  - Python script called by hv-gui.opi to create and place widgets.
  - This program only works correctly when called within CSS from hv-gui.opi.
  - If run from command line, program only outputs debugging info and channel mapping.

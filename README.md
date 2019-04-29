# EPICS Conversion Scripts
**Python script to convert EPICS formats.**

*Development of these scripts are ongoing as of December 6, 2018.*

Programs are designed to run from Linux command line. 



- backup-restore
  - all backup and restore programs developed for Hall C EPICS.
- group-controls
  - all scripts called in CSS to write values to multiple PVs using one widget.
  
- csv2edl.py
  - Converts comma-separated-variable table of PVs and labels to EDM .edl files.
  
- hv_map.py
  - Replicates Hall C's perl scripts used when generating HV TCL/TK HV screens.
  - Program reads in .hvc config file and outputs channel map, group map, and ALH config file.
  - Code hv_map.py has been integrated into tcl2css.py

- opi2edl.py
  - Converts CSS .opi files to EDM .edl files.

- tcl2css.py
  - Converts .tcl files to CSS .opi files.
  - Script will output hv_map.py's files if ```-m``` option is added as first input argument.
  - Script is not universal; Parsing of files used to generate .tcl screens are based on Hall C HV screens.

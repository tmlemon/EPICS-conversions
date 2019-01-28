# EPICS Conversion Scripts
**Python script to convert EPICS formats.**

*Development of these scripts are ongoing as of December 6, 2018.*

Programs are designed to run from Linux command line. 





- csv2edl.py
  - Converts comma-separated-variable table of PVs and labels to EDM .edl files.

- hv_map.py
  - Replicates Hall C's perl scripts used when generating HV TCL/TK HV screens.
  - Program reads in .hvc config file and outputs channel map, group map, and ALH config file.
  - Eventually, hv_map.py will be integrated into tcl2css.py

- opi2edl.py
  - Converts CSS .opi files to EDM .edl files.

- tcl2css.py
  - Converts .tcl files to CSS .opi files.
  - Script is not universal; Parsing of files used to generate .tcl screens are based on Hall C HV screens.

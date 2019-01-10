# EPICS Conversion Scripts
**Python script to convert EPICS formats.**

*Development of these scripts are ongoing as of December 6, 2018.*

Programs are designed to run from Linux command line. 





- csv2edl.py
  - Converts comma-separated-variable table of PVs and labels to EDM .edl files.

- csv2opi.py
  - Converts comma-separated-variable table of PVs and labels to CSS .opi files.

- opi2edl.py
  - Converts CSS .opi files to EDM .edl files.

- tcl2css
  - Converts .tcl files to CSS .opi files.
  - Script is not universal; Parsing of files used to generate .tcl screens are based on Hall C HV screens.

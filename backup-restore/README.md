 # EPICS Backup and Restore
**Python scripts to backup Hall C EPICS.**

*Development of these scripts are ongoing as of April 15, 2019.*

Programs are designed to run from Linux command line.

- epics-backup.py
  - Reads from a request file and creates log to act as backup record for PVs.

- epics-restore.py
  - Reads from a backup file and writes values to PVs.

- HV-backup.py
  - Backup program specifically for Hall C CSS HV screens.
  - Program designed to be called from a CS-Studio GUI.
  - Can still be called from Linux command line, but it contains very little error handling.
  
- chID_reference.txt
  - reference document containing all Hall C HV channel ID and mapping.

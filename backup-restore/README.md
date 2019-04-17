 # EPICS Backup and Restore
**Python scripts to backup Hall C EPICS.**

*Development of these scripts are ongoing as of April 15, 2019.*

- css-gui
  - All CS-Studio GUIs developed for backup and restore.

- HV-backup.py
  - Backup program specifically for Hall C CSS HV screens.
  - Program designed to be called from a CS-Studio GUI.
  - Can still be called from Linux command line, but it contains very little error handling.

- HV-bur.py
  - Combines HV-backup.py and HV-restore.py into one program for ease of import.
  - Program designed to be called from a CS-Studio GUI.
  - Can still be called from Linux command line, but it contains very little error handling.

- HV-restore.py
  - PV restore program specifically for Hall C CSS HV screens.
  - Program designed to be called from a CS-Studio GUI.
  - Can still be called from Linux command line, but it contains very little error handling.

- chID_reference.txt
  - reference document containing all Hall C HV channel ID and mapping.

- epics-backup.py
  - Reads from a request file and creates log to act as backup record for PVs.
  - Program designed to be run from Linux command line.
  
- epics-restore.py
  - Reads from a backup file and writes values to PVs.
  - Program designed to be run from Linux command line.

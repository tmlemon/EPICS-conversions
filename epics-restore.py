#!/usr/bin/env python
'''
author:  Tyler Lemon
date:    2019-03-19

This program works in conjunction with "epics-backup.py" to restore values
to EPICS fields using a backup file.

This main interface of this program to EPICS is through the command line
using the command "caput". "caput" is called using the subprocess module
and the output is logged into the backup file. "caput" is included in EPICS
base installations.

This program was developed to run from a terminal interface using input
arguements. The usage and command options are below:

python epics-restore.py [<input req file>]

If no input file is entered, program automatically looks in current working
directory for the latest backup file generated by "epics-backup.py".
'''
import subprocess
import sys
import os
from datetime import datetime


# Checks input arguments for file to restore from.
if '-h' not in sys.argv and '--help' not in sys.argv:
    if len(sys.argv)-1 > 0:
        savFile = sys.argv[1]
    else:
        print('\nNo input for save file received.\nProgram will find most \
recent in current working directory to use.')
        fList = os.listdir(os.getcwd())
        poss = []
        mostRecent = ['','']
        for item in fList:
            if item[-4:] == '.sav':
                check = '_'.join(item[:-4].split('_')[-2:])
                if check > mostRecent[0]:
                    mostRecent = [check,item]
        savFile = mostRecent[1]
    if not os.path.isfile(savFile) or savFile[-4:] != '.sav':
        if savFile == '':
            print('\nError:\tNo file to restore from found in current working \
directory.\nUse -h or --help for help information.\n')
        else:
            print('\nERROR:\tFile to restore from must exist and have ".sav" \
as its file extension\nUse -h or --help for help information.\n')
        sys.exit(1)
else:
    print('\npython epics-restore.py [<input req file>]\n\nIf no input\
 file is entered, program automatically looks in current working\ndirectory for\
 the latest backup file generated by "epics-backup.py".\n')
    sys.exit(1)


# Reads input file.
print('\nRestoring PVs from "'+savFile+'".')
fail = False
pvs = []
with open(savFile,'r') as f:
    for line in f.readlines():
        if line[0] != '#':
            pvs.append(line.strip().split('\t'))


# Writes data from input file to PVs.
total = len(pvs)*len(pvs[0][1:])
count = error = okay = 0
errorList = []
for pv in pvs:
    pvName = pv[0]
    fields = pv[1:]
    fieldName = ['.HIHI','.HIGH','.LOW','.LOLO','.HHSV','.HSV','.LSV','.LLSV']
    for i,field in enumerate(fields):
        cmd = ['caput','-t',pvName+fieldName[i],field]
        try:
            put = subprocess.check_output(cmd,stderr=subprocess.STDOUT)\
                .decode('utf-8').strip()
            okay = okay + 1
        except subprocess.CalledProcessError:
            error = error + 1
            errorList.append(field)
            fail = True
        count = count + 1
        sys.stdout.write('\r{1} |{0}|'.format(int(25*count/total)*'=',\
                str(int(100*count/total))+'%'))
        sys.stdout.flush()

# Prints message stating whether program was successful.
if not fail:
    print('\n\nRestore successful.\n')
else:
    print('\n\nRestore failed.\n')

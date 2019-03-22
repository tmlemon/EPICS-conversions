#!/usr/bin/env python
'''
Author: Tyler Lemon
Date:   2019-03-12

This program reads EPICS PVs and fields declared using an input file and
creates a document containing the current PV/field values.

This main interface of this program to EPICS is through the pyepics module.
The pyepics module uses EPICS channel access to write a list of values for
PVs defined by a ".req" file to a ".sav" file using the
epics.autosave.save_pvs() function.

For this program to run correctly, the pyepics module is needed.

This program was developed to run from a terminal interface using input
arguements. The usage and command options are below:

epics-backup.py <req-file> [--dev] [-h/--help] [-o <out>] [-c "<comment>"]

Mandatory Arguement:
<req-file>   - Name of request file containing PVs to backup. File extension
                must be ".req".

[Optional Arguemnts]:
-o           - Option that specifies prefix of output file. <out> cannot be
                the same as <req-file> (epics-backup.py -o example.req
                is not a valid input).

-c           - Option to add comment to end result log file. The comment to
                add to the backup file must be the arguement immediately
                following -c and should be enclosed in "double quotes".

-h/--help    - Prints this help message.
'''
#to add
#	gui?
# remove assumption youre doing alarm fields -- IN PROGRESS


import sys
import subprocess
from datetime import datetime
import os
import time

try:
    import epics
    import epics.autosave
except:
    print('\nERROR:\tEPICS PYTHON MODULE NOT FOUND.\n\tThe "pyepics" module \
is not installed or cannot be found.\n\t"pyepics" is required to run this \
program.\n')
    sys.exit(0)



#gets time at start of program for overall timing
startTime = time.time()

# flag used to indicate failure of backup
fail = False


# Checks user's input arguements for input file prefix of output file
if '-h' not in sys.argv and '--help' not in sys.argv:
#checking for -i arguement for input file
    for arg in sys.argv:
        if '.req' in arg:
            backupReq = arg
            break
        else:
            backupReq = ''
    if not os.path.isfile(backupReq):# or backupReq[-4:] != '.req':
        print('\nERROR: BACKUP REQUEST FILE NOT FOUND.\n\tInput was not a \
valid request file.\n\tTo perform backup, a valid request file is needed.\n\
\tUse -h or --help for more information.\n')
        sys.exit(0)
#checking for -o arguement for output file name.
    if '-o' in sys.argv:
        try:
            outName = sys.argv[sys.argv.index('-o')+1]
            outName.replace(' ','_')
            if outName == backupReq:
                print('\nERROR: INCORRECT SEQUENCE OF INPUT OPTIONS\n\
\tIf -o option is used, next arguement needs to be name of output file.\n\
\tThe name of the output file cannot be the same as the full backup\n\
\trequest file.\n\tUse -h or --help for more information.\n')
                fail = True
                sys.exit(0)
        except:
            if not fail:
                print('\nERROR: INCORRECT SEQUENCE OF INPUT OPTIONS\n\
\tIf -o option is used, next arguement needs to be name of output file.\n\
\tUse -h or --help for more information.\n')
            sys.exit(0)
    else:
        outName = 'backup'
# checking for -c arguement for commenmts
    if '-c' in sys.argv:
        try:
            comment = sys.argv[sys.argv.index('-c')+1]
        except:
            print('\nERROR:\tIf -c option is used, next arguement \
needs to the comment\n\tto add to log file.\n\tIf comment to add to log \
is more than one word, comment must be\n\tenclosed in "double quotes".\n\
\tUse -h or --help for more information.\n')
            sys.exit(0)
    else:
        comment = ''
# prints help message if -h or --help is in input arguements
else:
    print('\nepics-backup.py <req-file> [--dev] [-h/--help] [-o <out>] [-c\
"<comment>"]\n\n\
Mandatory Arguement:\n\
<req-file>\t- Name of request file containing PVs to backup. File extension\n\
\t\t\t  must be ".req".\n\n\
[Optional Arguemnts]:\n\
-o\t\t\t- Option that specifies prefix of output file. <out> cannot be\n\
\t\t\t  the same as <req-file> (epics-backup.py -o example.req\n\
\t\t\t  is not a valid input).\n\n\
-c\t\t\t- Option to add comment to end result log file. The comment to\n\
\t\t\t  add to the backup file must be the arguement immediately\n\
\t\t\t  following -c and should be enclosed in "double quotes".\n\n\
-h/--help\t- Prints this help message.\n')
    sys.exit(0)

# Date and name of output file to use
date = str(datetime.now())[:str(datetime.now()).find('.')]
outFile = outName+'_'+date.replace(' ','_')+'.sav'

print('')

epics.autosave.save_pvs(backupReq,outFile)

with open(outFile,'r') as f:
    restData = f.readlines()
pvs = []
vals = []
for line in restData:
    line = line.strip()
    if line[0] != '#' and line != '<END>':
        pvs.append(line.split(' ')[0])
        out = line.split(' ')[0]+'\t'
        if 'DESC' in line:
            vals.append(' '.join(line.split(' ')[1:]))
        else:
            vals.append(line.split(' ')[1])

check = epics.caget_many(pvs,as_string=True)
okay = True
failed = []
for i,item in enumerate(check):
    if 'SV' in pvs[i]:
        if item == 'MINOR':
            item = '1'
        elif item == 'MAJOR':
            item = '2'
        elif item == 'NO_ALARM':
            item = '0'
    if item != vals[i]:
        okay = False
        failed.append(pvs[i])
if not okay:
    print('\nERROR:\tBACKUP VERIFICATION FAILED.\n\tPVs who were unable to be\
backed up were:')
    for item in failed:
        print(item)
elif okay:
    print('Backup successful.\n')
else:
    print('\nERROR:\t SOMETHING UNEXPECTED HAPPENED.\n\tAn error occured that \
was not forseen ever happeneing and was not included in any error handling.')




# calculates and prints time it took to run program
runDuration = round(time.time() - startTime,2)
hours = str(int(runDuration/3600))
minutes = str(int((runDuration%3600)/60)).zfill(2)
seconds = str(int((runDuration%3600)%60)).zfill(2)
print('Program complete in '+hours+':'+minutes+':'+seconds)

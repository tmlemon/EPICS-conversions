#!/usr/bin/env python
'''
Author: Tyler Lemon
Date:   2019-03-12

This program reads EPICS PVs and fields declared using an input file and
creates a document containing the current PV/field values.

This main interface of this program to EPICS is through the command line
using the command "caget". "caget" is called using the subprocess module
and the output is logged into the backup file. "caget" is included in EPICS
base installations.

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

--dev        - Option to run program in dev mode where no output files are
                generated and program does not perform verification.

-h/--help    - Prints this help message.
'''
#to add
#	gui?



import sys
import subprocess
from datetime import datetime
import os
import time

#gets time at start of program for overall timing
startTime = time.time()

# flag used to indicate failure of backup
fail = False

# Message to print if --dev option is used
if '--dev' in sys.argv:
    print('\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print('!!======================= DEV MODE =======================!!')
    print('!!============== NO FILE WILL BE GENERATED ===============!!')
    print('!!======== AND VERIFICATION WILL NOT BE PERFORMED ========!!')
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

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
--dev\t\t- Option to run program in dev mode where no output files are\n\
\t\t\t  generated and program does not perform verification.\n\n\
-h/--help\t- Prints this help message.\n')
    sys.exit(0)



# Date and name of output file to use
date = str(datetime.now())[:str(datetime.now()).find('.')]
outFile = outName+'_'+date.replace(' ','_')+'.sav'

# fields that are added to backup file
fields = ['.HIHI','.HIGH','.LOW','.LOLO','.HHSV','.HSV','.LSV','.LLSV']

# reads in request file stated by user input
print('\nReading from request file "'+backupReq+'"')
pvs = []
with open(backupReq,'r') as f:
    for line in f.readlines():
        hold = []
        if line[0] != '#' and line.strip()[0] != '':
            for field in ['.HIHI','.HIGH','.LOW','.LOLO','.HHSV','.HSV','.LSV',\
                '.LLSV']:
                hold.append(line.strip()+field)
        pvs.append(hold)

total = len(pvs)*len(fields)
print('\nRunning backup...')

# reads all pvs using caget and writes their value to the string variable "log"
comment = '# Comments: '+comment
log = ['# Backup made: '+date,comment,\
    '#PV\tHIHI\tHIGH\tLOW\tLOLO\tHHSV\tHSV\tLSV\tLLSV']
count = okay = error = 0
errorList = []
for pv in pvs:
    line = pv[0].split('.')[0]+'\t'
    for field in pv:
        cmd = ['caget','-t',field]
        try:
            result = subprocess.check_output(cmd,stderr=subprocess.STDOUT)\
                .decode('utf-8').strip()
            line += str(result)+'\t'
            okay = okay + 1
        except subprocess.CalledProcessError:
            error = error + 1
            errorList.append(field)
            fail = True
        count = count + 1
        sys.stdout.write('\r{1} |{0}|'.format(int(25*count/total)*'=',\
                str(int(100*count/total))+'%'))
        sys.stdout.flush()
    log.append(line)

if len(errorList) != 0:
    print('\n'+str(error)+' PVs not backed up due to error.')
    print('Recieved errors for PVs/fields:')
    for item in errorList:
        print(item)
    print('\nBackup not completed due to error.')
    print('Check request file and re-run backup.\n')
else:
    print('\nBackup complete.')
    print(str(okay)+' PVs/fields successfully backed up.')



# reads from log and performs another series of caget commands to verify
# contents of backup file.
if '--dev' not in sys.argv and fail == False:
    with open(outFile,'w') as f:
        for line in log:
            f.write(line)
            f.write('\n')
    print('\nVerifying backup file...')
    checkErrorList = []
    with open(outFile,'r') as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        if line[0] != '#':
            rec = line.strip().split('\t')
            pv = rec[0]
            for i,item in enumerate(rec[1:]):
                cmd = ['caget','-t',pv+fields[i]]
                try:
                    result = subprocess.check_output\
                        (cmd,stderr=subprocess.STDOUT).\
                        decode('utf-8').strip()
                    if result != item:
                        checkErrorList.append(pv+field[i])
                except subprocess.CalledProcessError:
                    checkErrorList.append(pv+field[i])
                    fail = True
                count = count + 1
                sys.stdout.write('\r{1} |{0}|'.format(int(25*count/total)*'=',\
                    str(int(100*count/total))+'%'))
                sys.stdout.flush()
    # prints message stating whether verification was successful.
    if len(checkErrorList) != 0:
        print('\n\nVerification of backup file failed.')
        print('"'+outFile+'" does not match present settings of PVs/fields.')
        print('Restart backup program to attempt backup again.\n')
        fail = True
    else:
        print('\nVerification successful.')

# prints final success message if no previous errors.
if not fail:
    print('\nBackup successful.\nData backed up to "'+outFile+'".\n')

# calculates and prints time it took to run program
endTime = time.time()
runDuration = round(endTime - startTime,2)

if runDuration >= 3600:
    hours = runDuration/3600
    minutes = runDuration%3600
    if minutes >= 60:
        minutes = minutes/60
        seconds = minutes%60
    else:
        minutes = 0
        seconds = minutes
elif runDuration >= 60:
    hours = 0
    minutes = runDuration/60
    seconds = runDuration%60
else:
    hours = 0
    minutes = 0
    seconds = runDuration

if hours != 0:
    durationStr = 'Program complete in '+str(hours)+' hours, '+str(minutes)+\
        ' minutes, '+str(seconds)+' seconds.\n'
elif minutes != 0:
    durationStr = 'Program complete in '+str(minutes)+' minutes, '+\
        str(seconds)+' seconds.\n'
else:
    durationStr = 'Program complete in '+str(seconds)+' seconds.\n'

print(durationStr)

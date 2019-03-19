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

python epics-backup.py [--dev] [-i] [<input req file>] [-o] [<output>]

All input arguements are optional. Program will use default input file
"HV-backup.req" if -i option is not used. Default output file is
"backup_<data>_<time>.sav" where <date> and <time> are automatically filled
out with time of execution.

If user uses --dev option, no output file is generated and program does not
perform verification.
'''
#to add
# arg check for:
#	comment
#	gui?




import sys
import subprocess
from datetime import datetime
import os

# Default request file
backupReq = 'HV-backup.req'

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
    if os.path.isfile(backupReq) and '-i' not in sys.argv:
        backupReq = backupReq
    elif '-i' in sys.argv:
        try:
            backupReq = sys.argv[sys.argv.index('-i')+1]
        except:
            print('\nERROR:\tIf -i option is used, next arguement needs to be\
request file.\n')
            sys.exit(0)
    if not os.path.isfile(backupReq) or backupReq[-4:] != '.req':
        print('\nERROR:\tRequest file input is not a valid file.\n\t\
To perform backup, a valid request file is needed.\n')
        sys.exit(0)
    elif not os.path.isfile(backupReq) and '-i' not in sys.argv:
        print('\nERROR:\tTo perform backup, a valid request file is needed.\n\t\
Program looks for default file name "HV-backup.req" if -i option\n\tis\
not used.')
        sys.exit(0)
#checking for -o arguement for output file name.
    if '-o' in sys.argv:
        try:
            outName = sys.argv[sys.argv.index('-o')+1]
            outName.replace(' ','_')
        except:
            print('\nERROR:\tIf -o option is used, next arguement needs to be\
name of output file.\n')
            sys.exit(0)
    else:
        outName = 'backup'
else:
    print('\npython epics-backup.py [--dev] [-i] [<input req file>] [-o]\
[<output>]\n\n\
All input arguements are optional\n\
If no input options used default request file searched for is "HV-backup.req".\
\n\n-i\t\t\t\t- Option that specifies input request file.\
\n-o\t\t\t\t- Option that specifies prefix of output file.\
\n--dev\t\t\t- Option to run program in dev mode where no output files are\n\
\t\t\t\t  generated and program does not perform verification.\n\
-h/--help\t\t- Prints this help message.\n')
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
comment = '# Comments: '
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
    sys.exit(0)
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
        sys.exit(0)
    else:
        print('\nVerification successful.')

# prints final success message if no previous errors.
print('\nBackup successful.\nData backed up to "'+outFile+'".\n')



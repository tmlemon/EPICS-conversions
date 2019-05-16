#!/usr/bin/env python
'''
@author: Tyler Lemon (tlemon)
Date:    2019-05-15

Hall C HV EPICS Backup Restore Python Program - version 3

HV-bur.py = Hall C 'HV' EPICS 'B'ack'U'p 'R'estore 'PY'thon program

HV-bur.py uses CSS Java functions and the subprocess module to backup and
restore HV PVs for Hall C. The Java functions serve as the method to read
in user aruguments and perform the restore. The subprocess module is used to
call a "caget" command for a channel to read its values for the backup. With
the user's first input arguement, program can be set to either backup or
restore.

HV-bur.py is developed to be called from Hall C HV backup and restore
CSS-BOY GUIs. THIS PROGRAM WILL NOT WORK OUTSIDE OF CSS BECAUSE OF THE JAVA
PACKAGES.


Command syntax is:

to RESTORE:
python <path>/HV-bur.py restore <path> [file]

<path> is the path where HV-bur.py, backup files, and CSS-BOY OPI files are.
[file] (optional) is name of backup file to restore from. If not used,
        program looks at <path> and finds latest backup file to use for restore.


to BACKUP:
python <path>/HV-bur.py backup <path> [comment]

<path>    is the path where HV-bur.py, backup files, and CSS-BOY OPI files are.
[comment] (optional) is any comment to add to backup file. When running from
           command line, comment should be enclosed in "double quotes".
'''


import sys #used to read in user inputs
from datetime import datetime #used to get date/time of program execution
import time #used to get start and end time of program.
import os # used tot look for files in execution directory
import org.csstudio.opibuilder.scriptUtil as SU #Java package for CSS
import socket #used to get hostname of PC for dev status
import subprocess #used to call caget commands.

startT = time.time() #start time of program

# Boolean used to tell program to use development IOC rather than real PVs
# Looks at host name to see if it development PC. Add PC to devList to
# automatically run in dev mode when on PC.
devList = ['dsg-c-linux1.jlab.org']
dev = socket.gethostname() in devList

if dev:
    print('DEV MODE ENABLED (see HV-bur.py code, line 52)')
# Size of sub-arrays used in restore. caput_many seems to have problems with
# arrays larger than 600 PVs, so "size" variable was added to let user change
# sub-array size if it makes a difference in execution time.
size = 500

# Regardless of wheter backup or restore, second input arguement from CSS will
# be the path at which the files to backup will be stored.
path = SU.FileUtil.workspacePathToSysPath('CSS')
if path[-1] != '/': path += '/'

go = SU.PVUtil.getDouble(pvs[0])


# START OF CASE FOR RESTORE FUNCTIONALITY
if str(SU.PVUtil.getString(pvs[1])) == 'restore' and go == 1:
    # User can either put in a file to restore from, or leave the control
    # blank in CSS to look in path for latest backup file.
    if str(SU.PVUtil.getString(pvs[2])) != '':
        savFile = str(SU.PVUtil.getString(pvs[1]))
    else:
        fList = os.listdir(path)
        poss = []
        mostRecent = ['','']
        for item in fList:
            if item[-4:] == '.sav':
                check = '_'.join(item[:-4].split('_')[-2:])
                if check > mostRecent[0]:
                    mostRecent = [check,item]
        savFile = mostRecent[1]
    if not os.path.isfile(path+savFile) or savFile[-4:] != '.sav':
        if savFile == '':
            SU.ConsoleUtil.writeError('No file to restore from found in\ current directory.')
        else:
            SU.ConsoleUtil.writeError('File to restore from must exist.')
        sys.exit(1)

    # opens and reads lines of backup file.
    with open(path+savFile,'r') as f:
        restData = f.readlines()

    # Parses lines of backup file and extracts all PVs for a channel and the
    # value contained in the backup file. Also splits PVs and values into
    # sub-arrays of length "size" (variable from beginning).
    props = ['V0Set','I0Set','SVMax','RUp','RDWn']
    count = 0
    restPVs,vals = [],[]
    pvsHold,valsHold = [],[]
    for line in restData:
        if line.strip()[0] not in ['#','']:
            line = line.strip().split('\t')
            chid,crate,slot,channel,group = line[:5]
            basePV = 'hchv'+crate+':'+slot.zfill(2)+':'+channel.zfill(3)+':'
            propSet = line[5:]
            for i,prop in enumerate(propSet):
                count += 1
                if dev:
                    p = 'devIOC:ai'+str(count)
                    v = str(count*2)
                else:
                    p = basePV+props[i]
                    v = float(prop)
                pvsHold.append(p)
                valsHold.append(v)
                if len(pvsHold) >= size:
                    restPVs.append(pvsHold)
                    vals.append(valsHold)
                    pvsHold,valsHold = [],[]
    restPVs.append(pvsHold)
    vals.append(valsHold)

    # Performs the writePV function to write all PV values in backup file,
    # earlier stored in sub-arrays, to the PV.
    for q,grp in enumerate(restPVs):
        for v,item in enumerate(grp):
            SU.PVUtil.writePV(item,vals[q][v])
    # restore complete message to be printed.
    outMsg = 'RESTORE FROM\n'+savFile+'\nCOMPLETE'
# END OF RESTORE CASE.




# START OF CASE FOR BACKUP FUNCTIONALITY
elif str(SU.PVUtil.getString(pvs[1])) == 'backup' and go == 1:
    comment = str(SU.PVUtil.getString(pvs[2]))

    #does some nice formatting for user's comment to make sure it wraps nicely
    #in the final backup file.
    if len(comment) > 60:
        cut = []
        last = 0
        for i,word in enumerate(comment.split(' ')):
            if len(' '.join(comment.split(' ')[last:i])) > 60:
                cut.append(i-1)
                last = i-1
        start = 0
        newComm = ''
        for l,item in enumerate(cut):
            if l != 0:
                newComm += '#\t\t\t'+(' '.join(comment.split(' ')\
                    [start:item]))+'\n'
            else:
                newComm += (' '.join(comment.split(' ')[start:item]))+'\n'
            start = item
        newComm += '#\t\t\t'+(' '.join(comment.split(' ')[start:]))+'\n'
        comment = newComm.strip()


    # Looks at any previous backup file for channel ID mapping.
    # if no previous backup file exists, program uses HV.hcv as a reference
    # document containing only channel ID mapping information.
    prevSav = []
    for item in os.listdir(path):
        if item[-4:] == '.sav':
            prevSav.append(item)
    if len(prevSav) != 0:
        refFile = sorted(prevSav)[-1]
        sep = '\t'
    else:
        refFile = 'HV.hvc'
        sep = ' '

    groups,systems = [],[]
    with open(path+'HV.group','r') as f:
        for line in f.readlines():
            spectrometer = line.strip().split(' ')[1]
            groups.append(line.strip().split(' ')[0])
            systems.append([' '.join(line.strip().split(' ')[1:])])


    with open(path+refFile,'r') as f:    refData = f.readlines()


    for item in refData:
        if len(item.strip()) > 0:
            if item.strip()[0] != '#':
                chID = item.strip().split(sep)[0]
                cr,sl,ch,gr = item.strip().split(sep)[1:5]
                sysI = groups.index(gr)
                systems[sysI].append([chID,[cr,sl,ch,gr]])


    # Creates header for backup file
    date = str(datetime.now())[:str(datetime.now()).find('.')]
    bu = ['# Hall C HV Backup','# Backup created:\t'+date,'# Comment:\t'\
        +comment,'#']

    for item in systems:
        detector = item[0]
        buPVs = item[1:]
        #properties of each HV channel that will be backed up
        props = ['V0Set','I0Set','SVMax','RUp','RDWn']
        buList = []
        count = 1
        for pv in buPVs:
            channelID = pv[0]
            cr,sl,ch,gr = pv[1]
            hold = [channelID+'\t'+cr+'\t'+sl+'\t'+ch+'\t'+gr+'\t','caget','-t']
            for prop in props:
                if dev:
                    hold.append('devIOC:ai'+str(count))
                else:
                    hold.append('hchv'+cr+':'+sl.zfill(2)+':'+ch.zfill(3)\
                        +':'+prop)
                count += 1
            buList.append(hold)

        # Creates header for each detector group.
        bu.append('# Detector: '+detector)
        bu.append('# chid\tcrate\tslot\tchannel\tgroup\tV0Set\tI0Set\tSVMax\t\
RUp\tRDwn')

        # Calls caget for each channel properties and formats it for the
        # backup file.
        for pv in buList:
            cmd = pv[1:]
            line = pv[0]
            res = subprocess.check_output(cmd)
            res = res.strip().replace('\n','\t')
            line += res
            bu.append(line.strip())
        bu.append('#')


    #writes data to a text file (file extension .sav can be changed to fit user
    # preferences).
    outFile = 'HV-backup_'+date.replace(' ','_')+'.sav'
    with open(path+outFile,'w') as f:
        for line in bu:
            f.write(line)
            f.write('\n')

    # prints a reponse that CSS looks for to indicate program is done.
    outMsg = 'BACKUP COMPLETE\n'+outFile+' created.'
# END OF BACKUP CASE

# If for some reason neither backup or restore are entered as arguements,
# this case will catch that and give a message that something bad happened.
elif str(SU.PVUtil.getString(pvs[1])) not in ['backup','restore'] and go == 1:
    outMsg = 'ERROR: "backup" or "restore" not selected or other fatal error.'

dT = time.time() - startT # elapsed time of program
# Since CSS loops over program continuously, this below prevents the completion
# message from blocking the user controls.
try:
    outMsg += '\nExecution time: '+str(round(dT,2))+' seconds'
except:
    outMsg = ''
# Displays completion message in CSS
if go == 1:
    pvs[3].setValue(outMsg)

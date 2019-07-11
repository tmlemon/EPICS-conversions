#!/usr/bin/env python
'''
@author: Tyler Lemon (tlemon)
Date:    2019-07-10

NEW Hall C HV EPICS Backup Restore Python Program

HV-bur = Hall C 'HV' EPICS 'B'ack'U'p 'R'estore 'PY'thon program

NEW HV-bur uses CSS Java functions and the "subprocess" module to backup and
restore HV PVs for Hall C.

The Java functions serve as the method to read in user aruguments and perform
the restore.

The "subprocess" module is used to call a "caget" command (included with
EPICS base installation) for a channel to read its values for the backup.

With the user's first input arguement, program can be set to either backup or
restore.

This version is developed to be called from Hall C HV backup and restore
CSS-BOY GUIs.

*** THIS PROGRAM WILL NOT WORK OUTSIDE OF CSS BECAUSE OF THE JAVA PACKAGES. ***

'''


import sys,time,os,socket,subprocess
from datetime import datetime

# Sometimes CSS doesn't load the Jython packages used by this program.
# If this happens, a message stating the fix for this will be displayed.
try:
    import org.csstudio.opibuilder.scriptUtil as SU #Java package for CSS
except:
    outMsg = 'CSS Environment needs to be reset.\nExit this GUI and use RESET CSS ENV\nbutton at bottom of main menu.'
    pvs[3].setValue(outMsg)
    sys.exit(3)
    

# Function used in developement to print info to CSS console.
def cssPrint(data):
    SU.ConsoleUtil.writeInfo(str(data))

# made a variable for the backup extension to make it easier to change.
backupExt = '.sav'

#start time of program
startT = time.time() 

# Boolean used to tell program to use development IOC rather than real PVs
# Looks at host name to see if it development PC. Add PC to devList to
# automatically run in dev mode when on PC.
devList = ['dsg-c-linux1.jlab.org']
dev = socket.gethostname() in devList


# Path of workspace where all .opi files and scripts are stored.
# NOTE: for this script to work, everything must be in the top directory of
# a workspace.
path = SU.FileUtil.workspacePathToSysPath('CSS')
if path[-1] != '/': path += '/'

# PV for button clicked by user to start backup/restore.
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
            if item[-4:] == backupExt:
                check = '_'.join(item[:-4].split('_')[-2:])
                if check > mostRecent[0]:
                    mostRecent = [check,item]
        savFile = mostRecent[1]
    if not os.path.isfile(path+savFile) or savFile[-4:] != backupExt:
        if savFile == '':
            SU.ConsoleUtil.writeError('No file to restore from found in current directory.')
        else:
            SU.ConsoleUtil.writeError('File to restore from must exist.')
        sys.exit(1)

    # opens and reads lines of backup file.
    with open(path+savFile,'r') as f:
        restData = f.readlines()

    # Parses lines of backup file and extracts all PVs for a channel and the
    # value contained in the backup file.
    # For restore, control PVs are used.
    props = ['V0Set','I0Set','SVMax','RUp','RDWn']
    count = 0
    pvs,vals = [],[]
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
                pvs.append(p)
                vals.append(v)

    # Performs the writePV function to write all PV values in backup file,
    # earlier stored in sub-arrays, to the PV.
    for q,item in enumerate(pvs):
        SU.PVUtil.writePV(item,vals[q])
    # restore complete message to be printed.
    outMsg = 'RESTORE FROM\n'+savFile+'\nCOMPLETE'
# END OF RESTORE CASE.




# START OF CASE FOR BACKUP FUNCTIONALITY
elif str(SU.PVUtil.getString(pvs[1])) == 'backup' and go == 1:
    # comment to write to backup file
    comment = str(SU.PVUtil.getString(pvs[2]))

    #does some formatting for user's comment to make sure it wraps nicely
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
	

    # Creates overall header for backup file
    date = str(datetime.now())[:str(datetime.now()).find('.')]
    bu = ['# Hall C HV Backup','# Backup created:\t'+date,'# Comment:\t'\
        +comment,'#']


    # creates list of list-view files in the CSS workspace.
    listList = []
    for item in os.listdir(path):
        if item[-9:] == '-list.opi' and ('HMS' in item or 'SHMS' in item):
            listList.append(item)
    listList.sort()
    refList = []
    # looks at all files in CSS workspace that are list view screens and pulls
    # out PVs for each channel using a "hidden" reference label on each list
    # view screen.
	# NOTE: this part below isn't done immediatly after finding screen in
	# directory so the detectors can be listed in alphabetical order in final
	# backup file.
    for item in listList:
        hold = [str(item.split('-list.opi')[0].replace('-',' '))]
        with open(path+str(item),'r') as g:
            data = g.readlines()
        iStart = data.index('    <name>'+item.split('-list.opi')[0]+'-Channel-Reference-Str</name>\n')+8
        try:
            refdata = data[iStart:iStart+data[iStart:].index('</text>\n')]
        except:
            refdata = ''
        else:
            for item in refdata:
                if '<text>' in item:
                    hold.append(item.strip()[6:])
                else:
                    hold.append(item.strip())
            refList.append(hold)


    # Iterates through list of channel reference to get create base PVs for
    # each detector.
	# NOTE: this for loop is split off of the one above (even though they could
	# be combined) as a sort of break point to be used for debugging.
    for item in refList:
        detector = item[0]
        buPVs = item[1:]
        # Properties of each HV channel that will be backed up
		# For backup, readback PVs are used.
        props = ['V0Setr','I0Setr','SVMaxr','RUpr','RDWnr']
        buList = []
        count = 1
        for pvStr in buPVs:
            pv = pvStr.split(' ')
            channelID = pv[0]
            cr,sl,ch = pv[1:]
            hold = [channelID+'\t'+cr+'\t'+sl+'\t'+ch+'\t','caget','-t']
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
        bu.append('# chid\tcrate\tslot\tchannel\tV0Set\tI0Set\tSVMax\tRUp\tRDwn')

        # Uses subprocess module to call "caget" for each channel property 
		# and formats it for the backup file.
        for pv in buList:
            cmd = pv[1:]
            line = pv[0]
            res = subprocess.check_output(cmd)
            line += res.strip().replace('\n','\t')
            bu.append(line.strip())
        bu.append('#')


    # Writes all resulting backup data to a text file.
    outFile = 'HV-backup_'+date.replace(' ','_')+backupExt
    with open(path+outFile,'w') as f:
        for line in bu:
            f.write(line)
            f.write('\n')

    # The reponse that CSS looks for to indicate program is done.
    outMsg = 'BACKUP COMPLETE\n'+outFile+' created.'
# END OF BACKUP CASE



# If for some reason neither backup or restore are entered as arguements,
# this case will catch that and give a message that something bad happened.
elif str(SU.PVUtil.getString(pvs[1])) not in ['backup','restore'] and go == 1:
    outMsg = 'ERROR: "backup" or "restore" not selected or other fatal error.'


# Elapsed time of program. Backup takes ~30 seconds. Restore ~10 seconds.
# NOTE: Restore has not been tested with actual PVs, only development PVs.
dT = time.time() - startT

# Since CSS loops over program continuously, this below prevents the completion
# message from blocking the user controls when backup has not been complete.
try:
    outMsg += '\nExecution time: '+str(round(dT,2))+' seconds'
except:
    outMsg = ''

# Displays completion message in CSS, indicating program has 
# finished its operation.
if go == 1:
    pvs[3].setValue(outMsg)


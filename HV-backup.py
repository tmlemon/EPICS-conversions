#!/usr/bin/env python
'''
Author:  Tyler Lemon
Date:    2019-04-09

Program uses pyepics' caget_many to backup HV channel settings.
Progarm gets PVs from an input CS-Studio-BOY (CSS) .opi file.

Program is designed to be called from "backup-gui.opi".
It can still be run from command line, but there are no error handling, input
checking, or helpful printouts.

Use "dev = True" (line ~23) to use development IOC rather than real PVs.
Change "dev" to False for normal operation.
'''

import sys #used to read in user inputs
from datetime import datetime #used to get date/time of program execution
import os
try:
    import epics #used to call caget_many funciton
except:
    print('ERROR: pyepics not found.')
    sys.exit(1)

# Boolean used to tell program to use development IOC rather than real PVs
# Chaneg to false for normal operation.
dev = True


#group mapping from old Tcl/Tk system
groups = ['1','2','3','4','5','7','8','9','11','12','13','14','15','16','17',\
    '18','19','20','21','22','10']
systems = ['HMS Hodo 1 X','HMS Hodo 1 Y','HMS Hodo 2 X','HMS Hodo 2 Y',\
    'HMS Drift Chambers','HMS Shower Counter A','HMS Shower Counter B',\
    'HMS Cherenkov and Aerogel','SHMS Hodo 1 X','SHMS Hodo 1 Y',\
    'SHMS Hodo 2 X','SHMS Hodo 2 Y','SHMS HGC','SHMS NGC','SHMS Aerogel',\
    'SHMS Preshower','SHMS Shower A','SHMS Shower B','SHMS Shower C',\
    'SHMS Shower D','SHMS Drift Chambers']


#Checks whether user input a comment.
if len(sys.argv) >= 3: comment = sys.argv[2]
else: comment = ''

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
            newComm += '#\t\t\t'+(' '.join(comment.split(' ')[start:item]))+'\n'
        else:
            newComm += (' '.join(comment.split(' ')[start:item]))+'\n'
        start = item
    newComm += '#\t\t\t'+(' '.join(comment.split(' ')[start:]))+'\n'
    comment = newComm.strip()

#declares input file (inFile), and path where input file is (path).
#path will also be where final backup file is stored.
path = sys.argv[1]
if path[-1] != '/': path += '/'

prevSav = []
for item in os.listdir(path):
    if item[-4:] == '.sav':
        prevSav.append(item)
if len(prevSav) != 0:
    refFile = sorted(prevSav)[-1]
else:
    refFile = 'chID_reference.txt'

with open(path+refFile,'r') as f:    chids = f.readlines()
ids,maps = [],[]
for item in chids:
    if item.strip()[0] != '#':
        ids.append(item.split('\t')[0])
        maps.append('\t'.join(item.split('\t')[2:5]).strip())

date = str(datetime.now())[:str(datetime.now()).find('.')]
bu = ['# Hall C HV Backup','# Backup created:\t'+date,'# Comment:\t'\
    +comment,'#']

for item in systems:
    group = groups[systems.index(item)]
    inFile = item.replace(' ','-')+'-list.opi'

    #properties of each HV channel that will be backed up
    props = ['V0Set','I0Set','SVMax','RUp','RDwn']


    #Reads in input file and stores it as an array where each element is a line
    # in the file.
    with open(path+inFile,'r') as f: data = f.readlines()


    # reads data from input file and extracts PVs in file.
    # Output of code section (pvs) is an array of PV prefixes for each
    # HV channel (ex. hchv2:00:000:)
    pvs = []
    for item in data:
        item = item.strip()
        if item[:9] == '<pv_name>' and item[-10:] == '</pv_name>':
            pv  = item.split('<pv_name>')[1].split('</pv_name>')[0]
            if pv != '' and 'loc://' not in pv:
                if pv.split(':')[3] in props:
                    pvs.append(':'.join(pv.split(':')[:3]))
    pvs = list(set(pvs))

    #uses pv list and properties to generate list of all pvs that need backing
    # up. Result of code section (buList) is a 2D list where each element is
    # a list of a channel's properties PVs that need backing up.
    count = 1
    buList = []
    for pv in pvs:
        hold = [pv[4:].split(':')]
        for prop in props:
            if dev:
                hold.append('devIOC:ai'+str(count))
            else:
                hold.append(pv+':'+prop)
            count += 1
        buList.append(hold)

    # title of backup file.
    title = inFile.split('/')[-1].replace('-',' ')[:inFile.find('-list.opi')]

    bu.append('# Detector: '+title)
    bu.append('# chid\tgroup\tcrate\tslot\tchannel\tV0Set\tI0Set\tSVMax\t\
RUp\tRDwn')

    # performs caget_many function for every list element of buList
    count = 0
    for pv in buList:
        ch = '\t'.join(map(str,map(int,pv[0])))
        chid = ids[maps.index(ch)]
        line = chid+'\t'+group+'\t'+ch+'\t'
        res = epics.caget_many(pv[1:],as_string=True)
        line += '\t'.join(res)
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
print('BACKUP COMPLETE\n'+outFile+' created.')


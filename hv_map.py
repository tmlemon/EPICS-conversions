#!/usr/bin/env python

# Date:		January 28, 2019
# Author:	Tyler Lemon

#Change log:
# Date,	Changed by:,	Change
#2019-01-28,	Tyler Lemon,	Completion of initial development


# "hv_map.py" replicates TCL/TK's perl script of the same name used by
# Hall C to create group_map, channel_map, and HV.alhConfig files from HV.hvc.
# Resulting files of this python program are same as perl script with the
# exception of 1.) crate and group headers in channel_map and group_map were 
# changed to fit entire group name and fix spacing issues and 
# 2.) In .alhConfig file, channels are listed in increasing numerical order
# (side effect of reusing logic used to split crates and channels up).

import sys # used to check input arguements and exit program on error
import os # used to check whether .hvc and .group file exist
import array # used to count number of channels in each group
from math import ceil # used to calculate number of pages in output files.
from datetime import datetime # used to get timestamp for page headers



# Checks if there are any input arguements, assigns prefix and spec if so.
if len(sys.argv)-1 == 0:
	prefix,spec = 'HV','Hall C'
elif len(sys.argv)-1 == 1:
	prefix,spec = sys.argv[1],'Hall C'
elif len(sys.argv)-1 >= 2:
	prefix,spec = sys.argv[1],sys.argv[2]

# Declares input configuration files and output file name
hvConfig = prefix+'.hvc'
groupFile = prefix+'.group'
alhFile = prefix+'.alhConfig'

# Tries to open .hvc file, gives warning and exits if cannot.
try:
	with open(hvConfig,'r') as f:
		configLines = f.readlines()
except:
	print('Cannot open config file: '+hvConfig+'.\n')
	sys.exit(0)

# Reads in HV.hvc, prints crate numbers, checks channels for duplication.
chs,used,prevCrate,groups,labels = [],[],[],array.array('i'),[]
for line in configLines:
	if line[0] != '#' and line[0] != '\n':
		label,crate,slot,channel,group = line.strip().split()[:5]
		labels.append(label)
		chs.append([label,crate,slot,channel,group])
		groups.append(int(group))
		if crate not in prevCrate:
			prevCrate.append(crate)
			print('Found new crate... number '+crate)
		if [crate,slot,channel.zfill(2)] not in used:
			used.append([crate,slot,channel.zfill(2)])
		else:
			print('>>>'+'\033[1m'+'\tMultiply assigned HV channel!'+'\033[0m'+\
				'\n>>>\tCrate/Slot/Channel '+crate+'/'+slot+'/'+channel+\
				' already assigned to '+'\033[1m'+\
				chs[used.index([crate,slot,channel])][0]+'\033[0m'+\
				'.\n>>>\tAttempted assignment to '+'\033[1m'+label+'\033[0m'+\
				' has been ignored.\n>>>')

# Reads in HV.group and prints each group with ID number and number of channels
if (os.path.isfile(groupFile)):
	print('Opening group file '+groupFile)
	try:
		with open(groupFile,'r') as f:
			groupLines = f.readlines()
	except:
		print('Cannot open config file: '+groupFile+'.\n')
		sys.exit(0)
print('Group Information:')
grNames = []
for line in groupLines:
	if line[0] != '#' and line[0] != '\n':
		grID = line.strip().split(' ')[0]
		grName = ' '.join(line.strip().split(' ')[1:])
		grNames.append([grID,grName])
		print('\tGroup '+grName+' (id '+grID+')'+' has '+\
			str(groups.count(int(grID)))+' channels')


# Creates group_map file
date = datetime.now().strftime('%X %a %b %d %Y')
pgHeader = ('Group Contents Map Generated '+date).center(80)[:len((\
	'Group Contents Map Generated '+date).center(80))-len('Page:N')]+'Page:'

groupLines.sort()

mapping = []
for group in groupLines:
	grID = group.strip().split(' ')[0]
	grName = ' '.join(group.strip().split(' ')[1:])
	if len(grName) > 18:
		hold = ['_'*19+'|',('Group '+grID).center(19)+'|',\
			grName[:18].center(19)+'|',grName[18:].center(19)+'|',\
			'_'*19+'|',' '*19+'|']
	else:
		hold = ['_'*19+'|',('Group '+grID).center(19)+'|',\
			grName.center(19)+'|',' '*19+'|','_'*19+'|',' '*19+'|']
	for ch in chs:
		chID,cr,sl,chn,gr = ch
		chn = chn.zfill(2)
		if gr == str(grID):
			spacing = 17-len(chID)-len(cr+'/'+sl+'/'+chn)
			line = ' '+chID+' '*spacing+cr+'/'+sl+'/'+chn+' |'
			if len(line) > 20:
				line = line[: -2]+'|'
			hold.append(line)
	hold.append(' '*19+'|')
	mapping.append(hold)

numPgs = int(ceil(len(groupLines)/4.0))
start,final = 0,[]
for page in range(0,numPgs):
	pg = mapping[start*page:start*page+4]
	maxLen = 0
	for item in pg:
		if len(item) > maxLen:
			maxLen = len(item)
	for i,item in enumerate(pg):
		if len(item) < maxLen:
			diff = maxLen - len(item)
			for q in range(0,diff):
				pg[i].append(' '*19+'|')
	start += 4
	if page != 0:
		final.append('\f')
	final.append(pgHeader+str(page+1))
	for i in range(0,len(pg[0])):
		line = '|'	
		for grp in pg:
			line += grp[i]
		final.append(line)

with open('group_map','w') as f:
	for line in final:
		f.write(line)
		f.write('\n')


# Creates channel_map file
labels = [x for _,x in sorted(zip(used,labels))]
used.sort()

chMap = []
maxSl = maxCh = 0
for crate in prevCrate:
	hold = []
	for ch in used:
		if ch[0] == crate:
			hold.append(ch)
		if int(ch[2]) > maxCh:
			maxCh = int(ch[2])
		if int(ch[1]) > maxSl:
			maxSl = int(ch[1])
	chMap.append(hold)

pgHeader = ('Channel Map Generated '+date).center(80)[:len((\
	'Channel Contents Map Generated '+date).center(80))-len('Page:N')]+'Page:'
crateMap = []
for crNum,crate in enumerate(chMap):
	hold = ['_'*19+'|',('Crate '+str(crNum+1)).center(19)+'|','_'*19+'|',]
	for slot in range(0,maxSl+1):
		for ch in range(0,maxCh+1):
			chInfo = str(slot)+'/'+str(ch).zfill(2)
			try:
				chID = labels[used.index([str(crNum+1),str(slot),\
					str(ch).zfill(2)])]
				hold.append(' '+chInfo.ljust(6)+chID.center(12)+'|')
			except:
				hold.append((' '+chInfo).ljust(19)+'|')
	crateMap.append(hold)

numPgs = int(ceil(len(crateMap)/4.0))
start,final = 0,[]
for page in range(0,numPgs):
	pg = crateMap[start*page:start*page+4]
	start += 4
	if page != 0:
		final.append('\f')
	final.append(pgHeader+str(page+1))
	for i in range(0,len(pg[0])):
		line = '|'	
		for grp in pg:
			line += grp[i]
		final.append(line)

with open('channel_map','w') as f:
	for line in final:
		f.write(line)
		f.write('\n')


# Creates .alhConfig file
specNoSpace = spec.replace(' ','_')
final = 'GROUP    NULL'+' '*15+specNoSpace+'\n'+'$ALIAS '+spec+\
	' Detector High Voltage\n\n'
for grp in groupLines:
	grID = grp.strip().split(' ')[0]
	name = ' '.join(grp.strip().split(' ')[1:])
	nameNoSpace = name.replace(' ','_')
	final += 'GROUP    '+specNoSpace+' '*15+nameNoSpace+'\n'+'$ALIAS '+\
		name+'\n\n'
	for ch in chs:
		if ch[4] == grID:
			pvBase = 'hchv'+ch[1]+':'+ch[2].zfill(2)+':'+ch[3].zfill(3)
			final+= 'CHANNEL  '+nameNoSpace+' '*18+pvBase+':VDiff\n'+\
				'$ALIAS '+ch[0]+' '+ch[1]+'/'+ch[2]+'/'+ch[3].zfill(2)+\
				'\n'+'$COMMAND  edm -noautomsg -eolc -x -m "sig='+\
				pvBase+',title='+ch[0]+',address='+ch[1]+'/'+ch[2]+'/'+\
				ch[3].zfill(2)+'" HV_alarm_set.edl >> /dev/null\n\n'

with open(alhFile,'w') as f:
	f.write(final)

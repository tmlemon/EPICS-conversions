#!/usr/env python

import sys # used to check input arguements and exit program on error
import os # used to check whether .hvc and .group file exist
import array # used to count number of channels in each group
from math import ceil # used to calculate number of pages in output files.
from datetime import datetime # used to get timestamp for page headers

alhOnly = False
outPath = ''

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
			if not alhOnly:
				print('Found new crate... number '+crate)
		if [crate,slot,channel.zfill(2)] not in used:
			used.append([crate,slot,channel.zfill(2)])
		else:
			print('>>>'+'\033[1m'+'\tMultiply assigned HV channel!'+\
				'\033[0m'+'\n>>>\tCrate/Slot/Channel '+crate+'/'+\
				slot+'/'+channel+' already assigned to '+'\033[1m'+\
				chs[used.index([crate,slot,channel])][0]+'\033[0m'+\
				'.\n>>>\tAttempted assignment to '+'\033[1m'+label+\
				'\033[0m'+' has been ignored.\n>>>')

# Reads in HV.group and prints each group with ID number and number of
# channels
if (os.path.isfile(groupFile)):
	if not alhOnly:
		print('Opening group file '+groupFile)
	try:
		with open(groupFile,'r') as f:
			groupLines = f.readlines()
	except:
		print('Cannot open config file: '+groupFile+'.\n')
		sys.exit(0)
if not alhOnly:
	print('Group Information:')
grNames = []
for line in groupLines:
	if line[0] != '#' and line[0] != '\n':
		grID = line.strip().split(' ')[0]
		grName = ' '.join(line.strip().split(' ')[1:])
		grNames.append([grID,grName])
		if not alhOnly:
			print('\tGroup '+grName+' (id '+grID+')'+' has '+\
				str(groups.count(int(grID)))+' channels')


# Creates group_map file
date = datetime.now().strftime('%X %a %b %d %Y')
pgHeader = ('Group Contents Map Generated '+date).center(87)[:len((\
	'Group Contents Map Generated '+date).center(87))-len('Page:N')]+\
    'Page:'

groupLines.sort()

mapping = []
for group in groupLines:
	grID = group.strip().split(' ')[0]
	grName = ' '.join(group.strip().split(' ')[1:])
	if len(grName) > 18:
		hold = ['_'*21+'|',('Group '+grID).center(21)+'|',\
			grName[:18].center(21)+'|',grName[18:].center(21)+'|',\
			'_'*21+'|',' '*21+'|']
	else:
		hold = ['_'*21+'|',('Group '+grID).center(21)+'|',\
			grName.center(21)+'|',' '*21+'|','_'*21+'|',' '*21+'|']
	for ch in chs:
		chID,cr,sl,chn,gr = ch
		chn = chn.zfill(2)
		if gr == str(grID):
			spacing = 19-len(chID)-len(cr+'/'+sl+'/'+chn)
			line = ' '+chID+' '*spacing+cr+'/'+sl+'/'+chn+' |'
			hold.append(line)
	hold.append(' '*21+'|')
	mapping.append(hold)


numPgs = int(ceil(len(groupLines)/4.0))
final = []
for page in range(0,numPgs):
	pg = mapping[4*page:4*page+4]
	maxLen = 0
	for item in pg:
		if len(item) > maxLen:
			maxLen = len(item)
	for i,item in enumerate(pg):
		if len(item) < maxLen:
			diff = maxLen - len(item)
			for q in range(0,diff):
				pg[i].append(' '*21+'|')
	if page != 0:
		final.append('\f'+pgHeader+str(page+1))
	else:
		final.append(pgHeader+str(page+1))

	for i in range(0,len(pg[0])):
		line = '|'
		for grp in pg:
			line += grp[i]
		final.append(line)

'''
if not alhOnly:
	with open(outPath+'group_map','w') as f:
		for line in final:
			f.write(line)
			f.write('\n')
'''

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
prevCrate.sort()

pgHeader = ('Channel Map Generated '+date).center(87)[:len((\
	'Channel Contents Map Generated '+date).center(87))-\
	len('Page:N')]+'Page:'
crateMap = []

'''
for crNum,crate in enumerate(chMap):
	hold = ['_'*21+'|',('Crate '+str(crNum+1)).center(21)+'|','_'*21+'|',]
	for slot in range(0,maxSl+1):
		for ch in range(0,maxCh+1):
			chInfo = str(slot)+'/'+str(ch).zfill(2)
			try:
				chID = labels[used.index([str(crNum+1),str(slot),\
					str(ch).zfill(2)])]
				hold.append(' '+chInfo.ljust(6)+chID.center(14)+'|')
			except:
				hold.append((' '+chInfo).ljust(21)+'|')
	crateMap.append(hold)
'''

for i,crNum in enumerate(prevCrate):
	crate = chMap[i]
	hold = ['_'*21+'|',('Crate '+crNum).center(21)+'|','_'*21+'|',]
	for slot in range(0,maxSl+1):
		for ch in range(0,maxCh+1):
			chInfo = str(slot)+'/'+str(ch).zfill(2)
			try:
				chID = labels[used.index([crNum,str(slot),\
					str(ch).zfill(2)])]
				hold.append(' '+chInfo.ljust(6)+chID.center(14)+'|')
			except:
				hold.append((' '+chInfo).ljust(21)+'|')
	crateMap.append(hold)

numPgs = int(ceil(len(crateMap)/4.0))
final = []
for page in range(0,numPgs):
	pg = crateMap[4*page:4*page+4]
	if page != 0:
		final.append('\f'+pgHeader+str(page+1))
	else:
		final.append(pgHeader+str(page+1))
	for i in range(0,len(pg[0])):
		line = '|'
		for grp in pg:
			line += grp[i]
		final.append(line)

if not alhOnly:
	with open(outPath+'channel_map','w') as f:
		for line in final:
			f.write(line)
			f.write('\n')
'''
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

with open(outPath+alhFile,'w') as f:
	f.write(final)
'''

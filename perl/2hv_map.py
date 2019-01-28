#!/usr/env python

# Date:		January 18, 2019
# Author:	Tyler Lemon

# "hv_map.py" is an attempt to recreate perl script of the same name used by
# Hall C to create group_map, channel_map, and HV.alhConfig files from HV.hvc.

import sys
import os
import array
from datetime import datetime, timedelta
import pytz
import math


if len(sys.argv)-1 == 0:
	prefix,spec = 'HV','Hall C'
elif len(sys.argv)-1 == 1:
	prefix,spec = sys.argv[1],'Hall C'
elif len(sys.argv)-1 >= 2:
	prefix,spec = sys.argv[1],sys.argv[2]

hvConfig = prefix+'.hvc'
groupFile = prefix+'.group'
alhFile = prefix+'.alhConfig'

try:
	with open(hvConfig,'r') as f:
		configLines = f.readlines()
except:
	print('Cannot open config file: '+hvConfig+'.\n')
	sys.exit(0)

#reads in HV.hvc, prints crate numbers, checks channels for duplication.
chs,used,prevCrate,groups = [],[],[],array.array('i')
for line in configLines:
	if line[0] != '#' and line[0] != '\n':
		label,crate,slot,channel,group = line.strip().split()[:5]
		chs.append([label,crate,slot,channel,group])
		groups.append(int(group))
		if crate not in prevCrate:
			prevCrate.append(crate)
			print('Found new crate... number '+crate)
		if [crate,slot,channel] not in used:
			used.append([crate,slot,channel])
		else:
			print('>>>'+'\033[1m'+'\tMultiply assigned HV channel!'+'\033[0m'+\
				'\n>>>\tCrate/Slot/Channel '+crate+'/'+slot+'/'+channel+\
				' already assigned to '+'\033[1m'+\
				chs[used.index([crate,slot,channel])][0]+'\033[0m'+\
				'.\n>>>\tAttempted assignment to '+'\033[1m'+label+'\033[0m'+\
				' has been ignored.\n>>>')

#reads in HV.group and prints each group with ID number and number of channels
if (os.path.isfile(groupFile)):
	print('Opening group file '+groupFile)
	try:
		with open(groupFile,'r') as f:
			groupLines = f.readlines()
	except:
		print('Cannot open config file: '+groupFile+'.\n')
		sys.exit(0)
print('Group Information:')
for line in groupLines:
	if line[0] != '#' and line[0] != '\n':
		grID = line.strip().split(' ')[0]
		grName = ' '.join(line.strip().split(' ')[1:])
		print('\tGroup '+grName+' (id '+grID+')'+' has '+\
			str(groups.count(int(grID)))+' channels')

if pytz.utc.localize(datetime.utcnow()).astimezone(pytz.timezone('US/Eastern'))\
.dst() != timedelta(0):
	timezone = 'EDT'
else:
	timezone = 'EST'
date = datetime.now().strftime('%a %b %d %X '+timezone+' %Y')
pgHeader = ('Group Contents Map Generated '+date).center(80)[:len((\
	'Group Contents Map Generated '+date).center(80))-len('Page:N')]+'Page:'

#!/usr/bin/perl

# 
#
#      File:        hv_map.perl
#
#      Description: Hall C PERL script to list HV channel assignments 
#                   sorted by CAEN crate/channel and by group.
#
#      Function: To generate a human-readable list of high voltage
#                channel assignments by crate/channelas well as by 
#                group to which they belong. The main purpose
#                of this listing is forseen to be by anyone who has to
#                work with the cables as they break out of the HV
#                distribution patch panels or CAEN power supplies.
#
#      Change History:
#
#      Revision    Date    Engineer    Comments
#      1.0         15Apr99 H. Fenker    First issue.

#      1.0.1       28Mar01 V. Papavassiliou  Changed #!/usr/bin/perl
#                                            to #!/apps/bin/perl 
#      1.0.2       29.3.2001 saw       Tweak  previous fix
#
#      1.0.3       19.5.2003 hcf       fix bug that suppressed final crate info printout
# Definitions.


# associative array, links group id with number of channels.
%GROUP_SIZE;

# decode options. -q = quiet mode.
### looks at users arguements. if one arguement is given, file looks for
### "arg1".hvc, if two program looks for arg1.hvc and sets spec to arg2 for use
### in ALH config naming header
$spec = "Hall C";
if($ARGV[0]) {
   $prefix = $ARGV[0];
   if($ARGV[1]) {
       $spec = $ARGV[1];
   }
} else {
   $prefix = "HV";
}



# File Definitions.
$hv_cnfg  =   "$prefix".".hvc";
$group_file = "$prefix".".group";
$alh_file = "$prefix".".alhConfig";

# output file(s) dependent upon hv config file. They are
# defined later.

$status= 0; # this will be our exit status for the calling process.

# ********************************************************************

# Open HV Config File.
open(HV,"<$hv_cnfg")|| die "Cannot open config file: $hv_cnfg.\n  $! \n";


# find the number of groups, and the number of channels per group.
open(HV,$hv_cnfg)|| die "Cannot open config file: $hv_cnfg.\n  $! \n";

@crate_list=();
%sections={};
while ($input=<HV>) {
    # remove comments from rf_config.dat
    chomp $input;
    ($string,$rest) = split(/\#/,$input,2);
    if($string ne "")
    {
	# decode label, crate, channel and group
#	$string=~s/^\s*//;
	($label,$crate,$slot,$channel,$group,$rest)=split(' ',$string,6);
	$label=~s/\s//g;
	$crate=~s/\s//g;
	$slot=~s/\s//g;
	$channel=~s/\s//g;
	$identity= sprintf  "%-9s %2d/%1d/%2.2d",$label,$crate,$slot,$channel;

#
# Do some storage based on group assignment of this item
#
	$new=1;
	foreach $group_num (sort(keys %GROUP_SIZE))
	{
	    if($group_num==$group)
	    {
		# group has an entry in array, increment counter
		$GROUP_SIZE{$group_num}++;
		$new=0;
	    }
	}
	if($new)
	{
	    # new group, add to array
	    $GROUP_SIZE{$group}=1;
	}
	
   # Whether new group or existing one, add this item to the group's content list
	$group_contents{$group}[$GROUP_SIZE{$group}]= $identity;

#
# Do some storage based on crate/channel assignment of this item
#
	$new=1;
#	foreach $cr (@crate_list) {
#	    if($cr==$crate) {
#		$new = 0;
#	    }
#	}
	for ($cid=0; $cid <= $#crate_list; $cid++) {
	    $cr = $crate_list[$cid];
	    if($cr == $crate) {
		$new = 0;
	    }
	}
	if($new) {
	    # new crate, add it to the array
	    $cid = $#crate_list+1;
	    $crate_list[$cid] = $crate;
	    print "Found new crate.. number $crate\n";
	    $sections{$crate} =1;
	}
	if( $slot > 3) {
	    $sections{$crate} = 3;
	}
	
	# store assignment by crate/channel address...
	# ...after checking to make sure this channel is not already used.
	if ($crate_chan[$crate][$slot][$channel]) {
	   $status= 1;
	   print STDERR "\a";
	   print STDERR ">>> Multiply assigned HV channel!!\n";
	   print STDERR ">>>   Crate/Slot/Channel $crate/$slot/$channel \n";
	   print STDERR ">>>        is already assigned to $crate_chan[$crate][$slot][$channel]\n";
	   print STDERR ">>>        attempted assignment to $label has been ignored!!\n";
	} else {	
	   $crate_chan[$crate][$slot][$channel] = $label;
	}
    }
}

if( -e $group_file)
  {
  # read group names into array
  print "Opening group file $group_file\n";
  open(NAME,"<$group_file")|| die "Cannot open config file: $group_file.\n  $! \n";
  while($input=<NAME>)
    {
    chomp $input;
    ($id,$name)=split(/[ \t]/,$input,2);
    $GROUP_NAMES{$id}=$name;
    }
  }

# report group data.
print "Group Information:\n";
foreach $key (sort(keys %GROUP_SIZE))
  {
  if($GROUP_NAMES{$key})
    {
    print "    Group $GROUP_NAMES{$key} (id $key) ";
    print "has $GROUP_SIZE{$key} channels\n";
    }
  else
    {
    print "    Group $key has $GROUP_SIZE{$key} channels\n";
    }
  }


#---
# Report channel assignments by group membership
open (GRP,'>group_map') || die "failed to open hv group output file\n";

# Sort by Group Number and print four Groups per page with some
# identifying remarks at the top.

@groups= sort (keys %GROUP_SIZE);
foreach $group (@groups) {
  @{$group_contents_in_order{$group}}= sort (@{ $group_contents{$group} } );
}

$left_col=$rite_col=$page=0;
#print "Number of groups: $#groups\n";
while ($left_col <= $#groups) {
   $rite_col=$left_col+3;
   if ($rite_col > $#groups) {$rite_col= $#groups;}
   
   $page++;
   if ($left_col) {print GRP "\f";}  #new page
   $date= `date`; chomp $date;
   print GRP "     Group Contents Map Generated $date           Page:$page\n";
   printf GRP "|";
   foreach $group (@groups[$left_col..$rite_col]) {
      printf GRP  "___________________|";
      }
   printf GRP "\n";
#-------------------------------------   
   printf GRP "|";
   foreach $group (@groups[$left_col..$rite_col]) {
      printf GRP  "    Group %3d      |",$group;				#Group Number
      }
   printf GRP "\n";
#-------------------------------------   
   printf GRP "|";
   foreach $group (@groups[$left_col..$rite_col]) {
      printf GRP  " %-18.18s|",$GROUP_NAMES{$group};		#Group Name
      }
   printf GRP "\n";
#-------------------------------------   
   printf GRP "|";
   foreach $group (@groups[$left_col..$rite_col]) {
      printf GRP  "___________________|";
      }
   printf GRP "\n";
#-------------------------------------
   @length= (values %GROUP_SIZE);
   @length= @length[ $left_col..$rite_col ];
   @length= sort @length;
   $maxlen=  @length[-1];
   for ($ch=0; $ch<=$maxlen; $ch++) {  #for hysterical reasons, index goes 1..max. 0 is empty
      printf GRP "|";
      foreach $group (@groups[$left_col..$rite_col]) {
         printf GRP  " %-18.18s|", $group_contents_in_order{$group}[$ch];
      }
      printf GRP "\n";
      }
   $left_col+=4;
}
close GRP;






#---
# Report channel assignments by crate/channel
open (GEO,'>channel_map') || die "failed to open hv geo output file\n";

# Sort by Crate Number and print four crates per page with some
# identifying remarks at the top.


$left_col=$rite_col=$page=0;
@crate_order = ();
@sectionnum = ();
foreach $cr (sort @crate_list) {
    $nsec = $sections{$cr};
    $nsections += $nsec;
    for($sec=0;$sec<$nsec;$sec++) {
	$cid =  $#crate_order+1;
	$crate_order[$cid] = $cr;
	if($nsec == 1) {
	    $sectionnum[$cid] = 0;
	} else {
	    $sectionnum[$cid] = $sec+1;
	}
    }
}
while ($left_col < $nsections) {
   $rite_col=$left_col+3;
   if ($rite_col >= $nsections) {$rite_col= $nsections-1;}
   
   $page++;
   if ($left_col) {print GEO "\f";}  #new page
   $date= `date`; chomp $date;
   print GEO "     Channel Map Generated $date                   Page:$page\n";
   printf GEO "|";
   foreach $cr (@crate_order[$left_col..$rite_col]) {
      printf GEO  "_________________| ";
      }
   printf GEO "\n";
   printf GEO "|";
   foreach $cr ( @crate_order[$left_col..$rite_col]) {
      printf GEO  "   Crate %3d     | ",$cr;
      }
   printf GEO "\n";
   printf GEO "|";
   foreach $cr ( @crate_order[$left_col..$rite_col]) {
      printf GEO  "_________________| ";
      }
   printf GEO "\n";
   for ($line = 0; $line <64; $line++) {
       printf GEO "|";
       for ($column = $left_col;$column<=$rite_col;$column++) {
	   $cr = $crate_order[$column];
	   $secnum = $sectionnum[$column];
	   if($secnum == 0) {	# SY403
	       $sl = int($line/16);
	       $ch = $line%16;
	   } else {		# SY4527 with double width cards
	       $index = ($secnum-1)*64+$line;
	       $sl = 2*int($index/24);
	       $ch = $index%24;
	   }
	   printf GEO  " %1d/%2.2d %9s  | ", $sl, $ch, $crate_chan[$cr][$sl][$ch];
       }
       printf GEO "\n";
   }
   $left_col+=4;
}
close GEO;

#
# Write an alarm handler config file
#
open (ALH,">$alh_file") || die "failed to open alarm handler output file\n";

$spec_nospace = $spec;
$spec_nospace =~ s/ /_/g;

print ALH "GROUP    NULL               $spec_nospace\n";
print ALH "\$ALIAS $spec Detector High Voltage\n\n";

foreach $group (@groups) {
    $groupname = $GROUP_NAMES{$group};
    $groupname_nospace = $groupname;
    $groupname_nospace =~ s/ /_/g;
    print ALH "GROUP    $spec_nospace               $groupname_nospace\n";
    print ALH "\$ALIAS $groupname\n\n";

    $nchans = $GROUP_SIZE{$group};
    for ($ch = 1; $ch <= $nchans; $ch++) {
	($name,$address) = split(/\s+/,$group_contents_in_order{$group}[$ch]);
	($crate,$slot,$chan) = split(/\//,$address);
	$epics = sprintf("hchv%d:%2.2d:%3.3d", $crate, $slot, $chan);
	print ALH "CHANNEL  $groupname_nospace                  $epics:VDiff\n";
	print ALH "\$ALIAS $name $address\n";
	print ALH "\$COMMAND  edm -noautomsg -eolc -x -m \"sig=$epics,title=$name,address=$address\" HV_alarm_set.edl >> /dev/null\n\n"
    }
}
close ALH;



exit $status;


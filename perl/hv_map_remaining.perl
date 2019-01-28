

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


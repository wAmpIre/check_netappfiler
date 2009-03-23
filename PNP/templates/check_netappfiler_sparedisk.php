<?php
#
# check_netappfiler -s (failed|spare|)disk
#
# RRDtool Options
$opt[1] = "--vertical-label By -l 0 -r --title \"Disks $hostname / $servicedesc\"";
#
#
# Graphen Definitions
$def[1]  = "DEF:total=$rrdfile:$DS[1]:AVERAGE "; 
$def[1] .= "DEF:active=$rrdfile:$DS[2]:AVERAGE "; 
$def[1] .= "DEF:spare=$rrdfile:$DS[3]:AVERAGE "; 
$def[1] .= "DEF:failed=$rrdfile:$DS[4]:AVERAGE "; 

$def[1] .= "LINE1:total#000000:\"Total\: \" ";
$def[1] .= "GPRINT:total:LAST:\"%3.0lf%S\\n\" ";

$def[1] .= "AREA:active#0000ffee:\"Active\:\" ";
$def[1] .= "GPRINT:active:LAST:\"%3.0lf%S\\n\" ";

$def[1] .= "AREA:spare#77ff77cc:\"Spare\: \":STACK ";
$def[1] .= "GPRINT:spare:LAST:\"%3.0lf";
if($WARN[3] != "") {
	$def[1] .= ", WARN on ".$WARN[3].", CRIT on ".$CRIT[3]."\\n\" ";
} else {
	$def[1] .= "\\n\" ";
}

$def[1] .= "AREA:failed#ff3333:\"Failed\:\":STACK ";
$def[1] .= "GPRINT:failed:LAST:\"%3.0lf ";
if($WARN[4] != "") {
	$def[1] .= ", WARN on ".$WARN[4].", CRIT on ".$CRIT[4]."\\n\" ";
} else {
	$def[1] .= "\\n\" ";
}

$def[1] .= "LINE1:total#000000 ";

?>

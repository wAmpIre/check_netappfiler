<?php
#
# check_netappfiler -s vol
#
# RRDtool Options
# $opt[1] = "--vertical-label By -l 0 -u $MAX[1] --title \"Volume  $hostname / $servicedesc\" ";
$opt[1] = "--vertical-label By -l 0 -r --title \"Volume  $hostname / $servicedesc\" --height=200 -b 1024 ";
#
#
# Graphen Definitions
$def[1]  = "DEF:data=$rrdfile:$DS[1]:AVERAGE "; 
$def[1] .= "DEF:snap=$rrdfile:$DS[2]:AVERAGE "; 
$def[1] .= "DEF:datatotal=$rrdfile:$DS[3]:AVERAGE "; 
$def[1] .= "DEF:snaptotal=$rrdfile:$DS[4]:AVERAGE "; 

$def[1] .= "CDEF:snapsnap=snap,snaptotal,GT,snaptotal,snap,IF ";
$def[1] .= "CDEF:snapfree=snap,snaptotal,GT,0,snaptotal,snap,-,IF ";
$def[1] .= "CDEF:snapover=snap,snaptotal,GT,snaptotal,snap,-,0,IF ";
$def[1] .= "CDEF:datafree=datatotal,data,- ";

$def[1] .= "CDEF:warn=data,0,*,$WARN[1],+ ";
$def[1] .= "CDEF:crit=data,0,*,$CRIT[1],+ ";

$def[1] .= "AREA:data#aaaaaa:\"Data\: Used space\" "; 
$def[1] .= "GPRINT:data:LAST:\"%6.2lf%S\\n\" ";
$def[1] .= "AREA:datafree#00ff00:\"Data\: Free space\":STACK ";
$def[1] .= "GPRINT:datafree:LAST:\"%6.2lf%S\\n\" ";
$def[1] .= "AREA:snapover#aa0000:\"Snap\: Over resv.\":STACK ";
$def[1] .= "GPRINT:snapover:LAST:\"%6.2lf%S\\n\" ";
$def[1] .= "AREA:snapfree#00ffff:\"Snap\: Free space\":STACK ";
$def[1] .= "GPRINT:snapfree:LAST:\"%6.2lf%S\\n\" ";
$def[1] .= "AREA:snap#0000cc:\"Snap\: Used space\":STACK ";
$def[1] .= "GPRINT:snap:LAST:\"%6.2lf%S\\n\" ";

$def[1] .= "LINE1:datatotal#000000 "; 

$def[1] .= "LINE2:datafree#ffffff:\"Available space \": ";
$def[1] .= "GPRINT:datafree:LAST:\"%6.2lf%S\\n\" ";

if ($WARN[1] != "") {
	$def[1] .= "LINE1:warn#ffff00:\"Warning at      \" ";
	$def[1] .= "GPRINT:warn:LAST:\"%6.2lf%S\\n\" ";
}
if ($CRIT[1] != "") {
	$def[1] .= "LINE1:crit#ff0000:\"Critical at     \" ";
	$def[1] .= "GPRINT:crit:LAST:\"%6.2lf%S\\n\" ";
}

#$def[1] .= "LINE1:$MAX[1]#000000: ";
#$def[1] .= "LINE1:var1#00cc00: "; 
#$def[1] .= "HRULE:$MAX[1]#003300:\"Size $MAX[1] By \" ";
# $def[1] .= "HRULE:$WARN[1]#ffff00:\"Warning on $WARN[1] By \" ";
# $def[1] .= "HRULE:$CRIT[1]#ff0000:\"Critical on $CRIT[1] By \\n\" ";       
#$def[1] .= "GPRINT:var1:LAST:\"%6.2lf By of $MAX[1] By used \\n\" ";
#$def[1] .= "GPRINT:var1:MAX:\"%6.2lf By max used \\n\" ";
#$def[1] .= "GPRINT:var1:AVERAGE:\"%6.2lf By avg used\" ";
?>

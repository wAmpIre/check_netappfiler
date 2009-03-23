<?php
#
# check_netappfiler -s vol
#
# RRDtool Options
$opt[1] = "--vertical-label By -l 0 -r --title \"Volume  $hostname / $servicedesc\" --height=200 -b 1024 ";
#
#
# Graphen Definitions
$def[1]  = "DEF:data=$rrdfile:$DS[1]:AVERAGE "; 
$def[1] .= "DEF:snap=$rrdfile:$DS[2]:AVERAGE "; 
$def[1] .= "DEF:datatotal=$rrdfile:$DS[3]:AVERAGE "; 
$def[1] .= "DEF:snapsize=$rrdfile:$DS[4]:AVERAGE "; 

// $def[1] .= "CDEF:snapsnap=snap,snapsize,GT,snapsize,snap,IF ";
$def[1] .= "CDEF:snapfree=snap,snapsize,GT,0,snapsize,snap,-,IF ";
$def[1] .= "CDEF:snapover=snap,snapsize,GT,snap,snapsize,-,0,IF ";
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

?>

<?php
#
# check_netappfiler -s cpu
#
# RRDtool Options
$opt[1] = "--vertical-label By -l 0 -r --title \"CPU usage $hostname / $servicedesc\"";
$opt[2] = "--vertical-label \"Context Switches\" -l 0 -r --title \"Context switches $hostname / $servicedesc\"";
#
#
$def[1] = "";
$def[2] = "";

# Graphen Definitions

$def[1] .= "DEF:cpu_avg=$rrdfile:$DS[1]:AVERAGE "; 
$def[1] .= "DEF:cpu_min=$rrdfile:$DS[1]:MIN "; 
$def[1] .= "DEF:cpu_max=$rrdfile:$DS[1]:MAX "; 

$def[2] .= "DEF:cs_avg=$rrdfile:$DS[2]:AVERAGE "; 
$def[2] .= "DEF:cs_min=$rrdfile:$DS[2]:MIN "; 
$def[2] .= "DEF:cs_max=$rrdfile:$DS[2]:MAX "; 


$def[1] .= "AREA:cpu_max#6666ffcc: ";
$def[1] .= "AREA:cpu_min#ffffff ";
$def[1] .= "LINE1:cpu_avg#0000ff:\"CPU usage in pct:\" ";
$def[1] .= "GPRINT:cpu_avg:LAST:\"%3.1lf%% \" ";
$def[1] .= "GPRINT:cpu_min:MIN:\"(%3.1lf%% -\" ";
$def[1] .= "GPRINT:cpu_max:MAX:\"%3.1lf%%)\\n\" ";
$def[1] .= "HRULE:$WARN[1]#FFFF00:\"Warning $WARN[1]% \" " ;
$def[1] .= "HRULE:$CRIT[1]#FF0000:\"Critical $CRIT[1]% \" " ;

$def[2] .= "AREA:cs_max#ff6666cc ";
$def[2] .= "AREA:cs_min#ffffff ";
$def[2] .= "LINE1:cs_avg#ff0000:\"Context switches:\" ";
$def[2] .= "GPRINT:cs_avg:LAST:\"%3.1lf%S \" ";
$def[2] .= "GPRINT:cs_min:MIN:\"(%3.1lf%S -\" ";
$def[2] .= "GPRINT:cs_max:MAX:\"%3.1lf%S)\\n\" ";

?>

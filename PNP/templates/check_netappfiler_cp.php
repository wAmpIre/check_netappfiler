<?php
#
# check_netappfiler -s cp
#
# RRDtool Options
$opt[1] = "--vertical-label seconds -l 0 -r --title \"CP ops in progress on $hostname\"";
$opt[2] = "--vertical-label \"Count\" -l 0 -r --title \"Reasons for CP ops on $hostname\"";
#
#
$def[1] = "";
$def[2] = "";

# Graphen Definitions

$def[1] .= "DEF:progress=$rrdfile:$DS[1]:AVERAGE "; 

$def[2] .= "DEF:total=$rrdfile:$DS[2]:AVERAGE "; 
$def[2] .= "DEF:snapshot=$rrdfile:$DS[3]:AVERAGE "; 
$def[2] .= "DEF:lowwater=$rrdfile:$DS[4]:AVERAGE "; 
$def[2] .= "DEF:highwater=$rrdfile:$DS[5]:AVERAGE "; 
$def[2] .= "DEF:logfull=$rrdfile:$DS[6]:AVERAGE "; 
$def[2] .= "DEF:b2b=$rrdfile:$DS[7]:AVERAGE "; 
$def[2] .= "DEF:flush=$rrdfile:$DS[8]:AVERAGE "; 
$def[2] .= "DEF:sync=$rrdfile:$DS[9]:AVERAGE "; 
$def[2] .= "DEF:lowvbuf=$rrdfile:$DS[10]:AVERAGE "; 
$def[2] .= "DEF:deferred=$rrdfile:$DS[11]:AVERAGE "; 
$def[2] .= "DEF:lowdatavecs=$rrdfile:$DS[12]:AVERAGE "; 


$def[1] .= "AREA:progress#6666ffcc: ";
$def[1] .= "LINE1:progress#0000ff:\"Time in progress:\" ";
$def[1] .= "GPRINT:progress:LAST:\"%3.1lfs \" ";

$def[2] .= "LINE2:total#000000:\"Total\:  \" ";
$def[2] .= "AREA:snapshot#ff0000:\"Snapshot\: \" ";
$def[2] .= "AREA:lowwater#0000ff:\"Low water mark\: \":STACK ";
$def[2] .= "AREA:highwater#ccccff:\"High water mark\: \":STACK ";
$def[2] .= "AREA:logfull#00ff00:\"Log full\: \":STACK ";
$def[2] .= "AREA:b2b#ff00ff:\"Back-to-back\: \":STACK ";
$def[2] .= "AREA:flush#00ffff:\"FS flush\: \":STACK ";
$def[2] .= "AREA:sync#ffff00:\"FS sync\: \":STACK ";
$def[2] .= "AREA:lowvbuf#7f7f7f:\"Low vBuffer\: \":STACK ";
$def[2] .= "AREA:deferred#cc0000:\"Deferred\: \":STACK ";
$def[2] .= "AREA:lowdatavecs#ffccff:\"Low data Vecs\: \":STACK ";
$def[2] .= "LINE2:total#000000 ";

?>

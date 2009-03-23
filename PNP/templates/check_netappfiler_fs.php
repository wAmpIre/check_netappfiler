<?php
#
# Copyright (c) 2006-2008 Joerg Linge (http://www.pnp4nagios.org)
# Template for check_disk
# $Id: check_disk.php 367 2008-01-23 18:10:31Z pitchfork $
#
#
# RRDtool Options
$opt[1] = "--vertical-label By -l 0 -u $MAX[1] --title \"Filesystem  $hostname / $servicedesc\" ";
#
#
# Graphen Definitions
$def[1] = "DEF:var1=$rrdfile:$DS[1]:AVERAGE "; 
$def[1] .= "AREA:var1#c6c6c6:\"$servicedesc\\n\" "; 
$def[1] .= "LINE1:var1#00cc00: "; 
$def[1] .= "HRULE:$MAX[1]#003300:\"Size $MAX[1] By \" ";
# $def[1] .= "HRULE:$WARN[1]#ffff00:\"Warning on $WARN[1] By \" ";
# $def[1] .= "HRULE:$CRIT[1]#ff0000:\"Critical on $CRIT[1] By \\n\" ";       
$def[1] .= "GPRINT:var1:LAST:\"%6.2lf By of $MAX[1] By used \\n\" ";
$def[1] .= "GPRINT:var1:MAX:\"%6.2lf By max used \\n\" ";
$def[1] .= "GPRINT:var1:AVERAGE:\"%6.2lf By avg used\" ";
?>

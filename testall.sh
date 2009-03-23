#!/bin/sh
#
# $Id: testall.sh 73 2008-12-22 15:55:30Z svelt $

if [ -z "$1" ]
then
	echo Aufruf: $0 HOSTNAME
	exit 1
fi

for TEST in global cpu environment nvram sparedisk faileddisk cifs-users cifs-stats cluster snapmirror cacheage
do
	./check_netappfiler.py -H $1 -s $TEST
done

for FSIDX in aggr0 /vol/vol0
do
	./check_netappfiler.py -H $1 -s fs -f $FSIDX -w 50 -c 75
done

for FSIDX in `seq 1 8`
do
	./check_netappfiler.py -H $1 -s fs -f $FSIDX -w 50 -c 75
done

for FSIDX in aggr0 /vol/vol0
do
	./check_netappfiler.py -H $1 -s vol -f $FSIDX -w 50% -c 75%
done

for FSIDX in 3 5 7
do
	./check_netappfiler.py -H $1 -s vol -f $FSIDX -w 50% -c 75%
done


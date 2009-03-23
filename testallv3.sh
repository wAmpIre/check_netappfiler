#!/bin/sh
#
# $Id: testallv3.sh 70 2008-12-11 15:00:59Z svelt $

SECNAME=snmpuser
AUTHKEY=dont4get

if [ -z "$1" ]
then
	echo Aufruf: $0 HOSTNAME
	exit 1
fi

for TEST in global cpu environment nvram sparedisk faileddisk cifs-users cifs-stats cluster snapmirror
do
	./check_netappfiler.py -H $1 -P3 -U $SECNAME -A $AUTHKEY -s $TEST
done

for FSIDX in aggr0 /vol/vol0
do
	./check_netappfiler.py -H $1 -P3 -U $SECNAME -A $AUTHKEY -s fs -f $FSIDX -w 50 -c 75
done

for FSIDX in `seq 1 12`
do
	./check_netappfiler.py -H $1 -P3 -U $SECNAME -A $AUTHKEY -s fs -f $FSIDX -w 50% -c 75%
done


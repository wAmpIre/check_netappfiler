#!/usr/bin/env python

# (c) 2006-2009 by Sven Velt, Teamix GmbH
#                  sv@teamix.de

import optparse
import os
import re
import sys

import netsnmp



RETURNSTRINGS = { 0: "OK", 1: "WARNING", 2: "CRITICAL", 3: "UNKNOWN", 127: "UNKNOWN" }
RETURNCODE = { 'OK': 0, 'WARNING': 1, 'CRITICAL': 2, 'UNKNOWN': 3 }

available_subsys = ['global', 'version', 'cpu', 'environment', 'nvram', 'sparedisk', 'faileddisk', 'fs', 'vol', 'cifs-users', 'cifs-stats', 'cluster', 'snapmirror', 'cacheage', 'cp', 'ifstat', 'diskio', 'tapeio', 'ops']

OIDs	= {
		'Uptime':			'.1.3.6.1.2.1.1.3.0',
		'ONTAP_Version':		'.1.3.6.1.4.1.789.1.1.2.0',
		'Model':			'.1.3.6.1.4.1.789.1.1.5.0',

		'CPU_Arch':			'.1.3.6.1.4.1.789.1.1.11.0',
		'CPU_Time_Busy':		'.1.3.6.1.4.1.789.1.2.1.3.0',
		'CPU_Time_Idle':		'.1.3.6.1.4.1.789.1.2.1.5.0',
		'CPU_Context_Switches':		'.1.3.6.1.4.1.789.1.2.1.8.0',

		'Net_RcvdKB':			'.1.3.6.1.4.1.789.1.2.2.2.0',
		'Net_SentKB':			'.1.3.6.1.4.1.789.1.2.2.3.0',
		'Net64_RcvdKB':			'.1.3.6.1.4.1.789.1.2.2.30.0',
		'Net64_SentKB':			'.1.3.6.1.4.1.789.1.2.2.31.0',
		'Net_ifNumber':			'.1.3.6.1.4.1.789.1.22.1.1',
		'Net_ifIndex':			'.1.3.6.1.4.1.789.1.22.1.2.1.1',
		'Net_ifDescr':			'.1.3.6.1.4.1.789.1.22.1.2.1.2',

		'Global_Status':		'.1.3.6.1.4.1.789.1.2.2.4.0',
		'Global_Status_Message':	'.1.3.6.1.4.1.789.1.2.2.25.0',
		'Cache_Age':			'.1.3.6.1.4.1.789.1.2.2.23.0',

		'Env_Temp':			'.1.3.6.1.4.1.789.1.2.4.1.0',
		'Env_Failed_Fans':		'.1.3.6.1.4.1.789.1.2.4.2.0',
		'Env_Failed_Fans_Text':		'.1.3.6.1.4.1.789.1.2.4.3.0',
		'Env_Failed_PowerSup':		'.1.3.6.1.4.1.789.1.2.4.4.0',
		'Env_Failed_PowerSup_Text':	'.1.3.6.1.4.1.789.1.2.4.5.0',
		'NVRAM_Status':			'.1.3.6.1.4.1.789.1.2.5.1.0',

		'CP':				'.1.3.6.1.4.1.789.1.2.6',
		'CP_NV_Full':			'.1.3.6.1.4.1.789.1.2.6.6.0',
		'CP_Totals':			'.1.3.6.1.4.1.789.1.2.6.8.0',
		'CP_FS_Sync':			'.1.3.6.1.4.1.789.1.2.6.10.0',

		'Autosupport_Status':		'.1.3.6.1.4.1.789.1.2.7.1.0',
		'Autosupport_FailedSends':	'.1.3.6.1.4.1.789.1.2.7.4.0',

		'Disks_Total':			'.1.3.6.1.4.1.789.1.6.4.1.0',
		'Disks_Active':			'.1.3.6.1.4.1.789.1.6.4.2.0',
		'Disks_Reconstructing':		'.1.3.6.1.4.1.789.1.6.4.3.0',
		'Disks_ReconstParity':		'.1.3.6.1.4.1.789.1.6.4.4.0',
		'Disks_Scrubbing':		'.1.3.6.1.4.1.789.1.6.4.6.0',
		'Disks_Failed':			'.1.3.6.1.4.1.789.1.6.4.7.0',
		'Disks_Spare':			'.1.3.6.1.4.1.789.1.6.4.8.0',
		'Disks_ZeroDisks':		'.1.3.6.1.4.1.789.1.6.4.9.0',
		'Disks_Failed_Descr':		'.1.3.6.1.4.1.789.1.6.4.10.0',

		'df_Number':			'.1.3.6.1.4.1.789.1.5.6.0',
		'df_FS_Name':			'.1.3.6.1.4.1.789.1.5.4.1.2',
		'df_FS_Mounted_On':		'.1.3.6.1.4.1.789.1.5.4.1.10',
		'df_FS_kBAvail':		'.1.3.6.1.4.1.789.1.5.4.1.5',
		'df_FS_%Used':			'.1.3.6.1.4.1.789.1.5.4.1.6',
		'df_FS_INodeUsed':		'.1.3.6.1.4.1.789.1.5.4.1.7',
		'df_FS_INodeFree':		'.1.3.6.1.4.1.789.1.5.4.1.8',
		'df_FS_%INodeUsed':		'.1.3.6.1.4.1.789.1.5.4.1.9',
		'df_FS_kBTotal_High':		'.1.3.6.1.4.1.789.1.5.4.1.14',
		'df_FS_kBTotal_Low':		'.1.3.6.1.4.1.789.1.5.4.1.15',
		'df_FS_kBUsed_High':		'.1.3.6.1.4.1.789.1.5.4.1.16',
		'df_FS_kBUsed_Low':		'.1.3.6.1.4.1.789.1.5.4.1.17',
		'df_FS_kBAvail_High':		'.1.3.6.1.4.1.789.1.5.4.1.18',
		'df_FS_kBAvail_Low':		'.1.3.6.1.4.1.789.1.5.4.1.19',
		'df_FS_Status':			'.1.3.6.1.4.1.789.1.5.4.1.20',
		'df_FS_Type':			'.1.3.6.1.4.1.789.1.5.4.1.23',
		'df64_FS_kBTotal':		'.1.3.6.1.4.1.789.1.5.4.1.29',
		'df64_FS_kBUsed':		'.1.3.6.1.4.1.789.1.5.4.1.30',
		'df64_FS_kBAvail':		'.1.3.6.1.4.1.789.1.5.4.1.31',

		'License_SnapMirror':		'.1.3.6.1.4.1.789.1.9.19.0',
		'License_NFS':			'.1.3.6.1.4.1.789.1.3.3.1.0',
		'License_CIFS':			'.1.3.6.1.4.1.789.1.7.1.21.0',
		'License_vFiler':		'.1.3.6.1.4.1.789.1.16.1.0',
		'License_FCP':			'.1.3.6.1.4.1.789.1.17.1.0',
		'License_iSCSI':		'.1.3.6.1.4.1.789.1.17.2.0',
		'License_SnapVaultPrimary':	'.1.3.6.1.4.1.789.1.19.9.0',
		'License_SnapVaultSecondary':	'.1.3.6.1.4.1.789.1.19.10.0',
		'License_SIS':			'.1.3.6.1.4.1.789.1.23.1.0',

		'CIFS_Connected_Users':		'.1.3.6.1.4.1.789.1.7.2.9.0',
		'CIFS_Total_Ops':		'.1.3.6.1.4.1.789.1.7.3.1.1.1.0',
		'CIFS_Total_Calls':		'.1.3.6.1.4.1.789.1.7.3.1.1.2.0',
		'CIFS_Bad_Calls':		'.1.3.6.1.4.1.789.1.7.3.1.1.3.0',
		'CIFS_Get_Attrs':		'.1.3.6.1.4.1.789.1.7.3.1.1.4.0',
		'CIFS_Reads':			'.1.3.6.1.4.1.789.1.7.3.1.1.5.0',
		'CIFS_Writes':			'.1.3.6.1.4.1.789.1.7.3.1.1.6.0',
		'CIFS_Locks':			'.1.3.6.1.4.1.789.1.7.3.1.1.7.0',
		'CIFS_Opens':			'.1.3.6.1.4.1.789.1.7.3.1.1.8.0',
		'CIFS_DirOps':			'.1.3.6.1.4.1.789.1.7.3.1.1.9.0',
		'CIFS_Others':			'.1.3.6.1.4.1.789.1.7.3.1.1.10.0',

		'Cluster_Settings':		'.1.3.6.1.4.1.789.1.2.3.1.0',
		'Cluster_State':		'.1.3.6.1.4.1.789.1.2.3.2.0',
		'Cluster_InterconnectStatus':	'.1.3.6.1.4.1.789.1.2.3.8.0',
		'Cluster_CannotTakeOverCause':	'.1.3.6.1.4.1.789.1.2.3.3.0',

		'Snapmirror_On':		'.1.3.6.1.4.1.789.1.9.1.0',
		'Snapmirror_Src':		'.1.3.6.1.4.1.789.1.9.20.1.2',
		'Snapmirror_Dst':		'.1.3.6.1.4.1.789.1.9.20.1.3',
		'Snapmirror_Status':		'.1.3.6.1.4.1.789.1.9.20.1.4',
		'Snapmirror_State':		'.1.3.6.1.4.1.789.1.9.20.1.5',
	}

OID64s	= {
		'Net_InBytes':		[	'.1.3.6.1.4.1.789.1.22.1.2.1.4',
						'.1.3.6.1.4.1.789.1.22.1.2.1.3',
						'.1.3.6.1.4.1.789.1.22.1.2.1.25',],
		'Net_OutBytes':		[	'.1.3.6.1.4.1.789.1.22.1.2.1.16',
						'.1.3.6.1.4.1.789.1.22.1.2.1.15',
						'.1.3.6.1.4.1.789.1.22.1.2.1.31',],
		'Net_InDiscards':	[	'.1.3.6.1.4.1.789.1.22.1.2.1.10',
						'.1.3.6.1.4.1.789.1.22.1.2.1.9',
						'.1.3.6.1.4.1.789.1.22.1.2.1.28',],
		'Net_OutDiscards':	[	'.1.3.6.1.4.1.789.1.22.1.2.1.22',
						'.1.3.6.1.4.1.789.1.22.1.2.1.21',
						'.1.3.6.1.4.1.789.1.22.1.2.1.34',],
		'Net_InErrors':		[	'.1.3.6.1.4.1.789.1.22.1.2.1.12',
						'.1.3.6.1.4.1.789.1.22.1.2.1.11',
						'.1.3.6.1.4.1.789.1.22.1.2.1.29',],
		'Net_OutErrors':	[	'.1.3.6.1.4.1.789.1.22.1.2.1.24',
						'.1.3.6.1.4.1.789.1.22.1.2.1.23',
						'.1.3.6.1.4.1.789.1.22.1.2.1.35',],

		'DiskIO_ReadBytes':	[	'.1.3.6.1.4.1.789.1.2.2.16',
						'.1.3.6.1.4.1.789.1.2.2.15',
						'.1.3.6.1.4.1.789.1.2.2.32',],
		'DiskIO_WriteBytes':	[	'.1.3.6.1.4.1.789.1.2.2.18',
						'.1.3.6.1.4.1.789.1.2.2.17',
						'.1.3.6.1.4.1.789.1.2.2.33',],

		'TapeIO_ReadBytes':	[	'.1.3.6.1.4.1.789.1.2.2.20',
						'.1.3.6.1.4.1.789.1.2.2.19',
						'.1.3.6.1.4.1.789.1.2.2.34',],
		'TapeIO_WriteBytes':	[	'.1.3.6.1.4.1.789.1.2.2.22',
						'.1.3.6.1.4.1.789.1.2.2.21',
						'.1.3.6.1.4.1.789.1.2.2.35',],

		'OPs_NFS':		[	'.1.3.6.1.4.1.789.1.2.2.6',
						'.1.3.6.1.4.1.789.1.2.2.5',
						'.1.3.6.1.4.1.789.1.2.2.27',],
		'OPs_CIFS':		[	'.1.3.6.1.4.1.789.1.2.2.8',
						'.1.3.6.1.4.1.789.1.2.2.7',
						'.1.3.6.1.4.1.789.1.2.2.28',],
		'OPs_HTTP':		[	'.1.3.6.1.4.1.789.1.2.2.10',
						'.1.3.6.1.4.1.789.1.2.2.9',
						'.1.3.6.1.4.1.789.1.2.2.29',],
	}


Enum_CPU_Arch = {
		'1' : 'x86',
		'2' : 'alpha',
		'3' : 'mips',
		'4' : 'sparc',
		'5' : 'amd64_FIXME',
		}
Enum_df_FS_Status = {
		'1' : 'unmounted',
		'2' : 'mounted',
		'3' : 'frozen',
		'4' : 'destroying',
		'5' : 'creating',
		'6' : 'mounting',
		'7' : 'unmounting',
		'8' : 'nofsinfo',
		'9' : 'replaying',
		'10': 'replayed',
		}
Enum_df_FS_Type = {
		'1' : 'traditionalVolume',
		'2' : 'flexibleVolume',
		'3' : 'aggregate',
		}
Enum_NVRAM_Status = {
		'1' : 'ok',
		'2' : 'partiallyDischarged',
		'3' : 'fullyDischarged',
		'4' : 'notPresent',
		'5' : 'nearEndOfLife',
		'6' : 'atEndOfLife',
		'7' : 'unknown',
		'8' : 'overCharged',
		'9' : 'fullyCharged',
		}
Enum_Cluster_Settings = {
		'1' : 'notConfigured',
		'2' : 'enabled',
		'3' : 'disabled',
		'4' : 'takeoverByPartnerDisabled',
		'5' : 'thisNodeDead',
		}
Enum_Cluster_State = {
		'1' : 'dead',
		'2' : 'canTakeover',
		'3' : 'cannotTakeover',
		'4' : 'takeover',
		}
Enum_Cluster_InterconnectStatus = {
		'1' : 'notPresent',
		'2' : 'down',
		'3' : 'partialFailure',
		'4' : 'up',
		}
Enum_Cluster_CannotTakeOverCause = {
		'1' : 'ok',
		'2' : 'unknownReason',
		'3' : 'disabledByOperator',
		'4' : 'interconnectOffline',
		'5' : 'disabledByPartner',
		'6' : 'takeoverFailed',
		}
Enum_Snapmirror_Status = {
		'1' : 'idle',
		'2' : 'transferring',
		'3' : 'pending',
		'4' : 'aborting',
		'5' : 'migrating',
		'6' : 'quiescing',
		'7' : 'resyncing',
		'8' : 'waiting',
		'9' : 'syncing',
		'10': 'in-sync',
		}
Enum_Snapmirror_State = {
		'1' : 'uninitialized',
		'2' : 'snapmirrored',
		'3' : 'broken-off',
		'4' : 'quiesced',
		'5' : 'source',
		'6' : 'unknown',
}
Enum_Licensed = {
		'1' : 'false',
		'2' : 'true',
}


OkWarnCrit = {
		'CpuTimeBusy':			(       None,         80,         90, ),
		'DisksSpare':			(       None,          0,          0, ),
		'DisksFailed':			(       None,          0,          0, ),
		'GlobalStatusCode':		(       (3,),       (4,),      (5,6), ),
		'FailedFans':			(       None,       None,          1, ),
		'FailedPowerSup':		(       None,       None,          1, ),
		'NVRAMStatus':			(      (1,9),    (2,5,8),    (3,4,6), ),
		'ClusterSettings':		(       (2,),   (1,3,4,),       (5,), ),
		'ClusterState':			(     (2,4,),         (),     (1,3,), ),
		'ClusterInterconnectStatus':	(       (4,),       (3,),     (1,2,), ),
		'SnapmirrorState':		(     (2,5,),   (1,4,6,),       (3,), ),
	}

##################################################################################################

def SNMPGET(oid):
	VBoid = netsnmp.Varbind(oid)

	result = netsnmp.snmpget(oid, Version = int(options.version), DestHost=options.host, Community=options.community)[0]

	if result == None:
		back2nagios(RETURNCODE['UNKNOWN'], 'SNMP UNKNOWN: Timeout or no answer from %s' % options.host)

	if options.verb >= 1:
		print "%40s -> %s" %  (oid, result)

	return result

def SNMPWALK(oid):
	VBoid = netsnmp.Varbind(oid)

	result = netsnmp.snmpwalk(oid, Version = int(options.version), DestHost=options.host, Community=options.community)

	if result == None:
		back2nagios(RETURNCODE['UNKNOWN'], 'SNMP UNKNOWN: Timeout or no answer from %s' % options.host)

	if options.verb >= 1:
		print "%40s -> %s" %  (oid, result)

	return result

def get_fsid(fsid):
	# is fs not a number?
	if fsid.isdigit() == False:
		# Strip trailing slash
		if fsid[-1] == '/':
			fsid = fsid[0:-1]

		# Cache Lookup and recheck fsid
		if fsidcache.has_key(fsid):
			newindex = fsidcache[fsid]

			if options.verb >= 2:
				print "Found cached FSID: %s" % newindex

			dfFSName = SNMPGET(OIDs['df_FS_Name'] + "." + str(newindex)).replace('"','')
			if dfFSName[-1] == '/':
				dfFSName = dfFSName[0:-1]

			if dfFSName == fsid:
				if options.verb >= 2:
					print "Cached FSID up2date: %s - %s " % (fsid, newindex)
				return str(newindex)

		# No cache, not found or incorrect: Search for it
		NrOfPaths = int(SNMPGET(OIDs['df_Number']))

		for newindex in range(1,NrOfPaths+1):
			dfFSName = SNMPGET(OIDs['df_FS_Name'] + "." + str(newindex)).replace('"','')
			if dfFSName[-1] == '/':
				dfFSName = dfFSName[0:-1]

			# Update cache
			fsidcache[dfFSName] = newindex

			if dfFSName == fsid:
				break

		if dfFSName == fsid:
			fsid = str(newindex)
		else:
			back2nagios(RETURNCODE['CRITICAL'], 'Volume/Filesystem "%s" not found!' % fsid)

	return fsid

def get_kb_fs(fsid):
	if options.version == '1':
		dfFSkBTotal = long(SNMPGET(OIDs['df_FS_kBTotal_Low'] + "." + fsid))
		dfFSkBUsed  = long(SNMPGET(OIDs['df_FS_kBUsed_Low']  + "." + fsid))
		dfFSkBAvail = long(SNMPGET(OIDs['df_FS_kBAvail_Low'] + "." + fsid))

		if dfFSkBTotal < 0L:
			dfFSkBTotal += 2 ** 32
		if dfFSkBUsed  < 0L:
			dfFSkBUsed  += 2 ** 32
		if dfFSkBAvail  < 0L:
			dfFSkBAvail  += 2 ** 32

		dfFSkBTotal += long(SNMPGET(OIDs['df_FS_kBTotal_High'] + "." + fsid)) * 2L ** 32L
		dfFSkBUsed  += long(SNMPGET(OIDs['df_FS_kBUsed_High']  + "." + fsid)) * 2L ** 32L
		dfFSkBAvail += long(SNMPGET(OIDs['df_FS_kBAvail_High'] + "." + fsid)) * 2L ** 32L

	else:
		dfFSkBTotal = long(SNMPGET(OIDs['df64_FS_kBTotal'] + "." + fsid))
		dfFSkBUsed  = long(SNMPGET(OIDs['df64_FS_kBUsed']  + "." + fsid))
		dfFSkBAvail = long(SNMPGET(OIDs['df64_FS_kBAvail'] + "." + fsid))


	return (dfFSkBTotal, dfFSkBUsed, dfFSkBAvail)

def find_in_table(oid_index, oid_names, wanted):
	index = None
	indexes	= list(SNMPWALK(oid_index))
	names	= list(SNMPWALK(oid_names))

	try:
		index = names.index(wanted)
		index = indexes[index]
	except ValueError:
		pass

	return index

def get64bits(oids, idx):
	if options.version == '1':
		value = long(SNMPGET(oids[0] + "." + idx))
		if value < 0L:
			value += 2 ** 32
		value += long(SNMPGET(oids[1] + "." + idx)) * 2L ** 32L
	else:
		value = long(SNMPGET(oids[2] + "." + idx))

	return value

def back2nagios(retcode, retmsg):
	print 'NETAPP(%s) %s - %s' % (options.subsys, RETURNSTRINGS[retcode], retmsg)
	sys.exit(retcode)

##################################################################################################

parser = optparse.OptionParser()

parser.add_option("-H", "",
		  dest="host",
		  help="Hostname/IP to check",
		  metavar="HOST")
parser.add_option("-P", "",
		  dest="version",
		  help="(SNMP v1/v2c/v3) Protocol version",
		  metavar="1")
parser.add_option("-C", "",
		  dest="community",
		  help="(SNMP v1/v2c)    Community",
		  metavar="public")
parser.add_option("-L", "",
		  dest="seclevel",
		  help="(SNMP v3)        Security level",
		  metavar="AuthNoPriv")
parser.add_option("-a", "",
		  dest="authproto",
		  help="(SNMP v3)        Authentication protocol",
		  metavar="md5")
parser.add_option("-U", "",
		  dest="secname",
		  help="(SNMP v3)        Security name",
		  metavar="snmpuser")
parser.add_option("-A", "",
		  dest="authkey",
		  help="(SNMP v3)        Authentication key/password",
		  metavar="dont4get")
parser.add_option("-s", "",
		  dest="subsys",
		  help="What should be checked",
		  metavar="SUBSYSTEM")
parser.add_option("-f", "",
		  dest="fs",
		  help="FS Index in SNMP tables",
		  metavar="FS")
parser.add_option("-V", "",
		  dest="var",
		  help="Variable name",
		  metavar="FS")
parser.add_option("-w", "",
		  dest="warn",
		  help="WARNING Thresold")
parser.add_option("-c", "",
		  dest="crit",
		  help="CRITICAL Thresold")
parser.add_option("", "--cache",
		  dest="cache",
		  help="Enable FSID caching")
parser.add_option("-v", "",
		  action="count",
		  dest="verb",
		  help="Verbosity, more for more ;-)")

# Setting Defaults
parser.set_defaults(version='1')
parser.set_defaults(community='public')
parser.set_defaults(seclevel='AuthNoPriv')
parser.set_defaults(authproto='md5')
parser.set_defaults(secname='')
parser.set_defaults(authkey='')
parser.set_defaults(subsys='')
parser.set_defaults(fs='0')
parser.set_defaults(var='0')
parser.set_defaults(warn='0')
parser.set_defaults(crit='0')
parser.set_defaults(verb=0)

(options, args) = parser.parse_args()

if options.host == None:
	print "Hey! Please come back with a hostname or IP (-H) !"
	sys.exit(127)

if options.version == '3':
	if options.seclevel != 'AuthNoPriv' and options.seclevel != 'NoAuthNoPriv':
		print "Unknown security level (-L) %s!" % options.seclevel
		sys.exit(127)
	if options.authproto != 'md5' and options.authproto != 'sha':
		print "Unknown authentication protocol (-a) %s!" % options.authproto
		sys.exit(127)
	if options.secname == '' or options.authkey == '':
		print "Please specify security name (-U) and authentication key (-A) with SNMPv3!"
		sys.exit(127)

fsidcache = {}

if options.cache:
	if options.subsys in ['fs', 'vol',]:
		import shelve
		fsidcache = shelve.open(options.cache)

		if options.verb >= 1:
			print 'Loaded FSIDs: %s' % fsidcache





# Get the ONTAP Version
if options.verb >= 1:
	ONTAPver = re.search("NetApp\sRelease\s+([\d.a-zA-Z]+):", SNMPGET(OIDs['ONTAP_Version'])).group(1)
	print 'ONTAP Version: %s' % ONTAPver

	ONTAPver = ONTAPver.split('.')



if options.subsys == 'disk':
	options.subsys = 'sparedisk'

if options.subsys == '' or options.subsys =='global':
	Model = SNMPGET(OIDs['Model'])
	GlobalStatusCode = SNMPGET(OIDs['Global_Status'])
	GlobalStatusMsg = SNMPGET(OIDs['Global_Status_Message'])[:255]
	GlobalStatusCode = int(GlobalStatusCode)

	if GlobalStatusCode in OkWarnCrit['GlobalStatusCode'][0]:
		ReturnCode = RETURNCODE['OK']
	elif GlobalStatusCode in OkWarnCrit['GlobalStatusCode'][1]:
		ReturnCode = RETURNCODE['WARNING']
	elif GlobalStatusCode in OkWarnCrit['GlobalStatusCode'][2]:
		ReturnCode = RETURNCODE['CRITICAL']
	else:
		ReturnCode = RETURNCODE['UNKNOWN']

	options.subsys = 'global'
	ReturnMsg = Model.replace('"','') + ': ' + GlobalStatusMsg.replace('"','')

	if options.verb >= 1:
		print 'Uptime in seconds: %s' % SNMPGET('.1.3.6.1.2.1.1.3.0')
		print 'ONTAP version: %s' % '.'.join(ONTAPver)
		print 'Global system status: %s, %s' % (GlobalStatusCode, GlobalStatusMsg)



elif options.subsys == 'version':
	Model = SNMPGET(OIDs['Model'])
	ONTAPver = re.search("NetApp\sRelease\s+([\d.a-zA-Z]+):", SNMPGET(OIDs['ONTAP_Version'])).group(1).split('.')
	ReturnMsg =  Model.replace('"','') + ': ONTAP version: %s' % '.'.join(ONTAPver)
	ReturnCode = RETURNCODE['OK']



elif options.subsys == 'cpu':
	CpuArch     = SNMPGET(OIDs['CPU_Arch'])
	CpuTimeBusy = int(SNMPGET(OIDs['CPU_Time_Busy']))
	CpuTimeIdle = int(SNMPGET(OIDs['CPU_Time_Idle']))
	CpuCS       = SNMPGET(OIDs['CPU_Context_Switches'])

	LevelWarn = OkWarnCrit['CpuTimeBusy'][1]
	LevelCrit = OkWarnCrit['CpuTimeBusy'][2]
	if options.warn != '0':
		LevelWarn = int(options.warn)
	if options.crit != '0':
		LevelCrit = int(options.crit)

	if CpuTimeBusy > LevelCrit:
		ReturnCode = RETURNCODE['CRITICAL']
	elif CpuTimeBusy > LevelWarn:
		ReturnCode = RETURNCODE['WARNING']
	else:
		ReturnCode = RETURNCODE['OK']

	ReturnMsg  = 'CPU Busy: %s%%, Context Switches: %s, CPU Architecture: %s' % (CpuTimeBusy, CpuCS, Enum_CPU_Arch[CpuArch])
	ReturnMsg += '|nacpu=%s%%;%s;%s;0;100 nacs=%sc' % (CpuTimeBusy, OkWarnCrit['CpuTimeBusy'][1], OkWarnCrit['CpuTimeBusy'][2], CpuCS)



elif options.subsys == 'environment':
	OverTemp          = int(SNMPGET(OIDs['Env_Temp']))
	FailedFans        = int(SNMPGET(OIDs['Env_Failed_Fans']))
	FailedFansMsg     = SNMPGET(OIDs['Env_Failed_Fans_Text'])
	FailedPowerSup    = int(SNMPGET(OIDs['Env_Failed_PowerSup']))
	FailedPowerSupMsg = SNMPGET(OIDs['Env_Failed_PowerSup_Text'])

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = ''

	if OverTemp != 1:
		ReturnCode  = RETURNCODE['WARNING']
		ReturnMsg  += 'System too hot! '

	if FailedFans > OkWarnCrit['FailedFans'][2]:
		ReturnCode  = RETURNCODE['CRITICAL']
		ReturnMsg  += FailedFansMsg + ' '

	if FailedPowerSup > OkWarnCrit['FailedPowerSup'][2]:
		ReturnCode  = RETURNCODE['CRITICAL']
		ReturnMsg  += FailedPowerSupMsg + ' '

	if ReturnCode == RETURNCODE['OK']:
		ReturnMsg = 'Filer is happy with his environment ;-)'



elif options.subsys == 'nvram':
	NVRAMStatus = int(SNMPGET(OIDs['NVRAM_Status']))

	ReturnCode = RETURNCODE['UNKNOWN']

	if NVRAMStatus in OkWarnCrit['NVRAMStatus'][0]:
		ReturnCode = RETURNCODE['OK']
	elif NVRAMStatus in OkWarnCrit['NVRAMStatus'][1]:
		ReturnCode = RETURNCODE['WARNING']
	elif NVRAMStatus in OkWarnCrit['NVRAMStatus'][2]:
		ReturnCode = RETURNCODE['CRITICAL']

	ReturnMsg = 'NVRAM battery status is "%s"' % Enum_NVRAM_Status[str(NVRAMStatus)]



elif (options.subsys == 'sparedisk' or options.subsys == 'faileddisk'):
	DisksTotal          = int(SNMPGET(OIDs['Disks_Total']))
	DisksActive         = int(SNMPGET(OIDs['Disks_Active']))
	DisksReconstructing = int(SNMPGET(OIDs['Disks_Reconstructing']))
	DisksReconstParity  = int(SNMPGET(OIDs['Disks_ReconstParity']))
	DisksScrubbing      = int(SNMPGET(OIDs['Disks_Scrubbing']))
	DisksFailed         = int(SNMPGET(OIDs['Disks_Failed']))
	DisksSpare          = int(SNMPGET(OIDs['Disks_Spare']))
	DisksZeroDisks      = int(SNMPGET(OIDs['Disks_ZeroDisks']))
	DisksFailedDescr    = SNMPGET(OIDs['Disks_Failed_Descr'])

	Reconstructing = DisksReconstructing + DisksReconstParity

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = ''

	if (options.subsys == 'sparedisk'):
		LevelWarn = OkWarnCrit['DisksSpare'][1]
		LevelCrit = OkWarnCrit['DisksSpare'][2]
	elif options.subsys == 'faileddisk':
		LevelWarn = OkWarnCrit['DisksFailed'][1]
		LevelCrit = OkWarnCrit['DisksFailed'][2]
	if options.warn != '0':
		LevelWarn = int(options.warn)
	if options.crit != '0':
		LevelCrit = int(options.crit)


	if DisksScrubbing > 0:
		ReturnMsg += '%s disk(s) are being scrubbed. ' % DisksScrubbing

	if Reconstructing > 0:
		ReturnCode = RETURNCODE['WARNING']
		ReturnMsg += '%s disk(s) are being reconstructed! ' % Reconstructing


	if (options.subsys == 'sparedisk'):
		if DisksSpare <= LevelWarn:
			ReturnMsg += 'Not enough spare disks! '
			if DisksSpare <= LevelCrit:
				ReturnCode = RETURNCODE['CRITICAL']
			else:
				ReturnCode = RETURNCODE['WARNING']

		if DisksFailed > 0:
			ReturnCode = RETURNCODE['CRITICAL']
			ReturnMsg += '%s disk(s) failed (%s)! ' % (DisksFailed, DisksFailedDescr)

		ReturnMsg += 'Disk stats: %s total, %s active, %s spare, %s failed' % (DisksTotal, DisksActive, DisksSpare, DisksFailed)
		ReturnMsg += '|nadisk_total=%s;;;0; nadisk_active=%s;;;0;%s nadisk_spare=%s;%s;%s;0;%s nadisk_failed=%s;;;0;%s' % (DisksTotal, DisksActive, DisksTotal, DisksSpare, LevelWarn, LevelCrit, DisksTotal, DisksFailed, DisksTotal)

	elif options.subsys == 'faileddisk':
		if DisksFailed > LevelWarn:
			ReturnCode = RETURNCODE['WARNING']
			if DisksFailed > LevelCrit:
				ReturnCode = RETURNCODE['CRITICAL']
			ReturnMsg += '%s disk(s) failed (%s)! ' % (DisksFailed, DisksFailedDescr)

		ReturnMsg += 'Disk stats: %s total, %s active, %s spare, %s failed' % (DisksTotal, DisksActive, DisksSpare, DisksFailed)
		ReturnMsg += '|nadisk_total=%s;;;0; nadisk_active=%s;;;0;%s nadisk_spare=%s;;;0;%s nadisk_failed=%s;%s;%s;0;%s' % (DisksTotal, DisksActive, DisksTotal, DisksSpare, DisksTotal, DisksFailed, LevelWarn, LevelCrit, DisksTotal)



elif options.subsys == 'fs':
	if options.fs == '0':
		ReturnMsg = 'No filesystem was given (-f FS)!'
		ReturnCode = RETURNCODE['UNKNOWN']
	else:
		fsid = get_fsid(options.fs)
		# Now the index should be in fsid

		dfFSName          = SNMPGET(OIDs['df_FS_Name'] + "." + fsid)
		dfFSMountedOn     = SNMPGET(OIDs['df_FS_Mounted_On'] + "." + fsid)
		dfFSPctUsed       = int(SNMPGET(OIDs['df_FS_%Used'] + "." + fsid))
#		dfFSINodeUsed     = long(SNMPGET(OIDs['df_FS_INodeUsed'] + "." + fsid))		# NOT Used
		dfFSPctINodeUsed  = int(SNMPGET(OIDs['df_FS_%INodeUsed'] + "." + fsid))
		dfFSStatus        = SNMPGET(OIDs['df_FS_Status'] + "." + fsid)
		dfFSType          = SNMPGET(OIDs['df_FS_Type'] + "." + fsid)

		(dfFSkBTotal, dfFSkBUsed, dfFSkbAvail) = get_kb_fs(fsid)

		dfFSName          = dfFSName.replace('"','')
		dfFSMountedOn     = dfFSMountedOn.replace('"','')

		ReturnMsg = '%s "%s"' % (Enum_df_FS_Type[dfFSType], dfFSName)
		if dfFSName != dfFSMountedOn:
			ReturnMsg += ' ("%s")' % dfFSMountedOn

		ReturnMsg += ': %s%% used (%skB out of %skB), INodes: %s%% used, status: %s' % (
				dfFSPctUsed, dfFSkBUsed, dfFSkBTotal,
				dfFSPctINodeUsed,
				Enum_df_FS_Status[dfFSStatus] )

		ReturnCode = RETURNCODE['OK']
		LevelWarn = ''
		LevelCrit = ''

		if options.warn != '0':
			LevelWarn = str(long(dfFSkBTotal * 10.24 * int(options.warn)))
			if dfFSPctUsed >= int(options.warn):
				ReturnCode = RETURNCODE['WARNING']

		if options.crit != '0':
			LevelCrit = str(long(dfFSkBTotal * 10.24 * int(options.crit)))
			if dfFSPctUsed >= int(options.crit):
				ReturnCode = RETURNCODE['CRITICAL']

		ReturnMsg += '|nafs_%s=%sB;%s;%s;%s;%s' % (dfFSName, (dfFSkBUsed*1024L), LevelWarn, LevelCrit, 0, (dfFSkBTotal*1024))



elif options.subsys == 'vol':
	if options.fs == '0':
		back2nagios(RETURNCODE['UNKNOWN'], 'No filesystem was given (-f FS)!')
	
	if options.warn == '0' or options.crit == '0':
		back2nagios(RETURNCODE['UNKNOWN'], 'Volume check needs -w AND -c values!')

	fsid = get_fsid(options.fs)
	# Now the index should be in fsid

	if int(fsid) % 2 == 0:
		back2nagios(RETURNCODE['UNKNOWN'], 'I need a volume, not a snapshot!')

	dfFSName          = SNMPGET(OIDs['df_FS_Name'] + "." + fsid)
	dfFSMountedOn     = SNMPGET(OIDs['df_FS_Mounted_On'] + "." + fsid)
#			dfFSPctUsed       = int(SNMPGET(OIDs['df_FS_%Used'] + "." + fsid))
#			dfFSINodeUsed     = long(SNMPGET(OIDs['df_FS_INodeUsed'] + "." + fsid))		# NOT Used
	dfFSPctINodeUsed  = int(SNMPGET(OIDs['df_FS_%INodeUsed'] + "." + fsid))
	dfFSStatus        = SNMPGET(OIDs['df_FS_Status'] + "." + fsid)
	dfFSType          = SNMPGET(OIDs['df_FS_Type'] + "." + fsid)

	(dfFSkBTotal, dfFSkBUsed, dfFSkBAvail)    = get_kb_fs(fsid)
	(SdfFSkBTotal, SdfFSkBUsed, SdfFSkBAvail) = get_kb_fs(str(int(fsid)+1))

	dfFSName          = dfFSName.replace('"','')
	PD_dfFSName       = dfFSName[:-1].replace('/vol/','').replace('/','_')
	dfFSMountedOn     = dfFSMountedOn.replace('"','')
	dfFSPctUsed       = round(float(dfFSkBUsed)  / float(dfFSkBTotal) * 1000) / 10
	dfFSPctFree       = round(float(dfFSkBAvail) / float(dfFSkBTotal) * 1000) / 10

	ReturnMsg = '%s "%s"' % (Enum_df_FS_Type[dfFSType], dfFSName)
	if dfFSName != dfFSMountedOn:
		ReturnMsg += ' ("%s")' % dfFSMountedOn

	ReturnCode = RETURNCODE['OK']
	PD_LevelWarn = ''
	PD_LevelCrit = ''

	powers = ['b','k','m','g','t','p','e']

	if options.warn != '0':
		if options.warn[-1:] == '%':
			options.warn  = float(options.warn[:-1])
			PD_LevelWarn  = str(long(dfFSkBTotal * 10.24 * options.warn))
			TestLevelWarn = long(dfFSkBTotal*1024) * options.warn / 100
		elif options.warn[-1:].isdigit():
			options.warn  = float(options.warn)
			PD_LevelWarn  = str(long(dfFSkBTotal * 10.24 * options.warn))
			TestLevelWarn = long(dfFSkBTotal*1024) * options.warn / 100
		elif options.warn[-1:].lower() in powers:
			TestLevelWarn = 1024L ** powers.index(options.warn[-1:].lower()) * long(options.warn[:-1])
			PD_LevelWarn  = str(TestLevelWarn)

	if options.crit != '0':
		if options.crit[-1:] == '%':
			options.crit  = float(options.crit[:-1])
			PD_LevelCrit  = str(long(dfFSkBTotal * 10.24 * options.crit))
			TestLevelCrit = long(dfFSkBTotal*1024) * options.crit / 100
		elif options.crit[-1:].isdigit():
			options.crit  = float(options.crit)
			PD_LevelCrit  = str(long(dfFSkBTotal * 10.24 * options.crit))
			TestLevelCrit = long(dfFSkBTotal*1024) * options.crit / 100
		elif options.crit[-1:].lower() in powers:
			TestLevelCrit = 1024L ** powers.index(options.crit[-1:].lower()) * long(options.crit[:-1])
			PD_LevelCrit  = str(TestLevelCrit)

	if TestLevelWarn > TestLevelCrit:
		# Check for free Space
		if dfFSkBAvail*1024 < TestLevelWarn:
			ReturnCode = RETURNCODE['WARNING']

		if dfFSkBAvail*1024 < TestLevelCrit:
			ReturnCode = RETURNCODE['CRITICAL']

		if options.verb >= 1:
			print "TestAvail - Value: %s, Warn: %s, Crit: %s - RetCode %s" % ((dfFSkBAvail*1024), TestLevelWarn, TestLevelCrit, ReturnCode)
	else:
		# Check for used Space
		if dfFSkBUsed*1024 > TestLevelWarn:
			ReturnCode = RETURNCODE['WARNING']

		if dfFSkBUsed*1024 > TestLevelCrit:
			ReturnCode = RETURNCODE['CRITICAL']

		if options.verb >= 1:
			print "TestUsed - Value: %s, Warn: %s, Crit: %s - RetCode %s" % ((dfFSkBUsed*1024), TestLevelWarn, TestLevelCrit, ReturnCode)


	ReturnMsg += ': %s%% used (%skB out of %skB), INodes: %s%% used, status: %s' % (
			dfFSPctUsed, dfFSkBUsed, dfFSkBTotal,
			dfFSPctINodeUsed,
			Enum_df_FS_Status[dfFSStatus] )

	ReturnMsg += '|navoldata_%s=%sB;%s;%s;%s;%s' % (PD_dfFSName, (dfFSkBUsed*1024L), PD_LevelWarn, PD_LevelCrit, 0, (dfFSkBTotal*1024L))
	ReturnMsg += ' navolsnap_%s=%sB;;;%s;%s' % (PD_dfFSName, (SdfFSkBUsed*1024L), 0, (SdfFSkBTotal*1024L))
	ReturnMsg += ' nadatasize_%s=%sB' % (PD_dfFSName, (dfFSkBTotal*1024L))
	ReturnMsg += ' nasnapsize_%s=%sB' % (PD_dfFSName, (SdfFSkBTotal*1024L))



elif options.subsys == 'cifs-users':
	cifsConnectedUsers = int(SNMPGET(OIDs['CIFS_Connected_Users']))

	ReturnMsg = "%i connected users" % (cifsConnectedUsers)
	ReturnMsg += "|cifs_users=%i;;;0;" % (cifsConnectedUsers)
	
	ReturnCode = RETURNCODE['OK']

	if options.warn != '0':
		if cifsConnectedUsers >= int(options.warn):
			ReturnCode = RETURNCODE['WARNING']
	if options.crit != '0':
		if cifsConnectedUsers >= int(options.crit):
			ReturnCode = RETURNCODE['CRITICAL']



elif options.subsys == 'cifs-stats':
	cifsTotalOps	= int(SNMPGET(OIDs['CIFS_Total_Ops']))
	cifsTotalCalls	= int(SNMPGET(OIDs['CIFS_Total_Calls']))
	cifsBadCalls	= int(SNMPGET(OIDs['CIFS_Bad_Calls']))
	cifsGetAttrs	= int(SNMPGET(OIDs['CIFS_Get_Attrs']))
	cifsReads	= int(SNMPGET(OIDs['CIFS_Reads']))
	cifsWrites	= int(SNMPGET(OIDs['CIFS_Writes']))
	cifsLocks	= int(SNMPGET(OIDs['CIFS_Locks']))
	cifsOpens	= int(SNMPGET(OIDs['CIFS_Opens']))
	cifsDirOps	= int(SNMPGET(OIDs['CIFS_DirOps']))
	cifsOthers	= int(SNMPGET(OIDs['CIFS_Others']))


	#ReturnMsg = "total: %i others: %i reads: %i writes: %i" % (cifsTotalOps, cifsOthers, cifsReads, cifsWrites)
	ReturnMsg = "OK"
	ReturnMsg += "|total_ops=%ic;;;0; " \
		      "total_calls=%ic;;;0; " \
		      "bad_calls=%ic;;;0; " \
		      "get_attrs=%ic;;;0; " \
		      "reads=%ic;;;0; " \
		      "writes=%ic;;;0; " \
		      "locks=%ic;;;0; " \
		      "opens=%ic;;;0; " \
		      "dirops=%ic;;;0; "\
		      "others=%ic;;;0;" % ( \
				cifsTotalOps, \
				cifsTotalCalls, \
				cifsBadCalls, \
				cifsGetAttrs, \
				cifsReads, \
				cifsWrites, \
				cifsLocks, \
				cifsOpens, \
				cifsDirOps, \
				cifsOthers)

	ReturnCode = RETURNCODE['OK']



elif options.subsys == 'cluster':
	ClusterSettings = int(SNMPGET(OIDs['Cluster_Settings']))
	if ClusterSettings == 1:
		# notConfigured
		ReturnCode = RETURNCODE['WARNING']
		ReturnMsg  = "No cluster configured!"
	else:
		ClusterState			= int(SNMPGET(OIDs['Cluster_State']))
		ClusterInterconnectStatus	= int(SNMPGET(OIDs['Cluster_InterconnectStatus']))

		ReturnCode = RETURNCODE['OK']

		if (ClusterSettings in OkWarnCrit['ClusterSettings'][1] or ClusterState in OkWarnCrit['ClusterState'][1] or ClusterInterconnectStatus in OkWarnCrit['ClusterInterconnectStatus'][1]):
			ReturnCode = RETURNCODE['WARNING']

		if (ClusterSettings in OkWarnCrit['ClusterSettings'][2] or ClusterState in OkWarnCrit['ClusterState'][1] or ClusterInterconnectStatus in OkWarnCrit['ClusterInterconnectStatus'][1]):
			ReturnCode = RETURNCODE['CRITICAL']

		ReturnMsg  = 'Cluster settings: ' + Enum_Cluster_Settings[str(ClusterSettings)] + ', '
		ReturnMsg += 'state: ' + Enum_Cluster_State[str(ClusterState)] + ', '
		ReturnMsg += 'interconnect state: ' + Enum_Cluster_InterconnectStatus[str(ClusterInterconnectStatus)]

		if ClusterState == 4:
			# cannotTakeover
			ClusterCannotTakeOverCause = int(SNMPGET(OIDs['Cluster_CannotTakeOverCause']))

			ReturnMsg = 'Cannot takeover, reason: ' + Enum_Cluster_CannotTakeOverCause[str(ClusterCannotTakeOverCause)] + '! ' + ReturnMsg



elif options.subsys == 'snapmirror':
	if SNMPGET(OIDs['License_SnapMirror']) != '2':
		ReturnMsg = 'SnapMirror not licensed!'
		ReturnCode = RETURNCODE['CRITICAL']
	else:
		SnapmirrorOn = int(SNMPGET(OIDs['Snapmirror_On']))
		if SnapmirrorOn != 2:
			ReturnMsg  = 'SnapMirror is off!'
			ReturnCode = RETURNCODE['WARNING']
		else:
			ReturnCode = RETURNCODE['OK']

			if options.fs == '0':
				ReturnMsg  = 'SnapMirror is on'
			elif options.fs.isdigit() == False:
			# is fs not a number?
				ReturnMsg  = 'Sorry! You have to provide index number at the moment!'
				ReturnCode = RETURNCODE['UNKNOWN']
			else:
				SnapmirrorSrc		= SNMPGET(OIDs['Snapmirror_Src'] + "." + options.fs)
				SnapmirrorDst		= SNMPGET(OIDs['Snapmirror_Dst'] + "." + options.fs)
				SnapmirrorStatus	= int(SNMPGET(OIDs['Snapmirror_Status'] + "." + options.fs))
				SnapmirrorState		= int(SNMPGET(OIDs['Snapmirror_State'] + "." + options.fs))

				if SnapmirrorState in OkWarnCrit['SnapmirrorState'][2]:
					ReturnCode = RETURNCODE['CRITICAL']
				elif SnapmirrorState in OkWarnCrit['SnapmirrorState'][1]:
					ReturnCode = RETURNCODE['WARNING']

				ReturnMsg = 'SnapMiror state is \'' + Enum_Snapmirror_State[str(SnapmirrorState)] + '\'. '
				ReturnMsg += 'Source: \'' + SnapmirrorSrc + '\', Destination: \'' + SnapmirrorDst + '\', Status: \'' + Enum_Snapmirror_Status[str(SnapmirrorStatus)] + '\''



elif options.subsys == 'cacheage':
	CacheAge = int(SNMPGET(OIDs['Cache_Age']))
	ReturnCode = RETURNCODE['OK']
	ReturnMsg = 'Cache Age %s minutes|nacacheage=%s;;;0;' % (CacheAge, CacheAge)



elif options.subsys == 'cp':
	cp = SNMPWALK(OIDs['CP'])
	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = 'Consistency Point (in progress %s seconds), Ops: Total(%s) ' % (float(cp[0])/100, cp[7])
	ReturnMsg += 'Snapshot(%s) LowWaterMark(%s) HighWaterMark(%s) LogFull(%s) CP-b2b(%s) ' % cp[2:7]
	ReturnMsg += 'Flush(%s) Sync(%s) LowVBuf(%s) CpDeferred(%s) LowDatavecs(%s)' % cp[8:13]
	ReturnMsg += '|nacpprogress=%ss nacptotal=%sc ' % (float(cp[0])/100, cp[7])
	ReturnMsg += 'nacpsnapshot=%sc nacplowwatermark=%sc nacphighwatermark=%sc nacplogfull=%s nacpb2b=%sc ' % cp[2:7]
	ReturnMsg += 'nacpflush=%sc nacpsync=%sc nacplowvbuf=%sc nacpcpdeferred=%sc nacplowdatavecs=%sc' % cp[8:13]



elif options.subsys == 'ifstat':
	if options.var == '0':
		back2nagios(RETURNCODE['UNKNOWN'], 'No network interface name was given (-V NIC)!')

	idx = find_in_table(OIDs['Net_ifIndex'], OIDs['Net_ifDescr'], options.var)
	if not idx:
		back2nagios(RETURNCODE['UNKNOWN'], 'No network interface with name "%s" found!' % options.var)

	# get64bits(oids, idx)
	n_bytes_in	= get64bits(OID64s['Net_InBytes'], idx)
	n_bytes_out	= get64bits(OID64s['Net_OutBytes'], idx)
	n_discards_in	= get64bits(OID64s['Net_InDiscards'], idx)
	n_discards_out	= get64bits(OID64s['Net_OutDiscards'], idx)
	n_errors_in	= get64bits(OID64s['Net_InErrors'], idx)
	n_errors_out	= get64bits(OID64s['Net_OutErrors'], idx)

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = 'Network statistics for %s' % options.var
	ReturnMsg += '|nanet_by_in=%sc nanet_by_out=%sc ' % (n_bytes_in, n_bytes_out)
	ReturnMsg += 'nanet_dis_in=%sc nanet_dis_out=%sc ' % (n_discards_in, n_discards_out)
	ReturnMsg += 'nanet_err_in=%sc nanet_err_out=%sc ' % (n_errors_in, n_errors_out)




elif options.subsys == 'diskio':
	dio_read	= get64bits(OID64s['DiskIO_ReadBytes'], '0')
	dio_write	= get64bits(OID64s['DiskIO_WriteBytes'], '0')

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = 'Disk I/O statistics'
	ReturnMsg += '|nadiskread=%sB nadiskwrite=%sB' % (dio_read, dio_write)



elif options.subsys == 'tapeio':
	tio_read	= get64bits(OID64s['TapeIO_ReadBytes'], '0')
	tio_write	= get64bits(OID64s['TapeIO_WriteBytes'], '0')

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = 'Tape I/O statistics'
	ReturnMsg += '|nataperead=%sB natapewrite=%sB' % (tio_read, tio_write)



elif options.subsys == 'ops':
	ops_nfs		= get64bits(OID64s['OPs_NFS'], '0')
	ops_cifs	= get64bits(OID64s['OPs_CIFS'], '0')
	ops_http	= get64bits(OID64s['OPs_HTTP'], '0')

	ReturnCode = RETURNCODE['OK']
	ReturnMsg  = 'Total ops statistics'
	ReturnMsg += '|naops_nfs=%sc naops_cifs=%sc naops_http=%sc' % (ops_nfs, ops_cifs, ops_http)



else:
	parser.print_help()
	sys.exit(RETURNCODE['UNKNOWN'])





if options.cache:
	if options.verb >=1:
		print 'Store FSIDs: %s' % fsidcache
	fsidcache.close()

back2nagios(ReturnCode, ReturnMsg)

# vim: ts=8 sw=8

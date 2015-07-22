
'''
---ALU Metrocell WMS PowerMenu-----
# This program makes it easier to run
# diagnostic commands from the NESA
# ALU WMS. 
#
# Created by Russell Endicott (rendicott@gmail.com)
# 2014-08-19
'''

'''
This PowerMenu module is a place to store static variable input data.
Eventually stuff in this module should be stored in a database or user
configurable file. For now I'm just collecting it here so there's very little
content in the actual code that's 'hard coded'. 
'''
sversion = '0.4.8'


#some hardcoded script names for the two BASH scripts, need to do this better
''' NOTE: I had to put the /usr/bin/expect in front of the script 
name because WMS shell (ksh) is silly'''
fgw_bsgScript = '/usr/bin/expect ./EXP-getbsg.exp'
femtostatus_script = '/usr/bin/expect ./EXP-apcheck.exp'
femtostatus_script_new = '/usr/bin/expect ./EXP-apcheck-new.exp'
knownhosts_script = '/usr/bin/expect ./EXP-kh.exp'
reboot_script = '/usr/bin/expect ./EXP-apreboot.exp'

#define sources for data from files
prefix = '/home/customer/russ/wicldumps/'
#prefix = ''
#prefix = '../wicldumps/'
fromfiles_provisioning = prefix + 'RAWDATA-provisioning.dat'
fromfiles_alarms = prefix + 'RAWDATA-alarms.dat'
fromfiles_fddcell = prefix + 'RAWDATA-fddcell.dat'

#set a foodfiles directory to scan for newest file
# must have the trailing '/' !
foodFilesDir = '/home/customer/russ/pm_foodfiles/'
#foodFilesDir = '../pm_foodfiles/'


#default log file name
defaultlogfilename = 'pm.log'

#define a long banner string when we run an OS command
#declaring here saves space in the rest of the code
rob = "=-=-=-=-=- RUNNING OS COMMAND =-=-=-=-=-: "


'''current list of active FGW's monitored by Operations. This info will 
change slowly over time and the code will need to be updated
This could be done better. Probably just pass in a CSV to the script. '''

# key legend
# 'selector' - This is the menu selector item that shows up in the list
# 'fgwName' - This is the hostname of the FGW
# 'fgwIP' - this is the static IP of the FGW
# 'bsgDump' - this is a holding place for the output of bsr_get_bsg_reg cmd
# 'monitoredStatus' - whether the FGW is monitored or not
# 'clusterId' - this is the ALU/BC cluster ID for the FGW

fgwList = [
    { 'selector' : '03' , 
      'fgwName' : 'CRTNTX35CR9S01', 
      'fgwDesc' : 'Carrollton 1' , 
      'fgwIP' : '10.24.40.171' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '101'},
    { 'selector' : '04' , 
      'fgwName' : 'SNTDCAUJCR9S01', 
      'fgwDesc' : 'Santa Clara 1' , 
      'fgwIP' : '107.96.253.139' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '1'},
    { 'selector' : '05' , 
      'fgwName' : 'SNAPCAHHCR9S01', 
      'fgwDesc' : 'Santa Ana 1' , 
      'fgwIP' : '10.170.70.75' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '51'},
    { 'selector' : '11' , 
      'fgwName' : 'SNAPCAHHCR9S02', 
      'fgwDesc' : 'Santa Ana 2' , 
      'fgwIP' : '10.170.70.77' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '52'},
    { 'selector' : '01' , 
      'fgwName' : 'NWTPMOABCR9S01', 
      'fgwDesc' : 'Hazelwood 1' , 
      'fgwIP' : '10.174.33.171' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '151'},
    { 'selector' : '02' , 
      'fgwName' : 'NWTPMOABCR9S02', 
      'fgwDesc' : 'Hazelwood 2' , 
      'fgwIP' : '10.174.33.173' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '152'},
    { 'selector' : '06' , 
      'fgwName' : 'RCPKNJ02CR9S01', 
      'fgwDesc' : 'Rochelle Park 1' , 
      'fgwIP' : '10.191.178.171' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '201'},
    { 'selector' : '07' , 
      'fgwName' : 'ATLNGAACCR9S01', 
      'fgwDesc' : 'Decatur 1' , 
      'fgwIP' : '10.187.167.139' , 
      'bsgDump' : '', 
      'monitoredStatus' : 
      'Monitored', 
      'clusterId' : '301'},
    { 'selector' : '08' , 
      'fgwName' : 'LKMRFLMFCR9S01', 
      'fgwDesc' : 'Lake Mary 1' , 
      'fgwIP' : '10.187.167.43' , 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '351'},
    { 'selector' : '09' , 
      'fgwName' : 'CLMAMDORCR9S01', 
      'fgwDesc' : 'Columbia 1' , 
      'fgwIP' : '10.188.131.203', 
      'bsgDump' : '', 
      'monitoredStatus' : 'Monitored', 
      'clusterId' : '251'},
    ]
'''
{ 'selector' : '10' , 
'fgwName' : 'CRTNTX35CR9S02', 
'fgwDesc' : 'Carrollton 2' , 
'fgwIP' : '10.24.40.173', 
'bsgDump' : '', 
'monitoredStatus' : 'Not Monitored', 
'clusterId' : '102'}
'''
    
    
#make the default ASCII escape code blank so text shows up normally
colorlist = [
    {'index' : '1', 
     'example' : '\033[1;31mRed like Radish\033[m', 
     'code' : '31m'},
    {'index' : '2', 
     'example' : '\033[1;32mGreen like Grass\033[m', 
     'code' : '32m'},
    {'index' : '3', 
     'example' : '\033[1;33mYellow like Yolk\033[m', 
     'code' : '33m'},
    {'index' : '4', 
     'example' : '\033[1;34mBlue like Blood\033[m', 
     'code' : '34m'},
    {'index' : '5', 
     'example' : '\033[1;35mMagenta like Mimosa\033[m', 
     'code' : '35m'},
    {'index' : '6', 
     'example' : '\033[1;36mCyan like Caribbean\033[m', 
     'code' : '36m'},
    {'index' : '7', 
     'example' : '\033[1;37mWhite like Whipped Cream\033[m', 
     'code' : '37m'},
    {'index' : '8',  
     'example' : '\033[1;38mCrimson like Chianti\033[m', 
     'code' : '38m'},
    {'index' : '9', 
     'example' : '\033[1;41mHighlighted Red like Radish\033[m', 
     'code' : '41m'},
    {'index' : '10', 
     'example' : '\033[1;42mHighlighted Green like Grass\033[m', 
     'code' : '42m'},
    {'index' : '11', 
     'example' : '\033[1;43mHighlighted Brown like Bear\033[m', 
     'code' : '43m'},
    {'index' : '12', 
     'example' : '\033[1;44mHighlighted Blue like Blood\033[m', 
     'code' : '44m'},
    {'index' : '13', 
     'example' : '\033[1;45mHighlighted Magenta like Mimosa\033[m', 
     'code' : '45m'},
    {'index' : '14', 
     'example' : '\033[1;46mHighlighted Cyan like Caribbean\033[m', 
     'code' : '46m'},
    {'index' : '15', 
     'example' : '\033[1;47mHighlighted Gray like Ghost\033[m', 
     'code' : '47m'},
    {'index' : '16', 
     'example' : '\033[1;48mHighlighted Crimson like Chianti\033[m', 
     'code' : '48m'},
    {'index' : '17', 
     'example' : 'None like Nancy', 
     'code': ''}
        ]
        
timeoutlist = [{'index' : '1', 'timeout' : '8'},
                {'index' : '2', 'timeout' : '12'},
                {'index' : '3', 'timeout' : '16'},
                {'index' : '4', 'timeout' : '24'},
                {'index' : '5', 'timeout' : '40'},
                {'index' : '6', 'timeout' : '50'},
        ]
##############################################################        
#Begin global section to define column headers and widths
##############################################################
'''              BEGIN ALARM DISPLAY FORMAT CONFIG                  '''
'''This section defines the formats for how Alarm objects are displayed '''
# this defines the Alarm output column widths and placement order
display_format_alarm = (
        '{0:7}'                    # index
        '{1:10}'                   # AlarmID
        '{2:31}'                   # specificProblems
        '{3:20}'                   # eventTime
        '{4:73}'                   # alarmedComponent
        '{5:20}'                   # bSRName
        '{6:14}'                   # monitoredStatus
        '{7:12}'                   # adminStatus
        '{8:4}'                    # clusterID
        '{9:15}'                   # fgwName
        )

# this is what's displayed at the bottom of the columns on screen output 
alarmheaderlist = ['index',                 # 0
                   'AlarmID',               # 1
                   'specificProblems',      # 2
                   'eventTime',             # 3
                   'alarmedComponent',      # 4
                   'bSRName',               # 5
                   'monitored?',            # 6
                   'adminStatus',           # 7
                   'cid',                   # 8
                   'fgwName']               # 9

# this is what's displayed at the top of the columns in the output Alarm csv
alarmcsvlist = ['AlarmID',
                'specificProblems',
                'eventTime',
                'alarmedComponent',
                'bSRName',
                'monitored?',
                'adminStatus',
                'cid',
                'fgwName']

#now turn the Alarm CSV header list into a comma separated string
header_alarm_csv = ','.join(alarmcsvlist)

'''              END ALARM DISPLAY FORMAT CONFIG                  '''
                
                
'''          BEGIN METROCELL DISPLAY FORMAT CONFIG                  '''                
'''This section defines the formats for how Metrocell objects are displayed '''
#this defines the 'short' format column widths and placement order
display_format_metrocell = (
        '{0:7}'             # index
        '{1:13}'            # bsrName
        '{2:11}'            # serial
        '{3:7}'             # bsrId
        '{4:23}'            # groupName
        '{5:31}'            # specInfo
        '{6:15}'            # monitoredStatus
        '{7:16}'            # ipsecIpAddr
        '{8:5}'             # clusterId
        '{9:5}'             # groupId
        '{10:15}'           # groupId
        '{11:9}'            # fgw
        '{12:12}'           # gagr
        '{13:6}'            # adminStatus
        )
#this defines the full format column widths and placement order
display_format_metrocell_full = (
        '{0:7}'             # index
        '{1:13}'            # bsrName
        '{2:11}'            # serial
        '{3:7}'             # bsrId
        '{4:23}'            # groupName
        '{5:23}'            # ctsEquipName
        '{6:31}'            # specInfo
        '{7:15}'            # monitoredStatus
        '{8:16}'            # ipsecIpAddr
        '{9:5}'             # clusterId
        '{10:5}'            # groupId
        '{11:15}'           # fgw
        '{12:9}'            # gagr
        '{13:9}'            # usid
        '{14:12}'           # faLocCode
        '{15:8}'            # inout
        '{16:5}'            # technology
        '{17:7}'            # alarm?
        '{18:4}'            # use case (UC)
        '{19:19}'           # swVersion
        '{20:12}'           # adminStatus
        )
# define column header strings for Metrocell/femto
# this is what's displayed at the bottom of the columns on output
femtoheaderlist = ['index',             # 0
                   'bsrName',           # 1
                   'serial',            # 2
                   'bsrId',             # 3
                   'groupName',         # 4
                   'specInfo',          # 5
                   'monitored?',        # 6
                   'ipsecIpAddr',       # 7
                   'clstr',             # 8
                   'grp',               # 9
                   'fgw',               # 10
                   'gagr',              # 11
                   'adminStatus',       # 12
                   'alarm?']            # 13

femtoheaderlist_full = [
                    'index',            # 0
                    'bsrName',          # 1
                    'serial',           # 2
                    'bsrId',            # 3
                    'groupName',        # 4
                    'ctsEquipName',     # 5
                    'specInfo',         # 6
                    'monitored?',       # 7
                    'ipsecIpAddr',      # 8
                    'clstr',            # 9
                    'grp',              # 10
                    'fgw',              # 11
                    'gagr',             # 12
                    'usid',             # 13
                    'faLocCode',        # 14
                    'inout',            # 15
                    'tech',             # 16
                    'alarm?',           # 17
                    'UC',               # 18
                    'swVersion',        # 19
                    'adminStatus'       # 20
                    ]

# what's displayed at the top of the columns in the SHORT output Metrocell csv
femtocsvlist = ['bsrName',
                'serial',
                'bsrId',
                'groupName',
                'specInfo',
                'monitored?',
                'ipsecIpAddr',
                'clusterId',
                'groupId',
                'fgw',
                'grid-gateway',
                'adminStatus',
                'bsrAdminStatus',
                'bsrOperStatus',
                'cellAdminStatus',
                'cellOperStatus',
                'UEconnected?'
                ]
# what's displayed at the top of the columns in the FULL output Metrocell csv
femtocsvlist_full = ['index',
                     'bsrName',
                     'serial',
                     'bsrId',
                     'groupName',
                     'ctsEquipName',
                     'specInfo',
                     'monitored?',
                     'ipsecIpAddr',
                     'clstr',
                     'grp',
                     'fgw',
                     'gagr',
                     'usid',
                     'faLocCode',
                     'inout',
                     'tech',
                     'alarm?',
                     'usecase',
                     'swVersion',
                     'adminStatus'
                     ]


display_format_metrocell_status = (
            '{0:17}'            # monitoredStatus
            '{1:16}'            # ipsecIpAddr
            '{2:9}'             # gagr
            '{3:12}'            # adminStatus
            '{4:12}'            # bsrAStatus
            '{5:12}'            # bsrOStatus
            '{6:13}'            # cellAStatus
            '{7:13}'            # cellOStatus
            '{8:5}'             # UEs?
            '{9:5}'             # clstr
            '{10:5}'            # grp
            '{11:15}'           # fgw
            '{12:7}'            # alarm?
            '{13:14}'           # bsrName
            '{14:19}'           # mac address
            '{15:16}'           # local ip addr
            '{16:16}'           # firstPublicIpInPath
            '{17:16}'           # defaultroute
            '{18:16}'           # netmask
            '{19:16}'           # dhcps ip
            )

statusheaderlist = [
        'monitoredStatus',      # 0
        'ipsecIpAddr',          # 1
        'gagr',                 # 2
        'adminStatus',          # 3
        'bsrAStatus',           # 4
        'bsrOStatus',           # 5
        'cellAStatus',          # 6
        'cellOStatus',          # 7
        'UEs?',                 # 8
        'clstr',                # 9
        'grp',                  # 10
        'fgw',                  # 11
        'alarm?',               # 12
        'bsrName',              # 13
        'macaddr',              # 14
        'lcl_ip',              # 15
        'firstpublic',              # 16
        'def_rt',              # 17
        'netmask',              # 18
        'dhcps_ip',              # 19
        ]

statuscsvlist = [
        'monitoredStatus',
        'ipsecIpAddr',
        'gagr',
        'adminStatus',
        'bsrAStatus',
        'bsrOStatus',
        'cellAStatus',
        'cellOStatus',
        'UEconnected?',
        'bsrName',
        'macaddr',
        'local_ip_addr',
        'firstPublicIpInPath',
        'default_route',
        'netmask',
        'dhcp_server_ip',
        ]

#now turn the Metrocell CSV header lists into comma separated strings
header_metro_csv = ','.join(femtocsvlist)
header_metro_full_csv = ','.join(femtocsvlist_full)
header_status_csv = ','.join(statuscsvlist)

'''          END METROCELL DISPLAY FORMAT CONFIG                  '''                


'''here we'll set up our variable length separators 
(e.g., --------) using the above column header strings'''
def genseparator(headerstring):
    sep = ''
    separator = sep.join(['-' for x in range(len(headerstring))])
    return separator

#now build the actual strings
header_status = display_format_metrocell_status.format(*statusheaderlist)
header_alarm = display_format_alarm.format(*alarmheaderlist)
header_metro = display_format_metrocell.format(*femtoheaderlist)
header_metrofull = display_format_metrocell_full.format(*femtoheaderlist_full)

sep_status = genseparator(header_status)
sep_alarm = genseparator(header_alarm)
sep_metro = genseparator(header_metro)
sep_metrofull = genseparator(header_metrofull)

'''End global section to define column headers and widths'''

#we'll build a menu pre-set list so UI is more fluid
preset_list = { '10': { 'columnName' : 'additionalText' },
                '11': { 'columnName' : 'alarmedComponent' },
                '12': { 'columnName' : 'notificationIdentifier' },
                '13': { 'columnName' : 'bSRName' },
                '14': { 'columnName' : 'FemtoCluster' },
                '15': { 'columnName' : 'eventTime' },
                '16': { 'columnName' : 'specificProblems' },
                '24': { 'attribute' : 'groupName' },
                '23': { 'attribute' : 'groupId' },
                '20': { 'attribute' : 'bsrName' },
                '21': { 'attribute' : 'bsrId' },
                '22': { 'attribute' : 'serial' },
                '29': { 'attribute' : 'clusterId' },
                '26': { 'attribute' : 'ipsecIpAddr' },
                '27': { 'attribute' : 'ctsname' },
                '28': { 'attribute' : 'usid' },
                '25': { 'attribute' : 'faloc' },
            }

autoupdate_frequency_list = [
    {'index' : '1', 
     'description' : '10 minutes (default)', 
     'time' : 600},
    {'index' : '2', 
     'description' : '20 minutes', 
     'time' : 1200},
    {'index' : '3', 
     'description' : '5 minutes', 
     'time' : 300},
    {'index' : '999', 
     'description' : '10 seconds (WARNING: Debug only)', 
     'time' : 10}, 
        ]
            
# sometimes we want to dump FGW BSG Registrations output to file for offline
#   parsing. I'll define filename prefix here:
bsgdump_fname_prefix = 'DATA_BSGDUMP_'
bsgdump_bool = False
#bsgdump_offline_pull_dir = './'
bsgdump_offline_pull_dir = '../wicldumps/'


=== ALU WMS Metrocell Power Menu ===
|     Creator: rendicott@gmail.com
|     Date: 2014-09-15
|     Version: 0.4.7
====================================

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~CONTENTS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-INTRODUCTION
-PREREQS / INSTALLATION
-USAGE
-ALARM DB INTERACTIONS
-INVENTORY DB INTERACTIONS
-OTHER COMMANDS
-REGULAR OPERATION
-ADVANCED INFORMATION
-APPENDIX


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INTRODUCTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tool was created as a way to speed up the monitoring and administration of the Alcatel-Lucent Small Cell solution through WMS/HDM. This tool cannot do 
everything that WMS and HDM can do but it is a very useful supplement. 

This document is to help get the user started on using the tool and to outline some of the capabilities and rules for usage. 


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~PREREQS / INSTALLATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This tool is designed to be used from the SSH command prompt of the WMS Server. At the time of this writing that means using Putty to SSH to WMS like in 
the below example:

	ssh USERNAME@METROCELL-ALP2WMS-CLIENT nesa-aln.web.bc.com:8022

To obtain a copy of the PowerMenu perform the following steps:

Navigate to your home directory on WMS:

        $ cd ~

Create a new directory. Here we'll just call the directory 'pm' for "PowerMenu"

        $ mkdir pm

Navigate to the new directory

        $ cd pm

Unpack the latest PowerMenu release into the current directory:

        $ tar xvf /home/customer/russ/powermenu/powermenu-v0.4.7.tar
        x ./EXP-apcheck-new.exp, 2636 bytes, 6 tape blocks
        x ./EXP-apcheck.exp, 2432 bytes, 5 tape blocks
        x ./EXP-apreboot.exp, 718 bytes, 2 tape blocks
        x ./EXP-getbsg.exp, 373 bytes, 1 tape blocks
        x ./EXP-kh.exp, 324 bytes, 1 tape blocks
        x ./INSTRUCTIONS-UPGRADE.txt, 3606 bytes, 8 tape blocks
        x ./INSTRUCTIONS.txt, 3564 bytes, 7 tape blocks
        x ./PowerMenu.Job.Aid.docx, 2582839 bytes, 5045 tape blocks
        x ./README.txt, 192427 bytes, 376 tape blocks
        x ./RELEASENOTES.txt, 4811 bytes, 10 tape blocks
        x ./body.txt, 83 bytes, 1 tape blocks
        x ./pm.py, 61243 bytes, 120 tape blocks
        x ./pmClasses.py, 19777 bytes, 39 tape blocks
        x ./pmConfig.py, 18256 bytes, 36 tape blocks
        x ./pmFunctions.py, 43125 bytes, 85 tape blocks
        x ./pmLoaders.py, 76862 bytes, 151 tape blocks
        x ./pmRTest.py, 3054 bytes, 6 tape blocks
        x ./pmThreads.py, 26288 bytes, 52 tape blocks


Your directory contents should look like this:

        $ ls -l
        total 6010
        -rw-r--r--   1 russ   grouper     2636 Feb  9 13:48 EXP-apcheck-new.exp
        -rw-r--r--   1 russ   grouper     2432 Feb  9 13:48 EXP-apcheck.exp
        -rw-r--r--   1 russ   grouper      718 Feb  9 13:48 EXP-apreboot.exp
        -rw-r--r--   1 russ   grouper      373 Feb  9 13:48 EXP-getbsg.exp
        -rw-r--r--   1 russ   grouper      324 Feb  9 13:48 EXP-kh.exp
        -rw-r--r--   1 russ   grouper     3606 Feb  9 13:48 INSTRUCTIONS-UPGRADE.txt
        -rw-r--r--   1 russ   grouper     3564 Feb  9 13:48 INSTRUCTIONS.txt
        -rw-r--r--   1 russ   grouper  2582839 Feb  9 13:50 PowerMenu.Job.Aid.docx
        -rw-r--r--   1 russ   grouper   192427 Feb  9 13:48 README.txt
        -rw-r--r--   1 russ   grouper     4811 Feb  9 13:48 RELEASENOTES.txt
        -rw-r--r--   1 russ   grouper       83 Feb  9 13:00 body.txt
        -rw-r--r--   1 russ   grouper    61243 Feb  9 13:48 pm.py
        -rw-r--r--   1 russ   grouper    19777 Feb  9 13:48 pmClasses.py
        -rw-r--r--   1 russ   grouper    18256 Feb  9 13:48 pmConfig.py
        -rw-r--r--   1 russ   grouper    43125 Feb  9 13:48 pmFunctions.py
        -rw-r--r--   1 russ   grouper    76862 Feb  9 13:48 pmLoaders.py
        -rw-r--r--   1 russ   grouper     3054 Feb  9 13:48 pmRTest.py
        -rw-r--r--   1 russ   grouper    26288 Feb  9 13:48 pmThreads.py



Add execute permissions to the .exp scripts inside the directory.

        $ chmod +x *.exp

Now you should see that the .exp files have the execute permissions.


        $ ls -l
        total 6010
        -rwxr-xr-x   1 russ   grouper     2636 Feb  9 13:48 EXP-apcheck-new.exp
        -rwxr-xr-x   1 russ   grouper     2432 Feb  9 13:48 EXP-apcheck.exp
        -rwxr-xr-x   1 russ   grouper      718 Feb  9 13:48 EXP-apreboot.exp
        -rwxr-xr-x   1 russ   grouper      373 Feb  9 13:48 EXP-getbsg.exp
        -rwxr-xr-x   1 russ   grouper      324 Feb  9 13:48 EXP-kh.exp
        -rw-r--r--   1 russ   grouper     3606 Feb  9 13:48 INSTRUCTIONS-UPGRADE.txt
        -rw-r--r--   1 russ   grouper     3564 Feb  9 13:48 INSTRUCTIONS.txt
        -rw-r--r--   1 russ   grouper  2582839 Feb  9 13:50 PowerMenu.Job.Aid.docx
        -rw-r--r--   1 russ   grouper   192427 Feb  9 13:48 README.txt
        -rw-r--r--   1 russ   grouper     4811 Feb  9 13:48 RELEASENOTES.txt
        -rw-r--r--   1 russ   grouper       83 Feb  9 13:00 body.txt
        -rw-r--r--   1 russ   grouper    61243 Feb  9 13:48 pm.py
        -rw-r--r--   1 russ   grouper    19777 Feb  9 13:48 pmClasses.py
        -rw-r--r--   1 russ   grouper    18256 Feb  9 13:48 pmConfig.py
        -rw-r--r--   1 russ   grouper    43125 Feb  9 13:48 pmFunctions.py
        -rw-r--r--   1 russ   grouper    76862 Feb  9 13:48 pmLoaders.py
        -rw-r--r--   1 russ   grouper     3054 Feb  9 13:48 pmRTest.py
        -rw-r--r--   1 russ   grouper    26288 Feb  9 13:48 pmThreads.py



~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ USAGE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~



Launch the script with basic functionality like this:

	python pm.py
	
At this point the script will start logging to a file named "pm.log" in the same directory. 

You'll see the following out put on the screen:

        $ python pm.py

         _____                       __  __
        |  __ \                     |  \/  |
        | |__) |____      _____ _ __| \  / | ___ _ __  _   _
        |  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | |
        | |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| |
        |_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_|
               === ALU WMS Metrocell Power Menu ===
               |     Creator: rendicott@gmail.com
               |     Date: 2014-11-20
               |     Version: 0.4.7
               ====================================


        Current Directory: /home/customer/russ/pm

        Testing color support...
        starting up with loglevel 50 CRITICAL
        newest file detected: ../pm_foodfiles/2015-02-09-06-31-05Powermenu-Food-CTS.csv

        Enter the password for the admin@FGW user:
        Enter again for verification:

        Enter the password for the old localOperator@AP user:
        Enter again for verification:

        Enter the password for the old localAdmin@AP user:
        Enter again for verification:

        Enter the password for the new 14.2 localOperator@AP user:
        Enter again for verification:

        Enter the password for the new 14.2 localAdmin@AP user:
        Enter again for verification:

The program will ask you for the five passwords required in order to interact with the Metrocells and FemtoGateways out on the network. 
You'll have to enter each password twice upon launching the program. Alternatively you can pass the passwords in as parameters. 

	|---------------------------------------------------------------------------------------
	|
	| PASSING PASSWORDS AS PARAMETERS INSTEAD OF ENTERING INTERACTIVELY:
	| 	If your five passwords are "Pa$$word", "Pas$w0rd", "pa$$word", "$ecret", and "wh4tever" then you could start the PowerMenu like this:
	| 	NOTE: '$' characters must be escaped with a '\'
	| 	
	| 		python pm.py --fgwpw "Pa\$\$word" --apopw "Pas\$w0rd" --apapw "pa\$\$word" --apnopw "\$ecret" --apnapw "wh4tever"
	| 		
	|---------------------------------------------------------------------------------------

After entering the last password the program will go on to start loading data:

        Writing alarmDB to file for later use...
        Running check for CRTNTX35CR9S01
        Now parsing output for CRTNTX35CR9S01
        Running check for SNTDCAUJCR9S01
        Now parsing output for SNTDCAUJCR9S01
        Running check for SNAPCAHHCR9S01
        Now parsing output for SNAPCAHHCR9S01
        Running check for SNAPCAHHCR9S02
        Now parsing output for SNAPCAHHCR9S02
        Running check for NWTPMOABCR9S01
        Now parsing output for NWTPMOABCR9S01
        Running check for NWTPMOABCR9S02
        Now parsing output for NWTPMOABCR9S02
        Running check for RCPKNJ02CR9S01
        Now parsing output for RCPKNJ02CR9S01
        Running check for ATLNGAACCR9S01
        Now parsing output for ATLNGAACCR9S01
        Running check for LKMRFLMFCR9S01
        Now parsing output for LKMRFLMFCR9S01
        Running check for CLMAMDORCR9S01
        Now parsing output for CLMAMDORCR9S01
        Now parsing provisioning XML to build inventory. XML file: ../wicldumps/RAWDATA-provisioning.dat
        . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
         . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 
         . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
        Now converting Alarm dictionary to list of Alarm objects...
        . . . . . . . . . . . . . . . . . .
        Writing alarmDBo to file for later use...
        Writing inventory to file for later use...


        Enter Command ('h' for help):

		
At this point you should have a successful data pull and you can begin to work with the data. You can always see info about your current data by 
sending the "i" command like this:

        Enter Command ('h' for help): i
                 ====CURRENT SESSION INFORMATION====
                 STATISTICS
                 ------------------------------------------
                 Number of ALARMS total:                 932
                 Number of ALARMS ON MONITORED APs:      171
                 Number of ALARMS ON UNMONITORED APs:    421

                 Number of APs:                          7234
                 Number of known registered APs:         6504
                 Number of known unregistered APs:       730
                 Number of UNMONITORED APs:              1415

                 Number of MONITORED APs:        5552
                 Number of APs with UNKNOWN status: 233
                 ------------------------------------------
                 Size of eeker.db_cts:                   34584   bytes.
                 Size of eeker.db_alarmsd:               11184   bytes.
                 Size of eeker.db_femtos:                260424  bytes.
                 Size of fgwList:                        5240    bytes.

                 WMS/WICL portion of invList last updated: 20150209_135821
                 FGW/BSG registrations portion of invList last updated: 20150209_135821

                 Dump results to CSV: False

                 List of files created in this session:

                        Length of file_log = 0

        Enter Command ('h' for help):

So in order to use this tool it's helpful to understand a little bit about the type of data pulled by the tool. There are four primary sets of data 
that are needed in order to get the most out of the tool: Alarms, WMS inventory, BSG inventory, and data from CTS/AOTS which I dub "PowerMenu food". With all of this 
information you can get a pretty comprehensive picture of what's out there on the network. The info screen shows you the status of your data. As long 
as your "last updated" timestamps are recent and you have no zeros or negative numbers listed for the line items you should ready to get started. 

After almost every command sent to the menu prompt you'll be sent back to the same prompt to select another choice. You'll always know the system 
is ready for input when you see the prompt: 

		Enter Command ('h' for help):
		
Let's go ahead and hit 'h' now to see what some of our help options are:

        Enter Command ('h' for help): h

        ===========================HELP MENU===========================================
        |                     ALARM DB INTERACTIONS
        |
        | cmd 9+dd will list alarms for:
        |        03 - CRTNTX35CR9S01 - Carrollton 1 - ClusterID: 101
        |        04 - SNTDCAUJCR9S01 - Santa Clara 1 - ClusterID: 1
        |        05 - SNAPCAHHCR9S01 - Santa Ana 1 - ClusterID: 51
        |        11 - SNAPCAHHCR9S02 - Santa Ana 2 - ClusterID: 52
        |        01 - NWTPMOABCR9S01 - Hazelwood 1 - ClusterID: 151
        |        02 - NWTPMOABCR9S02 - Hazelwood 2 - ClusterID: 152
        |        06 - RCPKNJ02CR9S01 - Rochelle Park 1 - ClusterID: 201
        |        07 - ATLNGAACCR9S01 - Decatur 1 - ClusterID: 301
        |        08 - LKMRFLMFCR9S01 - Lake Mary 1 - ClusterID: 351
        |        09 - CLMAMDORCR9S01 - Columbia 1 - ClusterID: 251
        |
        | example: '9+01' will list all alarms for NWTPMOABCR9S01 in table format
        | NOTE: by default results are filtered to not show 'unmonitored' AP's
        | To show all alarms including unmonitored enter command 'f<enter>9+dd'
        |
        | cmd 8+dd+searchterm will search the dd column for searchterm
        | default is 10 - additionalText
        |        11 - alarmedComponent
        |        10 - additionalText
        |        13 - bSRName
        |        12 - notificationIdentifier
        |        15 - eventTime
        |        14 - FemtoCluster
        |        16 - specificProblems

        | example: '8+45812' will search the 'additionalText' column for '45812'
        | example: '8+15+20140821' will search the 'eventTime' column for '20140821'
        |
        | cmd 7+dbindex will display the full item at index dbindex in the db
        | example 7+234
        |
        | the 'm' command will toggle the unmonitored filter
        | cmd '111' will reload Alarms from WMS
        |------------------------------------------------------------------------------
        |                     INVENTORY DB INTERACTIONS
        |
        | cmd 6+commonid will send a reboot command to that AP
        |   example: '6+LFYTLAM12233' will log into LFYTLAM12233 and reboot it
        |
        | cmd '5+' will dump the contents of the full femto inventory
        | cmd '5+a' will show all AP's with alarms
        |
        | cmd 4+commonID will kick off status check
        | example: 4+LFYTLAM12233
        |
        | cmd 3+dd+searchterm:
                will search the femto db for 'searchterm' in particular attribute
        | List of available attributes to search is:
        |        22 - serial
        |        23 - groupId
        |        28 - usid
        |        29 - clusterId
        |        27 - ctsname
        |        26 - ipsecIpAddr
        |        25 - faloc
        |        24 - groupName
        |        20 - bsrName
        |        21 - bsrId
        | example: '3+chrysler' will search for APs with 'chrysler' in the 'groupName'
        | example: '3+20+ORLNFLM02904' will search
        |           for APs with 'ORLNFLM02904' in the 'bsrName'
        |
        | cmd 2+dbindex:
        |      will display all alarms associated with the AP at index 'dbindex'
        | example: Find an AP with an alarm using 9+XX then 3+20+bsrname
        | example: Then send 2+thatindexnumber
        |   NOTE: Obviously AP must have an alarm to display any sort of results.
        |         You can tell by noting if the AP has an * in the 'alarm?' column
        |
        | the 'q' command will launch the custom query builder
        | the 's' command will search for cluster/group
        | the 'f' command will toggle wide format (show more data)
        | the 'g' command will run bulk status check on entire cluster/group
        | the 'b' command will prompt for dash-separated list of CommonID's to search
        | the 't' command will prompt to change the default value for AP check timeout
        | cmd '112' will reload AP's registered on all FGWs
        |
        |------------------------------------------------------------------------------
        |                      OTHER COMMANDS
        | the '+++' command will exit the program
        | the '113' command will refresh Alarm, Registration, and Provisioning data
        | the '114' command will refresh Alarm, and Registration data
        | the 'h' command will display this help
        | the 'u' command will show stuck bsrOutOfService alarms
        | the 'c' command will launch the color picker
        | the 'i' command will show statistics on the current session
        | the 'n' command will toggle CSV dumping on or off
        |   (When True, query results are written to CSV in the local directory
        |   example: 20141027_112201-metro.csv )
        | the 'e' command will email the results of the last query in CSV format
        | the 'e+N' command will email the last N results to
        |           an email address of your choice
        |   example: 'e+3' will send the last three CSV files by email.
        |   (NOTE: CSV dumping must be on for email support)
        | the 'a' command will toggle auto-update of data
        | the 'z' command will prompt for auto-update frequency
        ===========================HELP MENU===========================================

        Enter Command ('h' for help):



Now this help menu looks really confusing to start with but we'll walk through a few examples. 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ALARM DB INTERACTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's say you wanted to look at all of the current alarms on the Carollton 1 Gateway. You would enter command '9+03' and then you'd see results like this:

        Enter Command ('h' for help): 9+03

                                 Data Timestamp: 20150209_135659
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        175    20518268  noBSRInReceivedLAC             20150113152104      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 13                                                                     locked      101 CRTNTX35CR9S01
        174    20530062  noBSRInReceivedRAC             20150114111749      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 111                                                                    locked      101 CRTNTX35CR9S01
        173    20530109  noBSRInReceivedLAC             20150114112113      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 8                                                                      locked      101 CRTNTX35CR9S01
        488    21255302  lmcFailure                     20150202232334      FemtoCluster 101 FemtoGroup 34 Femto 8670                                DLLSDXM13947        Monitored     unlocked    101 CRTNTX35CR9S01
        492    21399951  lmcFailure                     20150206171405      FemtoCluster 101 FemtoGroup 22 Femto 5302                                HSTNHXM30548        Monitored     unlocked    101 CRTNTX35CR9S01
        491    21413895  lmcFailure                     20150207025122      FemtoCluster 101 FemtoGroup 54 Femto 10095                               DLLSDXM15201        Monitored     unlocked    101 CRTNTX35CR9S01
        493    21422180  lmcFailure                     20150207112103      FemtoCluster 101 FemtoGroup 30 Femto 5819                                DLLSDXM11225        Monitored     unlocked    101 CRTNTX35CR9S01
        486    21477614  lmcFailure                     20150209052341      FemtoCluster 101 FemtoGroup 20 Femto 4622                                AUSTTXM26284        Monitored     unlocked    101 CRTNTX35CR9S01
        485    21484056  lmcFailure                     20150209101457      FemtoCluster 101 FemtoGroup 36 Femto 8122                                HSTNHXM30915        Monitored     unlocked    101 CRTNTX35CR9S01
        495    21486760  lmcFailure                     20150209114549      FemtoCluster 101 FemtoGroup 13 Femto 3544                                DLLSDXM15277        Monitored     unlocked    101 CRTNTX35CR9S01
        483    21488834  associationEstablishmentFailur 20150209124913      FemtoCluster 101 FemtoGroup 13 Femto 3526 SCTPASSOC 1                    DLLSDXM15259        Monitored     unlocked    101 CRTNTX35CR9S01
        489    21488809  lmcFailure                     20150209125034      FemtoCluster 101 FemtoGroup 12 Femto 3418                                DLLSDXM09213        Monitored     unlocked    101 CRTNTX35CR9S01
        494    21489692  lmcFailure                     20150209132029      FemtoCluster 101 FemtoGroup 22 Femto 5293                                HSTNHXM30002        Monitored     unlocked    101 CRTNTX35CR9S01
        176    21490469  invalidIuflexConfiguration     20150209134649      FGW CRTNTX35CR9S01                                                                                         locked      101 CRTNTX35CR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 14

        Alarm Count: 17                 Results Name: Alarms for CRTNTX35CR9S01 - Carrollton 1
        Dsply Count: 14

        Enter Command ('h' for help):





The same format applies if you want to search for alarms on other Femto Gateways. For example, to see all alarms on Lake Mary you would enter command '9+08':

        Enter Command ('h' for help): 9+08

                                 Data Timestamp: 20150209_135659
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        155    21358812  noResponseFromBGWY             20150205094228      FemtoCluster 351 FemtoGroup 51 Femto 1493 ItfBGWY 1                      ORLNFLM02068        Monitored     unlocked    351 LKMRFLMFCR9S01
        156    21358811  noResponseFromBGWY             20150205094242      FemtoCluster 351 FemtoGroup 106 Femto 10596 ItfBGWY 1                    JCVLFLM00211        Monitored     unlocked    351 LKMRFLMFCR9S01
        164    21358803  noResponseFromBGWY             20150205094255      FemtoCluster 351 FemtoGroup 73 Femto 5114 ItfBGWY 1                      ORLNFLM02134        Monitored     unlocked    351 LKMRFLMFCR9S01
        162    21358805  noResponseFromBGWY             20150205094305      FemtoCluster 351 FemtoGroup 94 Femto 7488 ItfBGWY 1                      MIAMFLM25062        Monitored     unlocked    351 LKMRFLMFCR9S01
        158    21358818  noResponseFromBGWY             20150205094316      FemtoCluster 351 FemtoGroup 24 Femto 1340 ItfBGWY 1                      ORLNFLM02449        Monitored     unlocked    351 LKMRFLMFCR9S01
        604    21349359  noBSRInReceivedRAC             20150205101147      FGW LKMRFLMFCR9S01 FGWConfig 1 IuPS 103                                                                    locked      351 LKMRFLMFCR9S01
        157    21358819  sctpAssocAssociationDownAlarm  20150205110038      FemtoCluster 351 FemtoGroup 63 Femto 4631 SCTPASSOC 1                    MIAMFLM23002        Monitored     unlocked    351 LKMRFLMFCR9S01
        603    21381461  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2078                          ORLNFLM02078        Monitored     unlocked    351 LKMRFLMFCR9S01
        168    21419933  lmcFailure                     20150207093028      FemtoCluster 351 FemtoGroup 123 Femto 11861                              MIAMFLM25017        Monitored     unlocked    351 LKMRFLMFCR9S01
        151    21443965  autoconfigfailure              20150208011202      FemtoCluster 351 FemtoGroup 96 Femto 8635                                MIAMFLM25238        Monitored     unlocked    351 LKMRFLMFCR9S01
        167    21445856  lmcFailure                     20150208025346      FemtoCluster 351 FemtoGroup 103 Femto 10122                              MIAMFLM23204        Monitored     unlocked    351 LKMRFLMFCR9S01
        605    21479810  noBSRInReceivedRAC             20150209072321      FGW LKMRFLMFCR9S01 FGWConfig 1 IuPS 101                                                                    locked      351 LKMRFLMFCR9S01
        578    21490340  invalidIuflexConfiguration     20150209134226      FGW LKMRFLMFCR9S01                                                                                         locked      351 LKMRFLMFCR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 13

        Alarm Count: 50                 Results Name: Alarms for LKMRFLMFCR9S01 - Lake Mary 1
        Dsply Count: 13

        Enter Command ('h' for help):



Now by default, the tool will filter out displaying results for unmonitored APs based on the latest CTS food file it detected on load (default directory 
it scans for input file is '/home/customer/russ/pm_foodfiles'). You can tell when the results are being filtered because you'll see "Alarm Count" vs "Dsply Count"
at the bottom of the results list. If you want to turn off the unmonitored filter you can just issue the 'm' command and then run the query again. 

For example, if you issue the command 'm<enter>9+08' you'll see unfiltered results for Lake Mary. 

        Enter Command ('h' for help): m
        Unmonitored filter is: False
        Enter Command ('h' for help): 9+08

                                 Data Timestamp: 20150209_135659
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        153    21358814  csCnConnectivityLost           20150205093949      FemtoCluster 351 FemtoGroup 121 Femto 11819 IuCSPrime 1                  SNJNPRM28222        Not Monitored unlocked    351 LKMRFLMFCR9S01
        155    21358812  noResponseFromBGWY             20150205094228      FemtoCluster 351 FemtoGroup 51 Femto 1493 ItfBGWY 1                      ORLNFLM02068        Monitored     unlocked    351 LKMRFLMFCR9S01
        156    21358811  noResponseFromBGWY             20150205094242      FemtoCluster 351 FemtoGroup 106 Femto 10596 ItfBGWY 1                    JCVLFLM00211        Monitored     unlocked    351 LKMRFLMFCR9S01
        164    21358803  noResponseFromBGWY             20150205094255      FemtoCluster 351 FemtoGroup 73 Femto 5114 ItfBGWY 1                      ORLNFLM02134        Monitored     unlocked    351 LKMRFLMFCR9S01
        161    21358807  noResponseFromBGWY             20150205094256      FemtoCluster 351 FemtoGroup 121 Femto 11816 ItfBGWY 1                    SNJNPRM28219        Not Monitored unlocked    351 LKMRFLMFCR9S01
        162    21358805  noResponseFromBGWY             20150205094305      FemtoCluster 351 FemtoGroup 94 Femto 7488 ItfBGWY 1                      MIAMFLM25062        Monitored     unlocked    351 LKMRFLMFCR9S01
        158    21358818  noResponseFromBGWY             20150205094316      FemtoCluster 351 FemtoGroup 24 Femto 1340 ItfBGWY 1                      ORLNFLM02449        Monitored     unlocked    351 LKMRFLMFCR9S01
        163    21358804  noResponseFromBGWY             20150205094427      FemtoCluster 351 FemtoGroup 104 Femto 10283 ItfBGWY 1                    SNJNPRM27240        Not Monitored unlocked    351 LKMRFLMFCR9S01
        159    21358817  noResponseFromBGWY             20150205094443      FemtoCluster 351 FemtoGroup 82 Femto 5332 ItfBGWY 1                      ORLNFLM02618        Not Monitored unlocked    351 LKMRFLMFCR9S01
        154    21358813  csCnConnectivityLost           20150205100035      FemtoCluster 351 FemtoGroup 104 Femto 10285 IuCSPrime 1                  SNJNPRM27242        Not Monitored unlocked    351 LKMRFLMFCR9S01
        604    21349359  noBSRInReceivedRAC             20150205101147      FGW LKMRFLMFCR9S01 FGWConfig 1 IuPS 103                                                                    locked      351 LKMRFLMFCR9S01
        160    21358816  csCnConnectivityLost           20150205105804      FemtoCluster 351 FemtoGroup 121 Femto 11816 IuCSPrime 1                  SNJNPRM28219        Not Monitored unlocked    351 LKMRFLMFCR9S01
        157    21358819  sctpAssocAssociationDownAlarm  20150205110038      FemtoCluster 351 FemtoGroup 63 Femto 4631 SCTPASSOC 1                    MIAMFLM23002        Monitored     unlocked    351 LKMRFLMFCR9S01
        166    21367436  lmcFailure                     20150205181928      FemtoCluster 351 FemtoGroup 114 Femto 12227                              MIAMFLM25258        Not Monitored unlocked    351 LKMRFLMFCR9S01
        165    21372361  lmcFailure                     20150205211515      FemtoCluster 351 FemtoGroup 102 Femto 10047                              MIAMFLM25241        Not Monitored unlocked    351 LKMRFLMFCR9S01
        169    21381283  femtoNotInAuthorizedAreaGPS    20150206043947      FemtoCluster 351 FemtoGroup 122 Femto 11848 GPS 1                        SNJNPRM27220        Not Monitored unlocked    351 LKMRFLMFCR9S01
        579    21381487  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 27237                         SNJNPRM27237        Not Monitored unlocked    351 LKMRFLMFCR9S01
        580    21381485  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 25008                         MIAMFLM25008        Not Monitored unlocked    351 LKMRFLMFCR9S01
        581    21381484  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2582                          ORLNFLM02582        Not Monitored unlocked    351 LKMRFLMFCR9S01
        582    21381482  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2581                          ORLNFLM02581        Not Monitored locked      351 LKMRFLMFCR9S01
        583    21381471  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2115                          ORLNFLM02115        Not Monitored locked      351 LKMRFLMFCR9S01
        584    21381470  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 203                           JCVLFLM00203        Not Monitored locked      351 LKMRFLMFCR9S01
        585    21381469  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2116                          ORLNFLM02116        Not Monitored locked      351 LKMRFLMFCR9S01
        586    21381468  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 204                           JCVLFLM00204        Not Monitored locked      351 LKMRFLMFCR9S01
        587    21381467  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2117                          ORLNFLM02117        Not Monitored locked      351 LKMRFLMFCR9S01
        588    21381466  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 206                           JCVLFLM00206        Not Monitored locked      351 LKMRFLMFCR9S01
        589    21381481  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2580                          ORLNFLM02580        Not Monitored locked      351 LKMRFLMFCR9S01
        590    21381480  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2579                          ORLNFLM02579        Not Monitored locked      351 LKMRFLMFCR9S01
        591    21381479  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2578                          ORLNFLM02578        Not Monitored locked      351 LKMRFLMFCR9S01
        592    21381478  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 210                           JCVLFLM00210        Not Monitored locked      351 LKMRFLMFCR9S01
        593    21381477  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 212                           JCVLFLM00212        Not Monitored locked      351 LKMRFLMFCR9S01
        594    21381476  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2020                          ORLNFLM02020        Not Monitored locked      351 LKMRFLMFCR9S01
        595    21381475  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2023                          ORLNFLM02023        Not Monitored locked      351 LKMRFLMFCR9S01
        596    21381474  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2157                          ORLNFLM02157        Not Monitored unlocked    351 LKMRFLMFCR9S01
        597    21381473  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2171                          ORLNFLM02171        Not Monitored locked      351 LKMRFLMFCR9S01
        598    21381472  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2503                          ORLNFLM02503        Unknown       unlocked    351 LKMRFLMFCR9S01
        599    21381465  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2118                          ORLNFLM02118        Not Monitored locked      351 LKMRFLMFCR9S01
        600    21381464  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 208                           JCVLFLM00208        Not Monitored locked      351 LKMRFLMFCR9S01
        601    21381463  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2044                          ORLNFLM02044        Unknown       unlocked    351 LKMRFLMFCR9S01
        602    21381462  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2095                          ORLNFLM02095        Not Monitored unlocked    351 LKMRFLMFCR9S01
        603    21381461  bsrOutOfService                20150206044201      FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2078                          ORLNFLM02078        Monitored     unlocked    351 LKMRFLMFCR9S01
        170    21395935  femtoNotInAuthorizedAreaGPS    20150206145834      FemtoCluster 351 FemtoGroup 121 Femto 11831 GPS 1                        SNJNPRM28234        Not Monitored unlocked    351 LKMRFLMFCR9S01
        152    21418807  femtoNotInAuthorizedAreaGPS    20150207082804      FemtoCluster 351 FemtoGroup 121 Femto 11818 GPS 1                        SNJNPRM28221        Not Monitored unlocked    351 LKMRFLMFCR9S01
        168    21419933  lmcFailure                     20150207093028      FemtoCluster 351 FemtoGroup 123 Femto 11861                              MIAMFLM25017        Monitored     unlocked    351 LKMRFLMFCR9S01
        151    21443965  autoconfigfailure              20150208011202      FemtoCluster 351 FemtoGroup 96 Femto 8635                                MIAMFLM25238        Monitored     unlocked    351 LKMRFLMFCR9S01
        167    21445856  lmcFailure                     20150208025346      FemtoCluster 351 FemtoGroup 103 Femto 10122                              MIAMFLM23204        Monitored     unlocked    351 LKMRFLMFCR9S01
        171    21457895  femtoNotInAuthorizedAreaGPS    20150208140528      FemtoCluster 351 FemtoGroup 121 Femto 11830 GPS 1                        SNJNPRM28233        Not Monitored unlocked    351 LKMRFLMFCR9S01
        605    21479810  noBSRInReceivedRAC             20150209072321      FGW LKMRFLMFCR9S01 FGWConfig 1 IuPS 101                                                                    locked      351 LKMRFLMFCR9S01
        577    21489031  aclViolation                   20150209125814      FGW LKMRFLMFCR9S01                                                                           Unknown       locked      351 LKMRFLMFCR9S01
        578    21490340  invalidIuflexConfiguration     20150209134226      FGW LKMRFLMFCR9S01                                                                                         locked      351 LKMRFLMFCR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 50

        Alarm Count: 50                 Results Name: Alarms for LKMRFLMFCR9S01 - Lake Mary 1

        Enter Command ('h' for help):


Now you can see many more results and you no longer see "Dsply Count:" below the results. 
To turn filtering back on simply issue the 'm' command again:

		Enter Command ('h' for help): m
		Unmonitored filter is: True
		Enter Command ('h' for help):


Now let's say you wanted to search the alarm database for specific information. This is possible and can be done with the '8+XX+XXXXX" series of commands. 	
Let's take a closer look at this section of the help:

        | cmd 8+dd+searchterm will search the dd column for searchterm
        | default is 10 - additionalText
        |        11 - alarmedComponent
        |        10 - additionalText
        |        13 - bSRName
        |        12 - notificationIdentifier
        |        15 - eventTime
        |        14 - FemtoCluster
        |        16 - specificProblems

        | example: '8+45812' will search the 'additionalText' column for '45812'
        | example: '8+15+20140821' will search the 'eventTime' column for '20140821'

So let's say we want to look for an alarm for a particular AP and we already know the bsrName (a.k.a, CommonID). We can do that with a command like '8+13+ORLNFLM02078' :

        Enter Command ('h' for help): 8+13+ORLNFLM02078
        you searched for 'ORLNFLM02078' in column 'bSRName'

                 You searched for:       ORLNFLM02078

                  managedObjectClass                      1003
                  alarmedComponent                        FGW LKMRFLMFCR9S01 FGWConfig 1 BSG 1 Femto 2078
                  eventTime                               20150206044201
                  monitoredStatus                         Monitored
                  probableCause                           operationalCondition
                  eventType                               equipmentAlarm
                  notificationIdentifier                  21381461
                  bSRName                                 ORLNFLM02078
                  additionalText                          bsrOutOfService\n Nature:ADAC, Specific Problem:bsrOutOfService, Additional Information from NE:bSRName=ORLNFLM02078;Alarm raised in Active.BSRID:2078,, SecurityAlarmDetector:, ServiceUser:, ServiceProvider:
                  correlatedNotifications
                  activeStatus                            1
                  additionalKeyString                     21381461
                  unknownStatus                           0
                  perceivedSeverity                       MAJOR
                  specificProblems                        bsrOutOfService
                  managedObjectInstance                   NW UTRAN EM FGWLKMRFLMFCR9S01
                  alarmDisplayInfo                        {NW/UTRAN FGW/LKMRFLMFCR9S01 FGWConfig/1 BSG/1 Femto/2078} {LKMRFLMFCR9S01} {}
                ---------------
        done. Number of results: 1
        Enter Command ('h' for help):


So you can see from the results that we see one alarm that contains the text for that CommonID. 
From these results you can get an idea of what type of text is in each field. So now if we look at the other available fields to search we can get an 
idea of what we can search for.

For example, let's search the eventTime field for all alarms triggered on 2015/02/08. We could do this with a command like '8+15+20150208' :

        Enter Command ('h' for help): 8+15+20150208
        you searched for '20150208' in column 'eventTime'

                 You searched for:       20150208

                  managedObjectClass                      1003
                  alarmedComponent                        FemtoCluster 351 FemtoGroup 96 Femto 8635
                  eventTime                               20150208011202
                  monitoredStatus                         Monitored
                  probableCause                           applicationSubsystemFailure
                  eventType                               OperationalViolation
                  notificationIdentifier                  21443965
                  bSRName                                 MIAMFLM25238
                  additionalText                          autoconfigfailure\n Nature:ADAC, Specific Problem:autoconfigfailure, Additional Information from NE:bSRName=MIAMFLM25238,OUI-FSN=001D4C-1214020552,, SecurityAlarmDetector:, ServiceUser:, ServiceProvider:
                  Femto                                   8635
                  correlatedNotifications
                  FemtoGroup                              96
                  additionalKeyString                     21443965
                  FemtoCluster                            351
                  unknownStatus                           0
                  activeStatus                            1
                  perceivedSeverity                       MAJOR
                  specificProblems                        autoconfigfailure
                  managedObjectInstance                   NW UTRAN EM FemtoCluster351
                  alarmDisplayInfo                        {NW/UTRAN FemtoCluster/351 FemtoGroup/96 Femto/8635} {351} {}
                ---------------

....(Additional results filtered from this README)

                 You searched for:       20150208

                  managedObjectClass                      1003
                  alarmedComponent                        FemtoCluster 1 FemtoGroup 71 Femto 4909
                  eventTime                               20150208060021
                  monitoredStatus                         Monitored
                  probableCause                           applicationSubsystemFailure
                  eventType                               OperationalViolation
                  notificationIdentifier                  21448672
                  bSRName                                 DNVRCOM04296
                  additionalText                          autoconfigfailure\n Nature:ADAC, Specific Problem:autoconfigfailure, Additional Information from NE:bSRName=DNVRCOM04296,OUI-FSN=001D4C-1213150067,, SecurityAlarmDetector:, ServiceUser:, ServiceProvider:
                  Femto                                   4909
                  correlatedNotifications
                  FemtoGroup                              71
                  additionalKeyString                     21448672
                  FemtoCluster                            1
                  unknownStatus                           0
                  activeStatus                            1
                  perceivedSeverity                       MAJOR
                  specificProblems                        autoconfigfailure
                  managedObjectInstance                   NW UTRAN EM FemtoCluster1
                  alarmDisplayInfo                        {NW/UTRAN FemtoCluster/1 FemtoGroup/71 Femto/4909} {1} {}
                ---------------
        done. Number of results: 16
        Enter Command ('h' for help):



For that query we got quite a few results (16 results). It's just an example of the types of things you can do with the '8+XX+XXXX' series of commands

The last thing we can do with the Alarm DB is to reference a specific alarm from the table view using the 7+XX command. For example, let's say we've 
issued the '9+01' command and we're looking at the alarms on the 'Hazelwood 1' Gateway:

        Enter Command ('h' for help): 9+01

                                 Data Timestamp: 20150209_135659
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        332    20496823  noBSRInReceivedRAC             20150112050316      FGW NWTPMOABCR9S01 FGWConfig 1 IuPS 105                                                                    locked      151 NWTPMOABCR9S01
        368    20517602  noBSRInReceivedRAC             20150113143537      FGW NWTPMOABCR9S01 FGWConfig 1 IuPS 109                                                                    locked      151 NWTPMOABCR9S01
        342    20850863  noBSRInReceivedLAC             20150123085414      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 5                                                                      locked      151 NWTPMOABCR9S01
        370    20945719  bsrOutOfService                20150126013704      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 40908                         CLMBOHM40908        Monitored     unlocked    151 NWTPMOABCR9S01
        371    20945718  bsrOutOfService                20150126013704      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 40907                         CLMBOHM40907        Monitored     unlocked    151 NWTPMOABCR9S01
        372    20945717  bsrOutOfService                20150126013704      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 40906                         CLMBOHM40906        Monitored     unlocked    151 NWTPMOABCR9S01
        373    20945716  bsrOutOfService                20150126013704      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 40904                         CLMBOHM40904        Monitored     unlocked    151 NWTPMOABCR9S01
        278    21274020  lmcFailure                     20150203141723      FemtoCluster 151 FemtoGroup 22 Femto 3164                                KSCYKSM28209        Monitored     unlocked    151 NWTPMOABCR9S01
        343    21316956  bsrOutOfService                20150204191628      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17343                         INDYINM17343        Monitored     unlocked    151 NWTPMOABCR9S01
        344    21316955  bsrOutOfService                20150204191628      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17341                         INDYINM17341        Monitored     unlocked    151 NWTPMOABCR9S01
        348    21316966  bsrOutOfService                20150204191630      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17344                         INDYINM17344        Monitored     unlocked    151 NWTPMOABCR9S01
        347    21316967  bsrOutOfService                20150204191631      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17338                         INDYINM17338        Monitored     unlocked    151 NWTPMOABCR9S01
        346    21316968  bsrOutOfService                20150204191632      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17339                         INDYINM17339        Monitored     unlocked    151 NWTPMOABCR9S01
        337    21316973  bsrOutOfService                20150204191634      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17336                         INDYINM17336        Monitored     unlocked    151 NWTPMOABCR9S01
        338    21316972  bsrOutOfService                20150204191634      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17340                         INDYINM17340        Monitored     unlocked    151 NWTPMOABCR9S01
        339    21316971  bsrOutOfService                20150204191634      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17342                         INDYINM17342        Monitored     unlocked    151 NWTPMOABCR9S01
        341    21316970  bsrOutOfService                20150204191634      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17337                         INDYINM17337        Monitored     unlocked    151 NWTPMOABCR9S01
        345    21316969  bsrOutOfService                20150204191634      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17013                         INDYINM17013        Monitored     unlocked    151 NWTPMOABCR9S01
        340    21445784  noBSRInReceivedLAC             20150208024940      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 10                                                                     locked      151 NWTPMOABCR9S01
        272    21446271  autoconfigfailure              20150208032015      FemtoCluster 151 FemtoGroup 110 Femto 9322                               INDYINM17326        Monitored     unlocked    151 NWTPMOABCR9S01
        274    21469854  autoconfigfailure              20150208221721      FemtoCluster 151 FemtoGroup 60 Femto 6584                                DETRMIM15318        Monitored     unlocked    151 NWTPMOABCR9S01
        276    21478572  associationEstablishmentFailur 20150209061317      FemtoCluster 151 FemtoGroup 82 Femto 8288 SCTPASSOC 1                    CLEVOHM36250        Monitored     unlocked    151 NWTPMOABCR9S01
        282    21479988  sctpAssocAssociationDownAlarm  20150209072337      FemtoCluster 151 FemtoGroup 114 Femto 9405 SCTPASSOC 1                   OMAHNEM49198        Monitored     unlocked    151 NWTPMOABCR9S01
        290    21481564  lmcFailure                     20150209084141      FemtoCluster 151 FemtoGroup 54 Femto 5858                                STLSMOM30556        Monitored     unlocked    151 NWTPMOABCR9S01
        281    21488707  sctpAssocAssociationDownAlarm  20150209124735      FemtoCluster 151 FemtoGroup 42 Femto 4974 SCTPASSOC 1                    INDYINM17264        Monitored     unlocked    151 NWTPMOABCR9S01
        280    21488743  sctpAssocAssociationDownAlarm  20150209124843      FemtoCluster 151 FemtoGroup 32 Femto 3738 SCTPASSOC 1                    STLSMOM30220        Monitored     unlocked    151 NWTPMOABCR9S01
        279    21488752  associationEstablishmentFailur 20150209124854      FemtoCluster 151 FemtoGroup 42 Femto 4974 SCTPASSOC 1                    INDYINM17264        Monitored     unlocked    151 NWTPMOABCR9S01
        277    21488767  associationEstablishmentFailur 20150209124917      FemtoCluster 151 FemtoGroup 32 Femto 3738 SCTPASSOC 1                    STLSMOM30220        Monitored     unlocked    151 NWTPMOABCR9S01
        350    21488864  bsrOutOfService                20150209125152      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 30220                         STLSMOM30220        Monitored     unlocked    151 NWTPMOABCR9S01
        349    21488865  bsrOutOfService                20150209125153      FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 17264                         INDYINM17264        Monitored     unlocked    151 NWTPMOABCR9S01
        336    21489784  invalidIuflexConfiguration     20150209132338      FGW NWTPMOABCR9S01                                                                                         locked      151 NWTPMOABCR9S01
        364    21490559  noBSRInReceivedLAC             20150209134947      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 3                                                                      locked      151 NWTPMOABCR9S01
        367    21490564  noBSRInReceivedLAC             20150209134958      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 15                                                                     locked      151 NWTPMOABCR9S01
        357    21490571  noBSRInReceivedLAC             20150209135009      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 11                                                                     locked      151 NWTPMOABCR9S01
        356    21490573  noBSRInReceivedLAC             20150209135021      FGW NWTPMOABCR9S01 FGWConfig 1 IuCS 6                                                                      locked      151 NWTPMOABCR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 35

        Alarm Count: 117                        Results Name: Alarms for NWTPMOABCR9S01 - Hazelwood 1
        Dsply Count: 35

        Enter Command ('h' for help):



Now, if you notice that the far left column is labeled 'index'. This is an index number you can use to reference an individual alarm. You can view the full 
details of this alarm by isuing the '7+indexnumber' command like this:

        Enter Command ('h' for help): 7+350
        matched 7+dddddddddd

                  managedObjectClass                      1003
                  alarmedComponent                        FGW NWTPMOABCR9S01 FGWConfig 1 BSG 1 Femto 30220
                  eventTime                               20150209125152
                  monitoredStatus                         Monitored
                  probableCause                           operationalCondition
                  eventType                               equipmentAlarm
                  notificationIdentifier                  21488864
                  bSRName                                 STLSMOM30220
                  additionalText                          bsrOutOfService\n Nature:ADAC, Specific Problem:bsrOutOfService, Additional Information from NE:bSRName=STLSMOM30220;Alarm raised in Active.BSRID:30220,, SecurityAlarmDetector:, ServiceUser:, ServiceProvider:
                  FemtoGroup                              32
                  Femto                                   3738
                  correlatedNotifications
                  activeStatus                            1
                  additionalKeyString                     21488864
                  FemtoCluster                            151
                  unknownStatus                           0
                  perceivedSeverity                       MAJOR
                  specificProblems                        bsrOutOfService
                  managedObjectInstance                   NW UTRAN EM FGWNWTPMOABCR9S01
                  alarmDisplayInfo                        {NW/UTRAN FGW/NWTPMOABCR9S01 FGWConfig/1 BSG/1 Femto/30220} {NWTPMOABCR9S01} {}
        ---------------------
        Enter Command ('h' for help):


Since the tool works with offline data it's important to know how to refresh the database so you can see up-to-date information. 
Sending the '111' command will refresh alarm data from the source file. The source alarm data file is updated every 15 minutes and is
stored by default in /home/customer/russ/wicldumps/RAWDATA-alarms.dat

        Enter Command ('h' for help): 111
        matched 111, updating alarms only
        Updating alarms...
        Writing alarmDB to file for later use...
        Now converting Alarm dictionary to list of Alarm objects...
        . . . . . . . . . . . . . . . . . .
        Writing alarmDBo to file for later use...
        Writing inventory to file for later use...
        Enter Command ('h' for help):

Now lets query alarms again and look at the 'Data Timestamp' at the top of the results list:

        Enter Command ('h' for help): 9+05

                                 Data Timestamp: 20150209_143208
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        184    20821711  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 30373                         LSANCLM30373        Monitored     unlocked    51  SNAPCAHHCR9S01
        188    20821708  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18394                         LSANCLM18394        Monitored     unlocked    51  SNAPCAHHCR9S01
        190    20821707  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18396                         LSANCLM18396        Monitored     unlocked    51  SNAPCAHHCR9S01
        192    20821706  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18393                         LSANCLM18393        Monitored     unlocked    51  SNAPCAHHCR9S01
        206    20821705  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18392                         LSANCLM18392        Monitored     unlocked    51  SNAPCAHHCR9S01
        207    20821704  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18395                         LSANCLM18395        Monitored     unlocked    51  SNAPCAHHCR9S01
        219    20821326  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 18391                         LSANCLM18391        Monitored     unlocked    51  SNAPCAHHCR9S01
        220    20821325  bsrOutOfService                20150122210557      FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 30314                         LSANCLM30314        Monitored     unlocked    51  SNAPCAHHCR9S01
        524    21306711  state change disabled or degra 20150204131718      FemtoCluster 51 FemtoGroup 142 Femto 7550                                HAWIHIM48150        Monitored     unlocked    51  SNAPCAHHCR9S01
        511    21306741  state change disabled or degra 20150204131820      FemtoCluster 51 FemtoGroup 142 Femto 7551                                HAWIHIM48800        Monitored     unlocked    51  SNAPCAHHCR9S01
        515    21306767  state change disabled or degra 20150204131921      FemtoCluster 51 FemtoGroup 142 Femto 7556                                HAWIHIM48801        Monitored     unlocked    51  SNAPCAHHCR9S01
        512    21306801  state change disabled or degra 20150204132030      FemtoCluster 51 FemtoGroup 142 Femto 7557                                HAWIHIM48802        Monitored     unlocked    51  SNAPCAHHCR9S01
        523    21306832  state change disabled or degra 20150204132124      FemtoCluster 51 FemtoGroup 142 Femto 7552                                HAWIHIM48803        Monitored     unlocked    51  SNAPCAHHCR9S01
        526    21306865  state change disabled or degra 20150204132221      FemtoCluster 51 FemtoGroup 142 Femto 7553                                HAWIHIM48804        Monitored     unlocked    51  SNAPCAHHCR9S01
        528    21306901  state change disabled or degra 20150204132335      FemtoCluster 51 FemtoGroup 142 Femto 7554                                HAWIHIM48805        Monitored     unlocked    51  SNAPCAHHCR9S01
        520    21306931  state change disabled or degra 20150204132435      FemtoCluster 51 FemtoGroup 142 Femto 7555                                HAWIHIM48806        Monitored     unlocked    51  SNAPCAHHCR9S01
        518    21385038  autoconfigfailure              20150206082902      FemtoCluster 51 FemtoGroup 144 Femto 7809                                LSANCLM18209        Monitored     unlocked    51  SNAPCAHHCR9S01
        519    21413564  autoconfigfailure              20150207023302      FemtoCluster 51 FemtoGroup 139 Femto 7370                                LSANCLM34215        Monitored     unlocked    51  SNAPCAHHCR9S01
        522    21480012  sctpAssocAssociationDownAlarm  20150209072324      FemtoCluster 51 FemtoGroup 91 Femto 2554 SCTPASSOC 1                     LSANCLM34011        Monitored     unlocked    51  SNAPCAHHCR9S01
        521    21480014  associationEstablishmentFailur 20150209072325      FemtoCluster 51 FemtoGroup 91 Femto 2560 SCTPASSOC 1                     LSANCLM34205        Monitored     unlocked    51  SNAPCAHHCR9S01
        211    21491157  invalidIuflexConfiguration     20150209141051      FGW SNAPCAHHCR9S01                                                                                         locked      51  SNAPCAHHCR9S01
        217    21491310  noBSRInReceivedLAC             20150209141529      FGW SNAPCAHHCR9S01 FGWConfig 1 IuCS 9                                                                      locked      51  SNAPCAHHCR9S01
        216    21491584  noBSRInReceivedLAC             20150209142514      FGW SNAPCAHHCR9S01 FGWConfig 1 IuCS 1                                                                      locked      51  SNAPCAHHCR9S01
        510    21491616  state change disabled or degra 20150209142619      FemtoCluster 51 FemtoGroup 94 Femto 6118                                 LSANCLM30314        Monitored     unlocked    51  SNAPCAHHCR9S01
        218    21491635  noBSRInReceivedRAC             20150209142656      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 111                                                                    locked      51  SNAPCAHHCR9S01
        214    21491655  noBSRInReceivedRAC             20150209142729      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 107                                                                    locked      51  SNAPCAHHCR9S01
        194    21491677  noBSRInReceivedRAC             20150209142824      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 113                                                                    locked      51  SNAPCAHHCR9S01
        201    21491687  noBSRInReceivedRAC             20150209142846      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 115                                                                    locked      51  SNAPCAHHCR9S01
        183    21491697  noBSRInReceivedRAC             20150209142908      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 101                                                                    locked      51  SNAPCAHHCR9S01
        215    21491718  noBSRInReceivedLAC             20150209142954      FGW SNAPCAHHCR9S01 FGWConfig 1 IuCS 3                                                                      locked      51  SNAPCAHHCR9S01
        205    21491723  noBSRInReceivedRAC             20150209143005      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 105                                                                    locked      51  SNAPCAHHCR9S01
        209    21491730  noBSRInReceivedRAC             20150209143016      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 103                                                                    locked      51  SNAPCAHHCR9S01
        208    21491736  noBSRInReceivedRAC             20150209143027      FGW SNAPCAHHCR9S01 FGWConfig 1 IuPS 109                                                                    locked      51  SNAPCAHHCR9S01
        193    21491743  noBSRInReceivedLAC             20150209143038      FGW SNAPCAHHCR9S01 FGWConfig 1 IuCS 2                                                                      locked      51  SNAPCAHHCR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 34

        Alarm Count: 94                 Results Name: Alarms for SNAPCAHHCR9S01 - Santa Ana 1
        Dsply Count: 34

        Enter Command ('h' for help):


You can see that the timestamp for the data is now set to '20150209_143208' (02/09/2015 @ 2:32.08 PM EST). 
Take a look at one of the last lines from the output of the '111' command:

		Writing alarmDBo to file for later use...
		
This is a feature of the tool where it will write data to a file on disk so that you don't have to load data from WMS every time you run the tool. This is done 
automatically every time data is loaded from WMS and doesn't require intervention from the user. By default the tool will always try to load data from the local 
files instead of going to WMS. If the files do not exist it will go straight to WMS instead. 

The local files are hard coded to be stored in the same directory as the tool and are named as follows:
		DATABASE-ALARMS.pkl
		DATABASE-ALARMSo.pkl
		DATABASE-INVENTORY.pkl
		
More info on how the tool works with local files can be found in the "Advanced Information" section of this README

So you see that you have some pretty powerful tools for browsing information about the alarms that are coming from WMS and HDM. 

	
	
	
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~INVENTORY DB INTERACTIONS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First of all let's take a look at what the Inventory DB looks like. You can issue the command '5+' to see a full dump of the entire known database. I hope you're ready, this is a lot of data:

		Enter Command ('h' for help): 5+
		........
        5619   CLMASCM57001 1213370257 57001  Acme12345_Academy_of_  "ACME12345 ACADEMY M   "North-West corner"            Monitored      10.5.166.35     301  26   ATLNGAACCR9S01          152657   13056651    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5620   BTRGLAM04037 1214010003 4037   TEXARCANA_DOTD         "TEXARCANA DOTD SMAL   "1st Floor East Corner"        Monitored      10.8.148.31     301  41   ATLNGAACCR9S01          154946   13046458    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5621   NSVLTNM41797 1214260149 41797  JACKSONVILLE_BLVDERII  "JACKSONVILLE_BLVDER   "1st Floor System 9"           Not Monitored  10.5.168.176    301  148  ATLNGAACCR9S01          152845   13014454    Indoor  UMTS        BSR-14.02.44       unlocked
        5622   ATLNGAM25032 1214010044 25032  DALAARTWoodstock       "DALAART WOODSTOCK S   "MainLevel NE System1"         Monitored      10.11.151.88    301  66   ATLNGAACCR9S01          151671   13027284    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5623   CHRLNCM55216 1213230199 55216  EMBARGOINDY_Two_Uptow  "EMBARGOINDY - CHARL   "Floor 10 Center"              Monitored      10.5.169.137    301  16   ATLNGAACCR9S01          146991   12983784    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5624   VLDSGAM21261 1214210944 21261  BURNOUTS_Lodge_Spa     "BURNOUTS GARDENS LO   "Lodge 4th South Center"       Monitored      10.11.149.41    301  115  ATLNGAACCR9S01          162211   13254056    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5625   JCSNMSM06902 1214160025 6902   DALAARTMcComb          "DALAART MCCOMB SMAL   "MainLevel Center System4"     Monitored      10.8.147.208    301  68   ATLNGAACCR9S01          153134   13064987    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5626   ATLNGAM25295 1214140283 25295  Brownsvill_Civic_Cent  "GAINESVILLE CIVIC C   "Floor 3 NE Corner"            Not Monitored  10.2.148.55     301  113  ATLNGAACCR9S01          142192   12928965    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5627   LXTNKYM36917 1214010381 36917  DALAARTPaintsville     "DALAART PAINTSVILLE   "MainLevel NW System4"         Monitored      10.8.147.116    301  76   ATLNGAACCR9S01          158106   13078078    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5628   CHRLNCM55225 1213230348 55225  EMBARGOINDY_Two_Uptow  "EMBARGOINDY - CHARL   "Floor 12 Northeast Corner  ne Monitored      10.5.169.119    301  16   ATLNGAACCR9S01          146991   12983784    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5629   HNVIALM00011 1214210932 11     ICORRE_Graphics_AL     "ICORRE GRAPHICS SMA   "H-way nr cubicle 1091 and 109 Monitored      10.5.161.247    301  86   ATLNGAACCR9S01          156825   13115731    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5630   NSVLTNM41796 1214260114 41796  JACKSONVILLE_BLVDERII  "JACKSONVILLE_BLVDER   "1st Floor System 8"           Not Monitored  10.5.168.177    301  148  ATLNGAACCR9S01          152845   13014454    Indoor  UMTS        BSR-14.02.44       unlocked
        5631   ATLNGAM23029 1214030058 23029  Cooleri_City_Hall      "COOLERI CITY HALL S   "Grd Fl in front of restrms"   Monitored      10.5.170.120    301  58   ATLNGAACCR9S01          140760   12902330    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5632   SHPTLAM14214 1214230179 14214  International_Paper_L  "INTERNATIONAL PAPER   "Training Bldg N E Corner"     Monitored      10.2.143.122    301  64   ATLNGAACCR9S01          158203   13127515    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5633   MOBLALM10208 1214200041 10208  HUPPENSDOWNS           "HUPPENSDOWNS STEEL    "SCRM Social 1st Flr NW Corner Monitored      10.5.166.222    301  48   ATLNGAACCR9S01          151580   12924957    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5634   BTRGLAM04201 1214020907 4201   Woali_Construction     "WOALI CONSTRUCTION    "Trailer SouthEast Corner"     Monitored      10.5.170.96     301  54   ATLNGAACCR9S01          148557   12997959    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5635   HNVIALM00009 1213280079 9      DALAARTMuscleShoals    "DALAART MUSCLE SHOA   "MainLevel Center System1"     Monitored      10.8.145.8      301  63   ATLNGAACCR9S01          151666   13030256    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5636   ATLNGAM23218 1214030194 23218  Cooleri_City_Hall      "COOLERI CITY HALL S   "1st Fl corridor near  WH0211" Monitored      10.11.156.92    301  58   ATLNGAACCR9S01          140760   12902330    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5637   CHRLNCM55904 1214090186 55904  DALAARTLincolnton      "DALAART LINCOLNTON    "MainLevel Register System6"   Monitored      10.2.147.18     301  57   ATLNGAACCR9S01          155484   13078067    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5638   SVNHGAM21213 1214090073 21213  CARBREAKS_GA_Plant     "CARBREAKS PLANT AUG   "2nd Floor Room 201"           Monitored      10.5.163.136    301  56   ATLNGAACCR9S01          159263   13148104    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5639   CLMASCM57204 1213370475 57204  Acme12345_Academy_of_  "ACME12345 ACADEMY M   "South-East Corner"            Monitored      10.5.166.91     301  26   ATLNGAACCR9S01          152657   13056651    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5640   HNVIALM00291 1213280255 291    ARFERE_Huntsville_Red  "HUNTSVILLE REDSTONE   "Building 3 Floor 1 SW Corner" Monitored      10.8.146.223    301  14   ATLNGAACCR9S01          146592   12991769    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5641   RLGHNCM59240 1214060167 59240  DALAART_STORE_4459_SM  "DALAART STORE # 445   "NW"                           Monitored      10.2.143.16     301  120  ATLNGAACCR9S01          162709   13277144    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5642   EVVLKYM38917 1214060060 38917  DALAARTGlasgow         "DALAART GLASGOW SMA   "MainLevel Center system3"     Monitored      10.5.169.166    301  91   ATLNGAACCR9S01          158109   13079105    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5643   LXTNKYM36925 1214010408 36925  DALAARTPaintsville     "DALAART PAINTSVILLE   "MainLevel Register System12"  Monitored      10.2.148.69     301  76   ATLNGAACCR9S01          158106   13078078    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5644   BRHMALM02211 1213160296 2211   Hoover_Office          "BCC OFFICE BLDG - H   "1st Floor South"              Monitored      10.8.147.179    301  20   ATLNGAACCR9S01          140711   12852260    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5645   ATLNGAM25398 1214200712 25398  ROPID_TECHNOLOGIES     "ROPID TECHNOLOGIES    "Existing office 336"          Not Monitored  10.11.155.97    301  139  ATLNGAACCR9S01          160735   13224162    Indoor  UMTS        BSR-14.02.44       unlocked
        5646   LXTNKYM36223 1214200544 36223  BOBBY_DOLGERS_CLARK_H  "BOBBY_DOLGERS CLARK   "First Flr SW corner nr IDF 4" Not Monitored  10.11.150.242   301  97   ATLNGAACCR9S01          162057   13226777    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5647   CHRLNCM55218 1214010391 55218  DELIAGG_HUNTERSVILLE_  "DELIAGG - HUNTERSVI   "Floor 2 East Corner"          Monitored      10.8.142.32     301  82   ATLNGAACCR9S01          161600   13229338    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        5648   NSVLTNM40279 1214230132 40279  LEBANON_DALAART_SUPER  "DALAART LEBANON SMA   "1st Floor System 2"           Not Monitored  10.8.146.230    301  164  ATLNGAACCR9S01          152844   13014453    Indoor  UMTS        BSR-14.02.44       unlocked
		.........
        7248   BLTMMDM00214 1214200562 214    LOLINDUSTRY_Arlington  "LOLINDUSTRY SMALL C   "Floor20 system 8"             Not Monitored  offline         251  41   CLMAMDORCR9S01          146409   12979918    Indoor  UMTS   *                       locked
        7249   BLTMMDM00218 1214200625 218    LOLINDUSTRY_Arlington  "LOLINDUSTRY SMALL C   "Floor21 system 12"            Not Monitored  offline         251  41   CLMAMDORCR9S01          146409   12979918    Indoor  UMTS   *                       locked
        7250   BLTMMDM00015 1214200308 15     LOLINDUSTRY_Arlington  "LOLINDUSTRY SMALL C   "Floor19 system 1"             Not Monitored  offline         251  41   CLMAMDORCR9S01          146409   12979918    Indoor  UMTS   *    BSR-14.02.44       locked
        7251   BLTMMDM00203 1214200427 203    LOLINDUSTRY_Arlington  "LOLINDUSTRY SMALL C   "Floor19 system 4"             Not Monitored  offline         251  41   CLMAMDORCR9S01          146409   12979918    Indoor  UMTS   *                       locked
        7252   RCMDVAM24203 1214020683 24203  Laired_Services        "LAIRED SERVICES SMA   "File storage room"            Not Monitored  offline         251  31   CLMAMDORCR9S01          159920   13182109    Indoor  UMTS   *    BSR-04.03.57.a.2   locked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 7252
        Enter Command ('h' for help):



	

As you can see, we have over 7,000 results displayed here. Depending on your SSH client you probably can't see the top of the list. 
The important thing to note here is that there's a lot of data to work with and that you can interact with data within the column names. Here's a breakdown of what each column means:

	index
		This is proprietary number used by the tool. Currently as of v0.4 this field is not used. 
	bsrName
		This is what you would refer to as the "CommonID" of the Metrocell
	serial
		This is the serial number of the Metrocell.
	bsrId
		Self explanatory, the bsrId of the device as configured in WMS. 
	groupName
		This is the human readable description of the site or group name. This is the value that's configured in "Group name" in WMS provisioning. 
	ctsEquipName
		This is the data from the "Equipment Name" field in CTS/AOTS as fed in by the CTS food file. Usually this is slightly different from the WMS group name. 
	specInfo
		This is the user specific human readable info configured for each Metrocell. This is defined by BIG_COMPANY during the provisioning process.
	monitored?
		This is the tool's best guess on whether or not the Metrocell is monitored based on input from the unmonitored file provided to the tool.
	ipsecIpAddr
		This is the ipsec IP Address as the Metrocell is registered on the Femto Gateway. 
		If this field has an IP address it means that the AP is online and reachable for status checks.
	clstr
		The cluster ID of the Metrocell
	grp
		The group ID of the Metrocell
	fgw
		The particular Femto Gateway on which the Metrocell is registered
	gagr
		Whether the Metrocell is configured as a GRID or GATEWAY device. In order to see data here you must run the PowerMenu with the '-g' parameter on startup. 
	usid
		This is the data from the "USID" field in CTS/AOTS as fed in by the CTS food file.
	faLocCode
		This is the data from the "FA Location Code" field in CTS/AOTS as fed in by the CTS food file.
	inout
		This is the data from the "Metrocell AP Location" field in CTS/AOTS as fed in by the CTS food file. This usually contains info regarding whether or not the AP is indoor or outdoor. 
	tech
		This is the data from the "Technology" field in CTS/AOTS as fed in by the CTS food file. The PowerMenu only handles "UMTS" gracefully. 
	alarm?
		Whether or not there is an active alarm associated with this bsrName/CommonID
    swVersion
        The version of software installed on the AP. 
	adminStatus
		The current Administrative Status of the device. 
		If this is in a 'locked' state it's a pretty good indication that the Metrocell is still in the process of being optimized or provisioned.

The 2+index command will display all alarms associated with that AP entry in the inventory DB. Let's look at the relevant section from the in-program help.

		| cmd 2+dbindex will display all alarms associated with the AP at index 'dbindex'
		| example: send cmd '5+a' then pick an index number in left column
		| example: Then send 2+thatindexnumber
		|   NOTE: Obviously AP must have an alarm to display any sort of results.
		|         You can tell by noting if the AP has an * in the 'alarm?' column

So an example of that would be as follows:

        Enter Command ('h' for help): s
        Enter Cluster and Groupseparated by - (example: 1-100): 52-26
        You entered:
        Cluster:        52
        Group:          26

                         ipsecIpAddr's updated: 20150210_090245  Everything else updated: 20150210_090245
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        2573   HAWIHIM48804 1214020999 48804  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center West Corner"    Monitored      10.11.131.152   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2582   HAWIHIM48802 1214020911 48802  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center East Corner"    Monitored      10.11.131.153   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2595   HAWIHIM48805 1214030106 48805  Sihani_HI              "COUNTY OF PROBAN AU   "State Attorneys Off SW Corner Monitored      10.11.131.157   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2601   HAWIHIM48800 1214020559 48800  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center Northeast Corne Monitored      10.11.131.156   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2644   HAWIHIM48803 1214020992 48803  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center Southeast Corne Monitored      10.11.131.158   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2668   HAWIHIM48150 1214010337 48150  Sihani_HI              "COUNTY OF PROBAN AU   "Conference Room North Corner" Monitored      10.11.131.159   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2669   HAWIHIM48801 1214020806 48801  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center Northwest Corne Monitored      10.11.131.155   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        2690   HAWIHIM48806 1214060139 48806  Sihani_HI              "COUNTY OF PROBAN AU   "State Attorneys Off South Cor Monitored      10.11.131.154   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 8
        Enter Command ('h' for help):

		
Since I see that index '2573' has an alarm ( see the '*' in the 'alarm?' column). So to see more details on that I can run '2+2573'.
		
        Enter Command ('h' for help): 2+2573
        matched 2+dddddddddd

        Displaying all alarms for inventory entry with index: 2573

                  managedObjectClass                      1003
                  alarmedComponent                        FemtoCluster 51 FemtoGroup 142 Femto 7553
                  eventTime                               20150204132221
                  monitoredStatus                         Monitored
                  probableCause                           underlyingResourceUnavailable
                  eventType                               qualityOfServiceAlarm
                  notificationIdentifier                  21306865
                  bSRName                                 HAWIHIM48804
                  additionalText                          state change disabled or degraded\n bSRName=HAWIHIM48804,OUI-FSN=001D4C-1214020999,associated Femto: Femto.7553 operationalStatus=disabled, availabilityStatus=failed
                  Femto                                   7553
                  correlatedNotifications
                  FemtoGroup                              142
                  additionalKeyString                     21306865
                  FemtoCluster                            51
                  unknownStatus                           0
                  activeStatus                            1
                  perceivedSeverity                       MAJOR
                  specificProblems                        state change disabled or degraded
                  managedObjectInstance                   NW UTRAN EM FemtoCluster51
                  alarmDisplayInfo                        {NW/UTRAN FemtoCluster/51 FemtoGroup/142 Femto/7553} {51} {}
        ---------------------

                                 Data Timestamp = NA
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        505    21306865  state change disabled or degra 20150204132221      FemtoCluster 51 FemtoGroup 142 Femto 7553                                HAWIHIM48804        Monitored     unlocked    51  SNAPCAHHCR9S01
        --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

        Number of results: 1

                         ipsecIpAddr's updated: 20150210_090245  Everything else updated: 20150210_090245
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        2573   HAWIHIM48804 1214020999 48804  Sihani_HI              "COUNTY OF PROBAN AU   "Sihani Center West Corner"    Monitored      10.11.131.152   52   26   SNAPCAHHCR9S02          152365   13029184    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 1
        Enter Command ('h' for help):



As you can see, the 2+index command is really useful for finding out which AP's have alarms in displayed groups. 

		
You can search the inventory DB by using the '3+XX+XXXXX' family of commands. For example, sending the '3+DODO' command will search for all Metrocells with "DODO" in the groupName:

        Enter Command ('h' for help): 3+DODO

        Searching Femto DB for 'DODO' in column 'groupName'

                         ipsecIpAddr's updated: 20150210_090245  Everything else updated: 20150210_090245
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        4175   NYCMNYM32083 1213360281 32083  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South West Corner" Monitored      10.11.131.83    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        4528   NYCMNYM32249 1213360378 32249  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South East Corner" Monitored      10.8.131.94     201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        4537   NYCMNYM32307 1214010103 32307  DODO_NYC               "DODO NYC SMALL CELL   "23rd Flr hallway near CEO off Monitored      10.11.131.98    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 3
        Enter Command ('h' for help):


To search other fields, let's take a look at the relevant section of the help menu:

| cmd 3+dd+searchterm:
|        will search the femto db for 'searchterm' in particular attribute
| List of available attributes to search is:
|        22 - serial
|        23 - groupId
|        28 - usid
|        29 - clusterId
|        27 - ctsname
|        26 - ipsecIpAddr
|        25 - faloc
|        24 - groupName
|        20 - bsrName
|        21 - bsrId
| example: '3+chrysler' will search for APs with 'chrysler' in the 'groupName'
| example: '3+20+ORLNFLM02904' will search
|           for APs with 'ORLNFLM02904' in the 'bsrName'


So from this it's easy to see how to search for a particular serial number. For example, sending '3+22+1213160041' will search the 'serial' column for '1213160041':

        Enter Command ('h' for help): 3+22+1213160041

        Searching Femto DB for '1213160041' in column 'serial'

                         ipsecIpAddr's updated: 20150210_090245  Everything else updated: 20150210_090245
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        3621   CHCGILM02539 1213160041 2539   ClarkApartments        "CLARK APARTMENTS SM   "7th Floor System 21"          Monitored      10.11.188.226   152  26   NWTPMOABCR9S02          137562   12854455    Indoor  UMTS        BSR-04.03.57.a.2   unlocked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 1
        Enter Command ('h' for help):


There's a quicker way to search for AP's in a particular cluster and group: you can enter the 's' command to launch a query for a particular cluster/group combination 
as shown below. After hitting 's<enter>' you'll be asked to enter a cluster/group combination separated by dash (e.g., '201-15')

        Enter Command ('h' for help): s
        Enter Cluster and Groupseparated by - (example: 1-100): 201-15
        You entered:
        Cluster:        201
        Group:          15

                         ipsecIpAddr's updated: 20150210_095905  Everything else updated: 20150210_095905
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        6833   NYCMNYM32242 1213370449 32242  TYBEC_NYC              "TYBEC! - NEW YORK T   "12th Floor South Corner"      Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6834   NYCMNYM32243 1213370458 32243  TYBEC_NYC              "TYBEC! - NEW YORK T   "12th Floor West Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6835   NYCMNYM32232 1213370225 32232  TYBEC_NYC              "TYBEC! - NEW YORK T   "10th Floor Northeast Corner"  Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6836   NYCMNYM32233 1213370274 32233  TYBEC_NYC              "TYBEC! - NEW YORK T   "10th Floor East Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6837   NYCMNYM32234 1213370277 32234  TYBEC_NYC              "TYBEC! - NEW YORK T   "10th Floor South Corner"      Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6838   NYCMNYM32235 1213370283 32235  TYBEC_NYC              "TYBEC! - NEW YORK T   "10th Floor West Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6839   NYCMNYM32236 1213370288 32236  TYBEC_NYC              "TYBEC! - NEW YORK T   "10th Floor North Corner"      Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6840   NYCMNYM32237 1213370291 32237  TYBEC_NYC              "TYBEC! - NEW YORK T   "11th Floor Northeast Corner"  Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6841   NYCMNYM32044 1213360335 32044  TYBEC_NYC              "TYBEC! - NEW YORK T   "9th Floor Northeast Corner"   Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6842   NYCMNYM32238 1213370311 32238  TYBEC_NYC              "TYBEC! - NEW YORK T   "11th Floor East Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6843   NYCMNYM32228 1213360398 32228  TYBEC_NYC              "TYBEC! - NEW YORK T   "9th Floor East Corner"        Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6844   NYCMNYM32239 1213370336 32239  TYBEC_NYC              "TYBEC! - NEW YORK T   "11th Floor South Corner"      Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6845   NYCMNYM32229 1213370205 32229  TYBEC_NYC              "TYBEC! - NEW YORK T   "9th Floor South Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6846   NYCMNYM32240 1213370349 32240  TYBEC_NYC              "TYBEC! - NEW YORK T   "11th Floor West Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        6847   NYCMNYM32241 1213370351 32241  TYBEC_NYC              "TYBEC! - NEW YORK T   "11th Floor North Corner"      Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *    BSR-04.03.57.a.2   unlocked
        6848   NYCMNYM32230 1213370210 32230  TYBEC_NYC              "TYBEC! - NEW YORK T   "9th Floor West Corner"        Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        6849   NYCMNYM32231 1213370212 32231  TYBEC_NYC              "TYBEC! - NEW YORK T   "9th Floor North Corner"       Not Monitored  offline         201  15   RCPKNJ02CR9S01          150126   13032718    Indoor  UMTS   *                       locked
        ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm? swVersion          adminStatus

        Number of results: 17
        Enter Command ('h' for help):


Nowe let's get into some action commands. You can perform two basic operations from the menu tool: reboot an AP and check AP status. 

In order to reboot an AP you can send the 6+COMMMONID command. 
NOTE: The reboot command depends on the AP being registered so it must have an ipSecIPAddr listed.

Here's an example of a reboot. 

        Enter Command ('h' for help): 6+ATLNGAM23164
        Entering AP Reboot function.
        Checking to see if I have enough info.....      First I'll connect to the AP and check it's serial number...
                I connected to the AP and saw that it has serial number:        1212170029
                The serial I have in my database for that AP is:                1212170029
                I feel confident in running the reboot command.

                Are you absolutely sure you want to reboot 'ATLNGAM23164'? (y/n) y

                                        spawn ssh admin@10.187.167.139
                                        *************************** Warning Message ***************************
                                        This system is restricted solely to the operators authorised users
                                        for  legitimate  business  purposes  only.    The  actual  or  attempted
                                        unauthorised  access,  use or modification of this  system  is  strictly
                                        prohibited  by the operator.  Unauthorised users are  subject  to
                                        Company disciplinary  proceedings  and/or  criminal  and civil penalties
                                        under state, federal or other applicable domestic and foreign laws.  The
                                        use of this system may be monitored  and recorded for administrative and
                                        security  reasons.  Anyone accessing  this system expressly consents  to
                                        such monitoring and is advised that  if such monitoring reveals possible
                                        evidence of  criminal  activity,  the operator  may  provide the
                                        evidence of such activity to law  enforcement officials.  All users must
                                        comply with  the operators Corporate  Instructions  regarding the
                                        protection of the operators information assets.
                                        ************************************************************************
                                        admin@10.187.167.139's password:
                                        Last login: Tue Feb 10 15:57:07 2015 from 10.37.20.73
                                        [admin@ATLNGAACCR9S01_BONO1 ~]$ ssh localOperator@10.2.149.80
                                        Password:
                                        Last login: Tue Feb 10 15:57:08 2015 from 172.23.92.183

                                        Linux femto-1212170029 2.6.34.8-femtobsr-femtobsrv2-alu ALU HomeBSR armv6l GNU/Linux

                                            FSN 1212170029
                                            MAC 00:30:ab:2a:64:15
                                            GDF BSR-14.02.44

                                        primuser@femto-1212170029:/$ su - localAdmin
                                        Password:
                                        root@femto-1212170029:~# reboot

                        I sent the reboot command!
                        In about 10 minutes refresh BSR ipSecIpAddr registrations with command '112'
                        After that you should be able to status the AP
        Enter Command ('h' for help):


You can issue a status check command by sending the '4+commonid' command (e.g., '4+NYCMNYM32307') as shown below:

Enter Command ('h' for help): 4+NYCMNYM32307
Detected status check request...

        Running status check for NYCMNYM32307 (1 of 1)
                                 Data Timestamp: 20150210_155924
        ----------------------------------------------------------------------------------------------------------------------------------------------------------
        Monitored        10.11.131.98             unlocked    unlocked    enabled     unlocked     enabled      YES  201  19   RCPKNJ02CR9S01        NYCMNYM32307
        ----------------------------------------------------------------------------------------------------------------------------------------------------------
        monitoredStatus  ipsecIpAddr     gagr     adminStatus bsrAStatus  bsrOStatus  cellAStatus  cellOStatus  UEs? clstrgrp  fgw            alarm? bsrName
        Number of results: 1
        (To collect syslog files from the previous check use 'y+')
        Would you like to see verbose results? (y/y+/n)


NOTE: The status check function only works when the tool has a listing for the ipsecIpAddr for a particular AP. If the tool has no IP address then it is unable to 
reach out and query the AP which means the AP is probably not registered with the FGW. 

The 'status' display format is slightly different from the alarm and inventory views. Here is a breakdown of the column descriptions:

monitoredStatus
	Same as with the inventory database, this is just the tool's best guess as to whether this is a monitored AP based on input from the unmonitored file.
ipsecIpAddr
	Same as with the inventory database, the ipsec IP address that is registered on the FGW.
gagr
	Whether or not the AP is listed as a GRID or GATEWAY device in WMS. 
adminStatus
	Whether the AP is administratively locked or unlocked.
bsrAStatus
	BSR Administrative Status - This is data directly from the AP. This is whether or not the AP believes it is administratively unlocked or not. 
bsrOStatus
	BSR Operational Status - This is data directly from the AP. This is whether or not the AP is in an operationlly enabled state. 
cellAStatus
	LCell Administrative Status - This is data directly from the AP. This is whether or not the LCell on the device is administratively locked or not. 
cellOStatus
	LCell Operational Status - This is data directly from the AP. This is whether or not the LCell is operationally enabled or disabled. 
UEs?
	Does this device have UEs connected? This is data directly from the AP. This indicates whether or not devices (a.k.a., cell phones) are connected and using the AP. 
clstr
	The FemtoCluster this AP is associated with
grp
	The FemtoGroup this AP is associated with
fgw
	The parent FGW of this AP
alarm?
	An asterisk indicates this AP has an alarm associated with it
bsrName
	The bsrName of the device (a.k.a, CommonID)
	

After seeing the results in table format the tool will ask you if you want to see results in verbose format. Issuing 'y' will show results like this:

		Would you like to see verbose results? (y/n)y

						---NYCMNYM32307---
						LCell: unlocked/enabled
						BSR: unlocked/enabled
						ueStatus IMSI list:
								310410724778313                         310410733934192                         310410635917480
						First NonPrivate IP: 68.173.213.161
						Neighbor bsrIds:
								32083 32249
						LCell Up/Down Log (covers roughly the last three days):
								===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===
								root@femto-1214010103:~# echo LOCAL AP TIME IS: `date`
								LOCAL AP TIME IS: Wed Dec 31 10:00:13 EST 2014
								Dec 30 19:02:54 fpu1.vx: #EVENT# Cell is now up
								Dec 30 19:00:02 fpu1.vx: #EVENT# Cell is now down
								Dec 29 19:39:17 fpu1.vx: #EVENT# Cell is now up
								Dec 29 19:36:01 fpu1.vx: #EVENT# Cell is now down
								Dec 28 20:36:55 fpu1.vx: #EVENT# Cell is now up
								Dec 28 20:33:01 fpu1.vx: #EVENT# Cell is now down
								Dec 27 18:31:35 fpu1.vx: #EVENT# Cell is now up
								Dec 27 18:28:01 fpu1.vx: #EVENT# Cell is now down
								Dec 26 20:26:24 fpu1.vx: #EVENT# Cell is now up
								Dec 26 20:22:00 fpu1.vx: #EVENT# Cell is now down
								Dec 25 20:50:31 fpu1.vx: #EVENT# Cell is now up
								Dec 25 20:47:00 fpu1.vx: #EVENT# Cell is now down
								Dec 24 22:59:11 fpu1.vx: #EVENT# Cell is now up
								Dec 24 22:56:00 fpu1.vx: #EVENT# Cell is now down
								Dec 23 22:04:24 fpu1.vx: #EVENT# Cell is now up
								Dec 23 22:01:01 fpu1.vx: #EVENT# Cell is now down

						---------------------------
		Enter Command ('h' for help):

		
The verbose output will show you a little more information than the table format. It will list the IMSIs of all UEs connected to the AP and the bsrId's of neighbor 
APs as well as the first non-private IP address (or internet address) of the last hop router before reaching the internet. Additionally the verbose results contain a
rudimentary scan of the /var/log/syslog/messages.* logs on the AP which shows LCell up/down times. This info can be used to determine the "Return to Service" time 
for updating the CTS/AOTS tickets. Take note that times shown in the LCell Up/Down log are local for the AP's time zone. 

In addition to being able to run status check on a single AP you can run checks on an entire cluster/group of APs with the 'g' command. After issuing 'g<enter>' you 
can enter a desired cluster/group in the format '<cluster>-<group>' just like with the 's' command. See example below:

		Enter Command ('h' for help): g
		Enter Cluster and Group separated by - (example: 1-100): 1-17
		You entered:
		Cluster:        1
		Group:          17

						 ipsecIpAddr's updated: 20141231_093550          Everything else updated: 20141231_093550
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		910    PTLDORM58900 1214100247 58900  Asplitze_Steel         "ASPLITZER STEEL SMA   "3rd Flr NW Hallwy Cafe 322"   Monitored      10.11.148.64    1    17   SNTDCAUJCR9S01          146631   12989947    Indoor  UMTS       unlocked
		1069   PTLDORM58209 1213160309 58209  Asplitze_Steel         "ASPLITZER STEEL SMA   "4th Floor East Corner"        Monitored      10.11.143.215   1    17   SNTDCAUJCR9S01          146631   12989947    Indoor  UMTS       unlocked
		1545   PTLDORM58208 1213160187 58208  Asplitze_Steel         "ASPLITZER STEEL SMA   "4th Floor North Corner"       Monitored      10.11.148.80    1    17   SNTDCAUJCR9S01          146631   12989947    Indoor  UMTS       unlocked
		1727   PTLDORM58029 1213370359 58029  Asplitze_Steel         "ASPLITZER STEEL SMA   "3rd Floor - East Corner"      Monitored      10.11.147.81    1    17   SNTDCAUJCR9S01          146631   12989947    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 4
		
Before the tool reaches out and runs the checks it will ask you if you're sure you want to do this as it could take a long time for large groups.
		
		Are you sure you wan to run status check on this entire group? (y/n) y

		Running status check for PTLDORM58900 (1 of 4)
		Running status check for PTLDORM58209 (2 of 4)
		Running status check for PTLDORM58208 (3 of 4)
		Running status check for PTLDORM58029 (4 of 4)
								 Data Timestamp: 20141231_100344
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		Monitored        10.11.148.64             unlocked    unlocked    enabled     unlocked     enabled      no   1    17   SNTDCAUJCR9S01        PTLDORM58900
		Monitored        10.11.143.215            unlocked    unlocked    enabled     unlocked     enabled      no   1    17   SNTDCAUJCR9S01        PTLDORM58209
		Monitored        10.11.148.80             unlocked    unlocked    enabled     unlocked     enabled      YES  1    17   SNTDCAUJCR9S01        PTLDORM58208
		Monitored        10.11.147.81             unlocked    unlocked    enabled     unlocked     enabled      no   1    17   SNTDCAUJCR9S01        PTLDORM58029
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		monitoredStatus  ipsecIpAddr     gagr     adminStatus bsrAStatus  bsrOStatus  cellAStatus  cellOStatus  UEs? clstrgrp  fgw            alarm? bsrName
		Number of results: 4
		Would you like to see verbose results? (y/n)

And again, it will ask you if you want to see verbose results for the entire group...

		Would you like to see verbose results? (y/n)y

						---PTLDORM58900---
						LCell: unlocked/enabled
						BSR: unlocked/enabled
						ueStatus IMSI list:

						First NonPrivate IP: 0.0.0.0
						Neighbor bsrIds:
								58029 58208 58209
						LCell Up/Down Log (covers roughly the last three days):
								===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===
								root@femto-1214100247:~# echo LOCAL AP TIME IS: `date`
								LOCAL AP TIME IS: Wed Dec 31 07:03:09 PST 2014
								Dec 29 11:13:56 fpu1.vx: #EVENT# Cell is now up
								Dec 29 10:59:18 fpu1.vx: #EVENT# Cell is now down
								Dec 29 10:51:01 fpu1.vx: #EVENT# Cell is now up
								Dec 29 10:37:38 fpu1.vx: #EVENT# Cell is now down
								Dec 29 04:50:04 fpu1.vx: #EVENT# Cell is now up
								Dec 29 04:45:05 fpu1.vx: #EVENT# Cell is now down
								Dec 28 18:14:48 fpu1.vx: #EVENT# Cell is now up
								Dec 28 18:10:05 fpu1.vx: #EVENT# Cell is now down
								Dec 27 02:54:46 fpu1.vx: #EVENT# Cell is now up
								Dec 27 02:50:03 fpu1.vx: #EVENT# Cell is now down
								Dec 26 02:28:35 fpu1.vx: #EVENT# Cell is now up
								Dec 26 02:23:01 fpu1.vx: #EVENT# Cell is now down
								Dec 25 18:06:40 fpu1.vx: #EVENT# Cell is now up
								Dec 25 18:02:15 fpu1.vx: #EVENT# Cell is now down
								Dec 24 16:05:45 fpu1.vx: #EVENT# Cell is now up
								Dec 24 16:01:01 fpu1.vx: #EVENT# Cell is now down

						---------------------------

						---PTLDORM58209---
						LCell: unlocked/enabled
						BSR: unlocked/enabled
						ueStatus IMSI list:

						First NonPrivate IP: 0.0.0.0
						Neighbor bsrIds:
								58900 58029 58208
						LCell Up/Down Log (covers roughly the last three days):
								===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===
								root@femto-1213160309:~# echo LOCAL AP TIME IS: `date`
								LOCAL AP TIME IS: Wed Dec 31 07:03:20 PST 2014
								Dec 31 04:09:57 fpu1.vx: #EVENT# Cell is now up
								Dec 31 04:05:04 fpu1.vx: #EVENT# Cell is now down
								Dec 30 04:37:30 fpu1.vx: #EVENT# Cell is now up
								Dec 30 04:33:02 fpu1.vx: #EVENT# Cell is now down
								Dec 29 04:27:05 fpu1.vx: #EVENT# Cell is now up
								Dec 29 04:25:01 fpu1.vx: #EVENT# Cell is now down
								Dec 28 02:46:53 fpu1.vx: #EVENT# Cell is now up
								Dec 28 02:43:02 fpu1.vx: #EVENT# Cell is now down
								Dec 27 00:48:21 fpu1.vx: #EVENT# Cell is now up
								Dec 27 00:44:01 fpu1.vx: #EVENT# Cell is now down
								Dec 26 00:29:25 fpu1.vx: #EVENT# Cell is now up
								Dec 26 00:25:01 fpu1.vx: #EVENT# Cell is now down
								Dec 25 00:06:07 fpu1.vx: #EVENT# Cell is now up
								Dec 25 00:02:01 fpu1.vx: #EVENT# Cell is now down
								Dec 24 04:16:45 fpu1.vx: #EVENT# Cell is now up
								Dec 24 04:12:01 fpu1.vx: #EVENT# Cell is now down
								Dec 23 04:20:18 fpu1.vx: #EVENT# Cell is now up
								Dec 23 04:16:01 fpu1.vx: #EVENT# Cell is now down

						---------------------------

						---PTLDORM58208---
						LCell: unlocked/enabled
						BSR: unlocked/enabled
						ueStatus IMSI list:
								310410727682523
						First NonPrivate IP: 0.0.0.0
						Neighbor bsrIds:
								58900 58029 58209
						LCell Up/Down Log (covers roughly the last three days):
								===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===
								root@femto-1213160187:~# echo LOCAL AP TIME IS: `date`
								LOCAL AP TIME IS: Wed Dec 31 07:03:30 PST 2014
								Dec 30 13:03:36 fpu1.vx: #EVENT# Cell is now up
								Dec 30 12:40:17 fpu1.vx: #EVENT# Cell is now down
								Dec 29 21:34:50 fpu1.vx: #EVENT# Cell is now up
								Dec 29 21:30:03 fpu1.vx: #EVENT# Cell is now down
								Dec 28 21:30:57 fpu1.vx: #EVENT# Cell is now up
								Dec 28 21:26:06 fpu1.vx: #EVENT# Cell is now down
								Dec 27 10:14:32 fpu1.vx: #EVENT# Cell is now up
								Dec 27 09:55:45 fpu1.vx: #EVENT# Cell is now down
								Dec 26 13:39:08 fpu1.vx: #EVENT# Cell is now up
								Dec 26 13:35:06 fpu1.vx: #EVENT# Cell is now down
								Dec 25 13:35:03 fpu1.vx: #EVENT# Cell is now up
								Dec 25 13:30:01 fpu1.vx: #EVENT# Cell is now down

						---------------------------

						---PTLDORM58029---
						LCell: unlocked/enabled
						BSR: unlocked/enabled
						ueStatus IMSI list:

						First NonPrivate IP: 0.0.0.0
						Neighbor bsrIds:
								58208 58209 58900
						LCell Up/Down Log (covers roughly the last three days):
								===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===
								root@femto-1213370359:~# echo LOCAL AP TIME IS: `date`
								LOCAL AP TIME IS: Wed Dec 31 07:03:39 PST 2014
								Dec 31 03:50:30 fpu1.vx: #EVENT# Cell is now up
								Dec 31 03:46:01 fpu1.vx: #EVENT# Cell is now down
								Dec 30 03:41:22 fpu1.vx: #EVENT# Cell is now up
								Dec 30 03:37:01 fpu1.vx: #EVENT# Cell is now down
								Dec 29 05:45:06 fpu1.vx: #EVENT# Cell is now up
								Dec 29 05:41:00 fpu1.vx: #EVENT# Cell is now down
								Dec 28 04:36:31 fpu1.vx: #EVENT# Cell is now up
								Dec 28 04:32:01 fpu1.vx: #EVENT# Cell is now down
								Dec 27 03:00:37 fpu1.vx: #EVENT# Cell is now up
								Dec 27 02:56:01 fpu1.vx: #EVENT# Cell is now down
								Dec 26 04:05:50 fpu1.vx: #EVENT# Cell is now up
								Dec 26 04:02:01 fpu1.vx: #EVENT# Cell is now down
								Dec 25 02:39:31 fpu1.vx: #EVENT# Cell is now up
								Dec 25 02:35:01 fpu1.vx: #EVENT# Cell is now down
								Dec 23 10:41:12 fpu1.vx: #EVENT# Cell is now up

						---------------------------
		Enter Command ('h' for help):
		
Sending the 'f' command will toggle between basic inventory view format and full format inventory view.

		Enter Command ('h' for help): f
		FullFormat toggle is: False
		Enter Command ('h' for help): 3+DODO

		Searching Femto DB for 'DODO' in column 'groupName'

						 ipsecIpAddr's updated: 20141231_102848          Everything else updated: 20141231_102848
		-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		4113   NYCMNYM32249 1213360378 32249  DODO_NYC               "23rd Floor South East Corner" Monitored      10.5.131.93     201  19   RCPKNJ02CR9S01          unlocked
		4197   NYCMNYM32307 1214010103 32307  DODO_NYC               "23rd Flr hallway near CEO off Monitored      10.2.130.124    201  19   RCPKNJ02CR9S01          unlocked
		4429   NYCMNYM32083 1213360281 32083  DODO_NYC               "23rd Floor South West Corner" Monitored      10.2.130.229    201  19   RCPKNJ02CR9S01          unlocked
		-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     adminStatus alarm?

		Number of results: 3
		
Notice how you see less data in when FullFormat is turned off? This is useful if you're on a laptop or smaller screen. To turn it back on simply issue the 'f' command again.
		
		Enter Command ('h' for help): f
		FullFormat toggle is: True
		Enter Command ('h' for help): 3+DODO

		Searching Femto DB for 'DODO' in column 'groupName'

						 ipsecIpAddr's updated: 20141231_102848          Everything else updated: 20141231_102848
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		4113   NYCMNYM32249 1213360378 32249  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South East Corner" Monitored      10.5.131.93     201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4197   NYCMNYM32307 1214010103 32307  DODO_NYC               "DODO NYC SMALL CELL   "23rd Flr hallway near CEO off Monitored      10.2.130.124    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4429   NYCMNYM32083 1213360281 32083  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South West Corner" Monitored      10.2.130.229    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 3
		Enter Command ('h' for help):


Sending the '112' command will refresh the data for all registered APs on the FGWs. An example is shown below. 
This can take up to 30 seconds depending on how many FGWs are listed.

		Enter Command ('h' for help): 112
		matched 112
		Reloading data from femto registrations...
		Running check for CRTNTX35CR9S01
		Now parsing output for CRTNTX35CR9S01
		Running check for SNTDCAUJCR9S01
		Now parsing output for SNTDCAUJCR9S01
		Running check for SNAPCAHHCR9S01
		Now parsing output for SNAPCAHHCR9S01
		Running check for SNAPCAHHCR9S02
		Now parsing output for SNAPCAHHCR9S02
		Running check for NWTPMOABCR9S01
		Now parsing output for NWTPMOABCR9S01
		Running check for NWTPMOABCR9S02
		Now parsing output for NWTPMOABCR9S02
		Running check for RCPKNJ02CR9S01
		Now parsing output for RCPKNJ02CR9S01
		Running check for ATLNGAACCR9S01
		Now parsing output for ATLNGAACCR9S01
		Running check for LKMRFLMFCR9S01
		Now parsing output for LKMRFLMFCR9S01
		Running check for CLMAMDORCR9S01
		Now parsing output for CLMAMDORCR9S01
		Number of AP's with new IP's since last load: 27
		
When the update is completed it will ask you if you want to see a detailed list of the APs with new ipsecIpAddr's.

This is useful if you're waiting for an AP to come online or if you're just curious. 
		
		Do you want to see the list of AP's that updated? (y/n)y

								 Data Timestamp: 20141231_100756
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		466    SNANSXM34227 1213370400 34227  DENDAG_Ranch_Encinal_  "DENDAG RANCH SMALL    "Ranch Hand"                   Monitored      10.11.135.112   101  27   CRTNTX35CR9S01          147753   12991773    Indoor  UMTS       unlocked
		525    SNANSXM34225 1213370188 34225  DENDAG_Ranch_Encinal_  "DENDAG RANCH SMALL    "Lodge -System 5"              Monitored      10.11.135.113   101  27   CRTNTX35CR9S01          147753   12991773    Indoor  UMTS       unlocked
		463    SNANSXM34222 1213370115 34222  DENDAG_Ranch_Encinal_  "DENDAG RANCH SMALL    "Bunk House"                   Monitored      10.11.135.114   101  27   CRTNTX35CR9S01          147753   12991773    Indoor  UMTS       unlocked
		446    SNANSXM34223 1213370499 34223  DENDAG_Ranch_Encinal_  "DENDAG RANCH SMALL    "Duplex IDF Location"          Monitored      10.11.135.115   101  27   CRTNTX35CR9S01          147753   12991773    Indoor  UMTS       unlocked
		6925   STTLWAM62242 1214160158 62242  ARFERE_South_Park      "ARFERE SOUTH PARK I   "Floor 2 in the Corridor lift" Not Monitored  10.5.171.183    1    158  SNTDCAUJCR9S01          161333   13239673    Indoor  UMTS   *   unlocked
		6924   STTLWAM62241 1214160157 62241  ARFERE_South_Park      "ARFERE SOUTH PARK I   "Flr2 in the Corridor Staircas Not Monitored  10.5.171.184    1    158  SNTDCAUJCR9S01          161333   13239673    Indoor  UMTS   *   unlocked
		6737   LSANCLM34223 1214210846 34223  CARBREAKS_Juicery      "CARBREAKS JUICERY I   "1st Floor Northwest Corner"   Monitored      10.2.145.128    51   166  SNAPCAHHCR9S01          160975   13224165    Indoor  UMTS   *   unlocked
		6738   LSANCLM34229 1214230340 34229  CARBREAKS_Juicery      "CARBREAKS JUICERY I   "1st Flr N Corner nr the cente Monitored      10.2.145.130    51   166  SNAPCAHHCR9S01          160975   13224165    Indoor  UMTS   *   unlocked
		2232   LSANCLM34222 1214210826 34222  CARBREAKS_Juicery      "CARBREAKS JUICERY I   "1st Flr N Corner nr in_egress Monitored      10.2.147.200    51   166  SNAPCAHHCR9S01          160975   13224165    Indoor  UMTS       unlocked
		3230   CLEVOHM36310 1214250233 36310  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "Basement Parking area"        Not Monitored  10.8.138.206    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		3147   CLEVOHM36318 1214250297 36318  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "2nd Floor Classroom 215"      Not Monitored  10.8.138.207    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		2888   CLEVOHM36319 1214250180 36319  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "2nd Floor Room 219 220"       Not Monitored  10.11.174.41    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		6368   CLEVOHM36317 1214250303 36317  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "2nd Floor Classroom 212"      Not Monitored  10.11.174.42    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		3175   CLMBOHM40913 1214030059 40913  HUPPENSDOWNSHamilton   "HUPPENSDOWNS HAMILT   "Buildg 8685 1st flr System 15 Monitored      10.2.158.25     151  138  NWTPMOABCR9S01          155718   13087784    Indoor  UMTS       unlocked
		4928   EVVLKYM38904 1214020502 38904  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Entry System6"      Monitored      10.2.143.211    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4936   EVVLKYM38906 1214010344 38906  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel W System8"          Monitored      10.2.143.210    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4887   EVVLKYM38907 1214020722 38907  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel E System9"          Monitored      10.2.143.201    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4871   EVVLKYM38908 1214010293 38908  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel NE System10"        Monitored      10.2.143.202    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		5001   EVVLKYM38900 1214010257 38900  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel NW System2"         Monitored      10.8.142.201    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4681   EVVLKYM38911 1214020584 38911  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Entry System13"     Monitored      10.2.143.203    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4924   EVVLKYM38903 1214020697 38903  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel W System5"          Monitored      10.2.143.206    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4813   EVVLKYM38912 1214020832 38912  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel SW System14"        Monitored      10.2.143.212    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4901   EVVLKYM38913 1214020728 38913  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Entry System15"     Monitored      10.2.143.208    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		6527   ATLNGAM23267 1214090016 23267  POBLANOSCITY_Hall      "POBLANOSCITY HALL S   "2nd Fl Assembly WD1006"       Not Monitored  10.5.159.41     301  58   ATLNGAACCR9S01          140760   12902330    Indoor  UMTS       unlocked
		5932   ORLNFLM02060 1213140236 2060   AK_Tunnel              "AFUNPLACETOBELANDER   ""                             Monitored      10.11.128.178   351  22   LKMRFLMFCR9S01          144590   12934862    Indoor  UMTS       unlocked
		5596   ORLNFLM02413 1213150128 2413   AK_Tunnel              "AFUNPLACETOBELANDER   "Tunnel - Stairway_14_Break Ar Monitored      10.11.128.179   351  22   LKMRFLMFCR9S01          144458   12934861    Indoor  UMTS       unlocked
		6180   WSS7TestAP   1212170029 13001  WSS7_TEST_CLMAMDORCR9                         "CLMAMDORCR9S01"               Unknown        10.8.133.120    251  48   CLMAMDORCR9S01                                                  unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 27
				Writing Inventory pickle to disk
		Enter Command ('h' for help):

	--NOTE--
	This only queries the FGWs for updated registrations (e.g., bsg_get_bsr_registrations) so it will not update WMS registrations/provisionings. 
	The only way to update WMS registrations is to run the '113' update command or delete the .pkl databases on disk before running the PowerMenu. 
	Since WMS provisioning happens much slower than FGW registrations and is driven by humans, it's usually sufficient to only updated the WMS registrations once at the beginning of the work day. 
	The '112' command really only reaches out to find new ipsecIpAddr's for registered APs. 
	--------
	
Now you'll notice that if you run any inventory queries you'll see an updated timestamp at the top of the results. The "Everything else updated" timestamp statement is 
referring to the WMS registrations information that is mentioned in the --NOTE-- above. The "ipsecIpAddr's updated:" statement is referring to the FGW registrations update that you just performed. 

		Enter Command ('h' for help): 3+DODO

		Searching Femto DB for 'DODO' in column 'groupName'

						 ipsecIpAddr's updated: 20141231_100756          Everything else updated: 20141231_093550
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		4120   NYCMNYM32249 1213360378 32249  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South East Corner" Monitored      10.5.131.93     201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4204   NYCMNYM32307 1214010103 32307  DODO_NYC               "DODO NYC SMALL CELL   "23rd Flr hallway near CEO off Monitored      10.2.130.124    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4437   NYCMNYM32083 1213360281 32083  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South West Corner" Monitored      10.2.130.229    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 3
		Enter Command ('h' for help):



		
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~REGULAR OPERATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
For daily continued usage here are some tips.

When running the program for the first time:
Navigate to the folder that contains the pm.py file, and your daily unmonitored APs list. 
Issue the "python pm.py" command. 

		$ pwd
		/home/customer/russ/pm
		$ ls -l
		total 17452
		-rw-r--r--   1 russ   grouper   888213 Dec 31 09:34 DATABASE-ALARMS.pkl
		-rw-r--r--   1 russ   grouper   415675 Dec 31 09:38 DATABASE-ALARMSo.pkl
		-rw-r--r--   1 russ   grouper  4347567 Dec 31 10:08 DATABASE-INVENTORY.pkl
		-rwxr-xr-x   1 russ   grouper     1957 Dec 30 15:52 EXP-apcheck.exp
		-rwxr-xr-x   1 russ   grouper      718 Dec 30 15:52 EXP-apreboot.exp
		-rwxr-xr-x   1 russ   grouper      373 Dec 30 15:52 EXP-getbsg.exp
		-rwxr-xr-x   1 russ   grouper      324 Dec 30 15:52 EXP-kh.exp
		-rw-r--r--   1 russ   grouper     2990 Dec 30 15:52 INSTRUCTIONS-UPGRADE.txt
		-rw-r--r--   1 russ   grouper     2943 Dec 30 15:52 INSTRUCTIONS.txt
		-rw-r--r--   1 russ   grouper  2521943 Dec 30 15:52 PowerMenu.Job.Aid.docx
		-rw-r--r--   1 russ   grouper   174104 Dec 30 15:52 README.txt
		-rw-r--r--   1 russ   grouper     3989 Dec 30 15:52 RELEASENOTES.txt
		-rw-r--r--   1 russ   grouper   293679 Dec 31 10:14 pm.log
		-rw-r--r--   1 russ   grouper    44662 Dec 31 09:34 pm.py
		-rw-r--r--   1 russ   grouper    14816 Dec 31 09:30 pmClasses.py
		-rw-r--r--   1 russ   grouper    13238 Dec 31 09:34 pmClasses.pyc
		-rw-r--r--   1 russ   grouper     8396 Dec 31 09:30 pmConfig.py
		-rw-r--r--   1 russ   grouper     5805 Dec 31 09:34 pmConfig.pyc
		-rw-r--r--   1 russ   grouper    26228 Dec 31 09:30 pmFunctions.py
		-rw-r--r--   1 russ   grouper    19458 Dec 31 09:34 pmFunctions.pyc
		-rw-r--r--   1 russ   grouper    43651 Dec 31 09:30 pmLoaders.py
		-rw-r--r--   1 russ   grouper    31417 Dec 31 09:34 pmLoaders.pyc
		$ python pm.py



The program will then initialize and load data from the .pkl files on disk. 


		 _____                       __  __
		|  __ \                     |  \/  |
		| |__) |____      _____ _ __| \  / | ___ _ __  _   _
		|  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | |
		| |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| |
		|_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_|
			   === ALU WMS Metrocell Power Menu ===
			   |     Creator: rendicott@gmail.com
			   |     Date: 2014-11-20
			   |     Version: 0.4.6
			   ====================================


		Current Directory: /home/customer/russ/pm

		Testing color support...
		starting up with loglevel 50 CRITICAL
		newest file detected: /home/customer/russ/pm_foodfiles/2014-12-31-06-31-09Powermenu-Food-CTS.csv

		Enter the password for the admin@FGW user:
		Enter again for verification:

		Enter the password for the localOperator@AP user:
		Enter again for verification:

		Enter the password for the localAdmin@AP user:
		Enter again for verification:


		Enter Command ('h' for help):


Once you see the "Enter Command" prompt the program is loaded and ready to use. You'll need to refresh the data in order to get the latest info from the network. 
		
		Enter Command ('h' for help): 113
		matched 113
		Reloading all data...
		Reloading registrations data...
		Running check for CRTNTX35CR9S01
		Now parsing output for CRTNTX35CR9S01
		Running check for SNTDCAUJCR9S01
		Now parsing output for SNTDCAUJCR9S01
		Running check for SNAPCAHHCR9S01
		Now parsing output for SNAPCAHHCR9S01
		Running check for SNAPCAHHCR9S02
		Now parsing output for SNAPCAHHCR9S02
		Running check for NWTPMOABCR9S01
		Now parsing output for NWTPMOABCR9S01
		Running check for NWTPMOABCR9S02
		Now parsing output for NWTPMOABCR9S02
		Running check for RCPKNJ02CR9S01
		Now parsing output for RCPKNJ02CR9S01
		Running check for ATLNGAACCR9S01
		Now parsing output for ATLNGAACCR9S01
		Running check for LKMRFLMFCR9S01
		Now parsing output for LKMRFLMFCR9S01
		Running check for CLMAMDORCR9S01
		Now parsing output for CLMAMDORCR9S01
		Number of AP's with new IP's since last load: 23

								 Data Timestamp: 20141231_102051
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		47     DLLSDXM09233 1214200375 9233   LIMEBOPE_Grapevine_TX  "LIMEBOPE-SMALLCELL"   "Level 2 System 6"             Monitored      10.11.135.117   101  67   CRTNTX35CR9S01          161538   12986745    Indoor  UMTS       unlocked
		3230   CLEVOHM36310 1214250233 36310  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "Basement Parking area"        Not Monitored  10.8.138.209    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		2888   CLEVOHM36319 1214250180 36319  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "2nd Floor Room 219 220"       Not Monitored  10.11.174.43    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		6368   CLEVOHM36317 1214250303 36317  BLEVELAND_METROPOLITA  "BMSD SMALLCELL"       "2nd Floor Classroom 212"      Not Monitored  10.11.174.44    151  209  NWTPMOABCR9S01          165684   13295800    Indoor  UMTS       unlocked
		4362   NYCMNYM32210 1213360056 32210  ACCORDY_NY             "RICHEMONT / ACCORDY   "5th floor West Corner"        Monitored      10.5.132.230    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4205   NYCMNYM32209 1213360034 32209  ACCORDY_NY             "RICHEMONT / ACCORDY   "5th floor South Corner"       Monitored      10.5.132.232    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4365   NYCMNYM32218 1213370063 32218  ACCORDY_NY             "RICHEMONT / ACCORDY   "7th floor East Corner"        Monitored      10.5.132.233    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4248   NYCMNYM32220 1213370082 32220  ACCORDY_NY             "RICHEMONT / ACCORDY   "7th floor West Corner"        Monitored      10.5.132.226    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4456   NYCMNYM32219 1213370069 32219  ACCORDY_NY             "RICHEMONT / ACCORDY   "7th floor South Corner"       Monitored      10.5.132.234    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4108   NYCMNYM32222 1213370185 32222  ACCORDY_NY             "RICHEMONT / ACCORDY   "7th floor Northeast center"   Monitored      10.5.132.231    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4098   NYCMNYM32223 1213370186 32223  ACCORDY_NY             "RICHEMONT / ACCORDY   "8th floor East Corner"        Monitored      10.5.132.225    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4350   NYCMNYM32226 1213370378 32226  ACCORDY_NY             "RICHEMONT / ACCORDY   "8th Floor North Corner"       Monitored      10.5.132.227    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4273   NYCMNYM32211 1213360480 32211  ACCORDY_NY             "RICHEMONT / ACCORDY   "5th Floor North Corner"       Monitored      10.5.132.228    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4306   NYCMNYM32227 1213370423 32227  ACCORDY_NY             "RICHEMONT / ACCORDY   "8th floor Northeast center"   Monitored      10.5.132.224    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4347   NYCMNYM32224 1213370192 32224  ACCORDY_NY             "RICHEMONT / ACCORDY   "8th floor South Corner"       Monitored      10.5.132.229    201  12   RCPKNJ02CR9S01          150133   13032719    Indoor  UMTS   *   unlocked
		4857   EVVLKYM38909 1214020713 38909  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Register System11"  Monitored      10.2.143.204    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4980   EVVLKYM38905 1214010458 38905  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Entry System7"      Monitored      10.2.143.209    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4979   EVVLKYM38901 1214020651 38901  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel NE System3"         Monitored      10.2.143.207    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4774   EVVLKYM38914 1214020781 38914  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Register System16"  Monitored      10.8.142.198    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4841   EVVLKYM38910 1214020700 38910  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Register System12"  Monitored      10.2.143.205    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4904   EVVLKYM38002 1214020833 38002  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel N System1"          Monitored      10.8.142.199    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		4939   EVVLKYM38902 1214020989 38902  DALAARTLeitchfield     "DALAART LEITCHFIELD   "MainLevel Center System4"     Monitored      10.8.142.200    301  77   ATLNGAACCR9S01          158108   13078080    Indoor  UMTS       unlocked
		5698   ORLNFLM02031 1213160108 2031   lalap_Norway           "AFUNP lalap - NORWA   "Main Floor - North Area"      Monitored      10.11.128.181   351  53   LKMRFLMFCR9S01          144611   12934874    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 23
		Reloading provisioning data...
		Now parsing provisioning XML to build inventory. XML file: /home/customer/russ/wicldumps/RAWDATA-provisioning.dat
		. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
		Reloading alarm data...
		Writing alarmDB to file for later use...
		Now converting Alarm dictionary to list of Alarm objects...
		. . . . . . . . . . . . . . . .
		Writing alarmDBo to file for later use...
				Writing Alarms pickle to disk
		Writing inventory to file for later use...
				Writing Inventory pickle to disk

		Enter Command ('h' for help):


If you ever get into a situation where you don't trust the freshness of the data you can always just clear out the .pkl files and start fresh. 
To clear out all of this data and start fresh you can issue these commands:

'rm *.pkl' - (Delete the existing .pkl files so that the tool will be forced to get new data from WMS/FGW.)
'rm *.csv' = (Delete the old CSV output files.)

		$ pwd
		/home/customer/russ/pm
		$ ls -l
		total 16796
		-rw-r--r--   1 russ   grouper   892244 Dec 31 10:24 DATABASE-ALARMS.pkl
		-rw-r--r--   1 russ   grouper   417595 Dec 31 10:24 DATABASE-ALARMSo.pkl
		-rw-r--r--   1 russ   grouper  4310654 Dec 31 10:24 DATABASE-INVENTORY.pkl
		-rwxr-xr-x   1 russ   grouper     1957 Dec 30 15:52 EXP-apcheck.exp
		-rwxr-xr-x   1 russ   grouper      718 Dec 30 15:52 EXP-apreboot.exp
		-rwxr-xr-x   1 russ   grouper      373 Dec 30 15:52 EXP-getbsg.exp
		-rwxr-xr-x   1 russ   grouper      324 Dec 30 15:52 EXP-kh.exp
		-rw-r--r--   1 russ   grouper     2990 Dec 30 15:52 INSTRUCTIONS-UPGRADE.txt
		-rw-r--r--   1 russ   grouper     2943 Dec 30 15:52 INSTRUCTIONS.txt
		-rw-r--r--   1 russ   grouper  2521943 Dec 30 15:52 PowerMenu.Job.Aid.docx
		-rw-r--r--   1 russ   grouper   174104 Dec 30 15:52 README.txt
		-rw-r--r--   1 russ   grouper     3989 Dec 30 15:52 RELEASENOTES.txt
		-rw-r--r--   1 russ   grouper        0 Dec 31 10:16 pm.log
		-rw-r--r--   1 russ   grouper    44662 Dec 31 09:34 pm.py
		-rw-r--r--   1 russ   grouper    14816 Dec 31 09:30 pmClasses.py
		-rw-r--r--   1 russ   grouper    13238 Dec 31 09:34 pmClasses.pyc
		-rw-r--r--   1 russ   grouper     8396 Dec 31 09:30 pmConfig.py
		-rw-r--r--   1 russ   grouper     5805 Dec 31 09:34 pmConfig.pyc
		-rw-r--r--   1 russ   grouper    26228 Dec 31 09:30 pmFunctions.py
		-rw-r--r--   1 russ   grouper    19458 Dec 31 09:34 pmFunctions.pyc
		-rw-r--r--   1 russ   grouper    43651 Dec 31 09:30 pmLoaders.py
		-rw-r--r--   1 russ   grouper    31417 Dec 31 09:34 pmLoaders.pyc
		$ rm *.pkl
		$ rm *.csv
		*.csv: No such file or directory
		$ ls -l
		total 5756
		-rwxr-xr-x   1 russ   grouper     1957 Dec 30 15:52 EXP-apcheck.exp
		-rwxr-xr-x   1 russ   grouper      718 Dec 30 15:52 EXP-apreboot.exp
		-rwxr-xr-x   1 russ   grouper      373 Dec 30 15:52 EXP-getbsg.exp
		-rwxr-xr-x   1 russ   grouper      324 Dec 30 15:52 EXP-kh.exp
		-rw-r--r--   1 russ   grouper     2990 Dec 30 15:52 INSTRUCTIONS-UPGRADE.txt
		-rw-r--r--   1 russ   grouper     2943 Dec 30 15:52 INSTRUCTIONS.txt
		-rw-r--r--   1 russ   grouper  2521943 Dec 30 15:52 PowerMenu.Job.Aid.docx
		-rw-r--r--   1 russ   grouper   174104 Dec 30 15:52 README.txt
		-rw-r--r--   1 russ   grouper     3989 Dec 30 15:52 RELEASENOTES.txt
		-rw-r--r--   1 russ   grouper        0 Dec 31 10:16 pm.log
		-rw-r--r--   1 russ   grouper    44662 Dec 31 09:34 pm.py
		-rw-r--r--   1 russ   grouper    14816 Dec 31 09:30 pmClasses.py
		-rw-r--r--   1 russ   grouper    13238 Dec 31 09:34 pmClasses.pyc
		-rw-r--r--   1 russ   grouper     8396 Dec 31 09:30 pmConfig.py
		-rw-r--r--   1 russ   grouper     5805 Dec 31 09:34 pmConfig.pyc
		-rw-r--r--   1 russ   grouper    26228 Dec 31 09:30 pmFunctions.py
		-rw-r--r--   1 russ   grouper    19458 Dec 31 09:34 pmFunctions.pyc
		-rw-r--r--   1 russ   grouper    43651 Dec 31 09:30 pmLoaders.py
		-rw-r--r--   1 russ   grouper    31417 Dec 31 09:34 pmLoaders.pyc
		$


Now you'll notice that the directory only contains the files necessary to run a fresh operation. 


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~OTHER COMMANDS~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

Sending the 'h' command will show the quick help for the tool. 

Sending the '+++' command will exit the program: 

		Enter Command ('h' for help): +++
		matched +++
		Good Bye!
		$

	To get back into the program just type 'python pm.py' to quickly get back into the tool and reload data from local files on disk. 

		 _____                       __  __
		|  __ \                     |  \/  |
		| |__) |____      _____ _ __| \  / | ___ _ __  _   _
		|  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | |
		| |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| |
		|_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_|
			   === ALU WMS Metrocell Power Menu ===
			   |     Creator: rendicott@gmail.com
			   |     Date: 2014-11-20
			   |     Version: 0.4.6
			   ====================================


		Current Directory: /home/customer/russ/pm

		Testing color support...
		starting up with loglevel 50 CRITICAL
		newest file detected: /home/customer/russ/pm_foodfiles/2014-12-31-06-31-09Powermenu-Food-CTS.csv

		Enter the password for the admin@FGW user:
		Enter again for verification:

		Enter the password for the localOperator@AP user:
		Enter again for verification:

		Enter the password for the localAdmin@AP user:
		Enter again for verification:


		Enter Command ('h' for help):

Sending the 'b' command will prompt for a dash-separated list of AP CommonID's. This will allow you to check the inventory for a specific list of 
APs regardless of whether or not they're part of the same cluster/group.

		Enter Command ('h' for help): b
		Enter list of CommonID's separated by '-' (e.g., 'CHCGILM02580-SPFDILM02648-SPFDILM02646'): JCVLFLM00202-ORLNFLM02476-DETRMIM15236-BLTMMDM00219-NYCMNYM32249
		Searching for 5 objects, hang on...
		Could not find the following Metrocell objects:
		BLTMMDM00219
		Successfully found the following Metrocell objects:


						 ipsecIpAddr's updated: 20141231_102848          Everything else updated: 20141231_102848
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		5709   JCVLFLM00202 1214200261 202    DALAART_Chipley        "DALAART CHIPLEY SMA   "NE"                           Not Monitored  10.5.129.130    351  106  LKMRFLMFCR9S01          158100   12888650    Indoor  UMTS       unlocked
		5904   ORLNFLM02476 1213050265 2476   WWS_Lampion_Gradyand   "AFUNP WIDE WORLD OF   "Ground Level - Officials Rm,  Monitored      10.2.128.130    351  58   LKMRFLMFCR9S01          144563   12934849    Indoor  UMTS       unlocked
		3354   DETRMIM15236 1213280067 15236  GMACGalleria           "AWE - GMAC GALLERIA   "2nd Floor Southwest"          Not Monitored  10.2.156.160    151  28   NWTPMOABCR9S01          146832   13027209    Indoor  UMTS       unlocked
		4113   NYCMNYM32249 1213360378 32249  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South East Corner" Monitored      10.5.131.93     201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 4
		Enter Command ('h' for help):



Sending the 'n' command will toggle the auto-generation of CSV files for every table that's displayed on the screen.

		Enter Command ('h' for help): n
		Auto-dump query results to CSV: True
		Enter Command ('h' for help):

		
	Now that CSV dumping is turned on you'll notice that at the bottom of every table view it will tell you the filename of the CSV report that it generated. 

			Enter Command ('h' for help): 9+03
			matched format 9+dd

									 Data Timestamp: 20141231_102737
			--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			250    19232600  noBSRInReceivedLAC             20141210113137      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 7                                                                      locked      101 CRTNTX35CR9S01
			217    19233234  noBSRInReceivedLAC             20141210113220      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 14                                                                     locked      101 CRTNTX35CR9S01
			214    19233251  noBSRInReceivedRAC             20141210113304      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 111                                                                    locked      101 CRTNTX35CR9S01
			254    19234783  noBSRInReceivedRAC             20141210114224      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 123                                                                    locked      101 CRTNTX35CR9S01
			207    19292316  noBSRInReceivedRAC             20141211011003      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 125                                                                    locked      101 CRTNTX35CR9S01
			218    19292334  noBSRInReceivedRAC             20141211011014      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 117                                                                    locked      101 CRTNTX35CR9S01
			213    19651105  noBSRInReceivedRAC             20141216024752      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 127                                                                    locked      101 CRTNTX35CR9S01
			210    19651138  noBSRInReceivedRAC             20141216024804      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 119                                                                    locked      101 CRTNTX35CR9S01
			212    19651129  noBSRInReceivedRAC             20141216024815      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 113                                                                    locked      101 CRTNTX35CR9S01
			211    19651136  noBSRInReceivedLAC             20141216024829      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 15                                                                     locked      101 CRTNTX35CR9S01
			251    19770678  dnsServerDownNode1             20141217024943      FGW CRTNTX35CR9S01 FGWConfig 1 DNS 1                                                                       locked      101 CRTNTX35CR9S01
			252    19770677  aspInactive                    20141217025414      FGW CRTNTX35CR9S01 FGWConfig 1 BSG 1 M3UA 1 IPSP 3                                                         locked      101 CRTNTX35CR9S01
			255    19770661  initialisationInProgress       20141217031402      FGW CRTNTX35CR9S01                                                                                         locked      101 CRTNTX35CR9S01
			249    19724724  noBSRInReceivedLAC             20141217031553      FGW CRTNTX35CR9S01 FGWConfig 1 IuCS 13                                                                     locked      101 CRTNTX35CR9S01
			253    19770673  aspInactive                    20141218010609      FGW CRTNTX35CR9S01 FGWConfig 1 BSG 1 M3UA 1 IPSP 4                                                         locked      101 CRTNTX35CR9S01
			215    19769113  noBSRInReceivedRAC             20141218010649      FGW CRTNTX35CR9S01 FGWConfig 1 IuPS 115                                                                    locked      101 CRTNTX35CR9S01
			523    20087498  lmcFailure                     20141226061133      FemtoCluster 101 FemtoGroup 11 Femto 3437                                DLLSDXM11213        Monitored     unlocked    101 CRTNTX35CR9S01
			537    20148681  lmcFailure                     20141228021342      FemtoCluster 101 FemtoGroup 67 Femto 10209                               DLLSDXM09230        Monitored     unlocked    101 CRTNTX35CR9S01
			532    20167555  lmcFailure                     20141228175231      FemtoCluster 101 FemtoGroup 54 Femto 10094                               DLLSDXM15008        Monitored     unlocked    101 CRTNTX35CR9S01
			535    20167603  lmcFailure                     20141228175333      FemtoCluster 101 FemtoGroup 54 Femto 10095                               DLLSDXM15201        Monitored     unlocked    101 CRTNTX35CR9S01
			541    20172089  lmcFailure                     20141228210035      FemtoCluster 101 FemtoGroup 22 Femto 5297                                HSTNHXM30543        Monitored     unlocked    101 CRTNTX35CR9S01
			518    20218533  autoconfigfailure              20141230060505      FemtoCluster 101 FemtoGroup 19 Femto 9813                                AUSTTXM26021        Monitored     unlocked    101 CRTNTX35CR9S01
			520    20219175  autoconfigfailure              20141230064810      FemtoCluster 101 FemtoGroup 44 Femto 8258                                TULSOKM04942        Monitored     unlocked    101 CRTNTX35CR9S01
			544    20229441  lmcFailure                     20141230132136      FemtoCluster 101 FemtoGroup 11 Femto 3419                                DLLSDXM11201        Monitored     unlocked    101 CRTNTX35CR9S01
			519    20236724  lmcFailure                     20141230170936      FemtoCluster 101 FemtoGroup 11 Femto 3441                                DLLSDXM11217        Monitored     unlocked    101 CRTNTX35CR9S01
			208    20258347  invalidIuflexConfiguration     20141231094524      FGW CRTNTX35CR9S01                                                                                         locked      101 CRTNTX35CR9S01
			545    20259067  lmcFailure                     20141231101024      FemtoCluster 101 FemtoGroup 67 Femto 10214                               DLLSDXM09233        Monitored     unlocked    101 CRTNTX35CR9S01
			--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
			index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

			Number of results: 27
																													 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_103403-alarm.csv

			Alarm Count: 79                 Results Name: Alarms for CRTNTX35CR9S01 - Carrollton 1
			Dsply Count: 27

			Enter Command ('h' for help):



	See in the above results where it says "WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_103403-alarm.csv".
	To access the generated CSV you can connect to WMS through FileZilla (SFTP) or you can use the email functionality.

Sending the 'e' command will email the last result file to an email address of your choice.


		Enter Command ('h' for help): e
				 Enter an email address ('q' to cancel): rendicott@gmail.com
		Sending email with the following information:

				 Subject:       PowerMenu Query Result
				 Body:          This report was generated by the Operations PowerMenu. Created by rendicott@gmail.com
				 Attach:        20141231_103403-alarm.csv
				 Recipient:     rendicott@gmail.com

		Enter Command ('h' for help):

		
	Sending the 'e+N' command will email the last N result CSVs instead of just the last result. (e.g., 'e+3' will send the last three CSVs)
	
	NOTE: The CSV dumping feature must be switched on in order to email a CSV. If CSV dumping is turned off and you attempt to email a report you'll receive a helpful warning message:
		
			Enter Command ('h' for help): e
			Oops, the file_log history is empty. Are you sure you have CSV dumping turned on? (HINT: 'n' to toggle, 'i' to check)
			Enter Command ('h' for help):

Sending the 'i' command will show some informational statistics about the current loaded session:

		Enter Command ('h' for help): i
				 ====CURRENT SESSION INFORMATION====
				 STATISTICS
				 ------------------------------------------
				 Number of ALARMS total:                 823
				 Number of ALARMS ON MONITORED APs:      152
				 Number of ALARMS ON UNMONITORED APs:    359

				 Number of APs:                          7123
				 Number of known registered APs:         6278
				 Number of known unregistered APs:       845
				 Number of UNMONITORED APs:              1594

				 Number of MONITORED APs:        5264
				 Number of APs with UNKNOWN status: 227
				 ------------------------------------------
				 Size of loo_ctsEntry:           34584   bytes.
				 Size of alarmDB:                9876    bytes.
				 Size of invList:                256428  bytes.
				 Size of fgwList:                5240    bytes.

				 WMS/WICL portion of invList last updated: 20141231_102848
				 FGW/BSG registrations portion of invList last updated: 20141231_102848

				 Dump results to CSV: True

				 List of files created in this session:
						 ------------------------------------
						 Filename: 20141231_103403-alarm.csv
						 Abs Path: /home/customer/russ/pm/20141231_103403-alarm.csv
						 Timestamp: 20141231_103403
						 ------------------------------------
						 Filename: 20141231_103610-alarm.csv
						 Abs Path: /home/customer/russ/pm/20141231_103610-alarm.csv
						 Timestamp: 20141231_103610
						 ------------------------------------
						 Filename: 20141231_103615-metrofull.csv
						 Abs Path: /home/customer/russ/pm/20141231_103615-metrofull.csv
						 Timestamp: 20141231_103615

						Length of file_log = 3

		Enter Command ('h' for help):
	
	Notice how at the end of the info screen you can see a list of all the CSV files generated in this session. 

Sending the 'c' command will launch the color picker. By default the tool does not use colors in the results display. If you wish to use colors:

		Enter Command ('h' for help): c

		1. Red like Radish
		2. Green like Grass
		3. Yellow like Yolk
		4. Blue like Blood
		5. Magenta like Mimosa
		6. Cyan like Caribbean
		7. White like Whipped Cream
		8. Crimson like Chianti
		9. Highlighted Red like Radish
		10. Highlighted Green like Grass
		11. Highlighted Brown like Bear
		12. Highlighted Blue like Blood
		13. Highlighted Magenta like Mimosa
		14. Highlighted Cyan like Caribbean
		15. Highlighted Gray like Ghost
		16. Highlighted Crimson like Chianti
		17. None like Nancy

		Default is Magenta like Mimosa
		Choose a color: 5
		You chose Magenta like Mimosa
		Enter Command ('h' for help): 

Sending the 't' command will launch the timeout picker. This lets you adjust the timeout for AP checks (e.g. 4+CommonID checks)

		Detected pattern: 't'
		Change value for AP check procedure timeout...

				1. 8 seconds.
				2. 12 seconds.
				3. 16 seconds.
				4. 24 seconds.
				5. 40 seconds.
				6. 50 seconds.

		Choose an AP check timeout value (default is 8 seconds): 4
		You chose 24 seconds.

		Exiting submenu timeout is set to: 24 seconds.
		Enter Command ('h' for help):

		
		
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~STUCK ALARM DETECTION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

The PowerMenu tool has a new experimental feature that allows the user to search for "Stuck" alarms. In order to understand what the feature can detect it's 
important to understand how it works.:

				"Stuck" Alarms Report
				Logic Flow Explanation

				This report is generated using the following logic:
				1. Pull all alarms using the WICL "FM getAlarm" command.
				2. Parse the alarms and determine which ones can be tied back to an AP

					 Examples of alarmedComponents that can be linked to an AP:
					 -FGW SNAPCAHHCR9S01 FGWConfig 1 BSG 1 Femto 355
					 -FemtoCluster 151 FemtoGroup 30 Femto 3598 SCTPASSOC 1

				3. Pull a list of all registered BSRs with ipSecIpAddr's by SSHing to each FGW and running the
				   /opt/bin/BSGConsole.exe bsg_get_bsr_registrations command.

				4. Parse the output from the bsg_get_bsr_registrations command and 
				   create individual "Metrocell" objects based on the data.

				5. From the BSR alarms, filter out the alarms that can't be discredited by statusing the AP. 

					 Types of stuck BSR alarms I can detect:
							DETECTABLE: bsrOutOfService
							  DETECTABLE: ipsecTunnelFailureNoResponse
							  DETECTABLE: sctpAssocAssociationDownAlarm
							  DETECTABLE: associationEstablishmentFailure
							  DETECTABLE: noResponseFromBGWY
					 
					 Types of stuck BSR alarms I can't verify:
							  UNDETECTABLE: lmcFailure
							  UNDETECTABLE: securityViolation

				6. Now we have a list of detectable BSR alarms and their associated BSRNames

				7. Take that list of BSRs and SSH to each one using the ipSecIpAddr for the registered BSR

				8. Use the $console > $menu options to determine LCell status and connected UE's, etc. 

				9. Parse the data from the AP to determine an overall healthy status. 
					Flag the Metrocell object as HEALTHY: True/False

					 (The output from this step is saved as the "suspect-BSRsXXXXXXXX_XXXXXX.csv" report)

				10. Compare again to the list of alarms. If the AP is healthy, then there's a chance that that 
					alarm is invalid. 

				11. Remove alarms from the list that are linked to an unhealthy AP.

				12. The resulting list of alarms is your "probably stuck" list. 

					 (The output from this step is saved as the "stuck-BSR-alarmsXXXXXX_XXXXXX.csv" report)

USAGE
To run the stuck alarm check you can issue the 'u' command. You'll be asked a series of questions regarding the type of check you wish to run. 

		Enter Command ('h' for help): u
		Detected pattern: 'u'
		Do you want to see 'Not Monitored' AP's? (y/n):

Answering 'n' to this question will cause the scan to only look at 'Monitored' AP's.

		Do you want to see 'Not Monitored' AP's? (y/n): n

		Types of stuck BSR alarms I can detect:
				 DETECTABLE: bsrOutOfService
				 DETECTABLE: ipsecTunnelFailureNoResponse
				 DETECTABLE: sctpAssocAssociationDownAlarm
				 DETECTABLE: associationEstablishmentFailure
				 DETECTABLE: noResponseFromBGWY

		Types of stuck BSR alarms I can't verify:
				 UNDETECTABLE: lmcFailure
				 UNDETECTABLE: securityViolation

		Do you want to limit search to 'bsrOutOfService' alarms only? (y/n):

After that, the list of detectable and undetectable alarms are listed. Answering 'y' to this question will cause the scan to only search for 'bsrOutOfService' alarms.
Answering 'n' to this question will cause the scan to search for all alarms in the "DETECTABLE" list. 

		Do you want to limit search to 'bsrOutOfService' alarms only? (y/n): n
		Do you want to see verbose results? (y/n):

The next question asks you if you want to see verbose results. This just gives you more information about what the scan is doing as it's running. Answering 'y' or 'n' leads you to the same results.

		Do you want to see verbose results? (y/n): n
		I noticed you had CSV output turned off. Do you want to output results to CSV? (y/n)

Next you'll be asked if you want to turn on CSV output. Turning this on will enable the check to send results of the scan by email.

		I noticed you had CSV output turned off. Do you want to output results to CSV? (y/n) y
		Do you want to email the results? (y/n)y
				Enter a single email address: rendicott@gmail.com

Along the same line of inquiry you'll be asked if you want to email the results and the email address you want to email to.

				Enter a single email address: rendicott@gmail.com

		Ok, checking for stuck alarms, this might take a bit...
		NOTE: AP's with administrativeState = 'locked' are filtered from this check.


		Now checking status of alarmed AP's, this could take up to 60 seconds...

		. . . . . Showing list of BSR's that have Alarms but appear to be online...


						 ipsecIpAddr's updated: 20141231_102848          Everything else updated: 20141231_102848
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		5592   ORLNFLM02060 1213140236 2060   MK_Tunnel              "AFUNPLACETOBELANDER   ""                             Monitored      10.11.128.178   351  22   LKMRFLMFCR9S01          144590   12934862    Indoor  UMTS   *   unlocked
		5580   ORLNFLM02361 1213060022 2361   lalap_Norway           "AFUNP lalap - NORWA   "Main Floor - East Area"       Monitored      10.8.128.197    351  53   LKMRFLMFCR9S01          144611   12934874    Indoor  UMTS   *   unlocked
		3479   CHCGILM02256 1213370273 2256   ABC_CORP               "ABC_CORPORATION SMA   "16th Floor Northeast Corner"  Monitored      10.5.165.119    152  10   NWTPMOABCR9S02          146986   13007928    Indoor  UMTS   *   unlocked
		3479   CHCGILM02256 1213370273 2256   ABC_CORP               "ABC_CORPORATION SMA   "16th Floor Northeast Corner"  Monitored      10.5.165.119    152  10   NWTPMOABCR9S02          146986   13007928    Indoor  UMTS   *   unlocked
		4420   NYCMNYM32277 1214020771 32277  BALMER_SALE            "BALMER_SALE - 7 WOR   "44th Floor South Corner"      Monitored      10.8.129.37     201  35   RCPKNJ02CR9S01          159854   13148105    Indoor  UMTS   *   unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 5
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_103919-metrofull.csv
																												 
First the tool will show you AP's that have ipSecIpAddr's and have alarms. 

		Now running detailed status check on APs with potential stuck alarms...

		Running status check for ORLNFLM02060 (1 of 5)
		Running status check for ORLNFLM02361 (2 of 5)
		Running status check for CHCGILM02256 (3 of 5)
		Running status check for CHCGILM02256 (4 of 5)
		Running status check for NYCMNYM32277 (5 of 5)
								 Data Timestamp: 20141231_104000
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		Monitored        10.11.128.178            unlocked    unlocked    enabled     unlocked     enabled      no   351  22   LKMRFLMFCR9S01 *      ORLNFLM02060
		Monitored        10.8.128.197             unlocked    unlocked    enabled     unlocked     enabled      YES  351  53   LKMRFLMFCR9S01 *      ORLNFLM02361
		Monitored        10.5.165.119             unlocked    unlocked    enabled     unlocked     enabled      no   152  10   NWTPMOABCR9S02 *      CHCGILM02256
		Monitored        10.5.165.119             unlocked    unlocked    enabled     unlocked     enabled      no   152  10   NWTPMOABCR9S02 *      CHCGILM02256
		Monitored        10.8.129.37              unlocked    unlocked    enabled     unlocked     enabled      no   201  35   RCPKNJ02CR9S01 *      NYCMNYM32277
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		monitoredStatus  ipsecIpAddr     gagr     adminStatus bsrAStatus  bsrOStatus  cellAStatus  cellOStatus  UEs? clstrgrp  fgw            alarm? bsrName
		Number of results: 5
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_104001-status.csv
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/suspect-BSRs20141231_104001.csv

Then the tool shows you the output of detailed checks on those APs.

		Now doing final comparison of AP's to OOS alarms...

		Showing final list of stuck alarms...


								 Data Timestamp: 20141231_102737
		--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		191    20258340  ipsecTunnelFailureNoResponse   20141229101103      FemtoCluster 351 FemtoGroup 22 Femto 1877                                ORLNFLM02060        Monitored     unlocked    351 LKMRFLMFCR9S01
		508    20202919  noResponseFromBGWY             20141229183623      FemtoCluster 201 FemtoGroup 35 Femto 9122 ItfBGWY 1                      NYCMNYM32277        Monitored     unlocked    201 RCPKNJ02CR9S01
		422    20259253  sctpAssocAssociationDownAlarm  20141231101713      FemtoCluster 152 FemtoGroup 10 Femto 6468 SCTPASSOC 1                    CHCGILM02256        Monitored     unlocked    152 NWTPMOABCR9S02
		427    20259272  associationEstablishmentFailur 20141231101752      FemtoCluster 152 FemtoGroup 10 Femto 6468 SCTPASSOC 1                    CHCGILM02256        Monitored     unlocked    152 NWTPMOABCR9S02
		199    20259341  ipsecTunnelFailureNoResponse   20141231102006      FemtoCluster 351 FemtoGroup 53 Femto 1547                                ORLNFLM02361        Monitored     unlocked    351 LKMRFLMFCR9S01
		--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  AlarmID   specificProblems               eventTime           alarmedComponent                                                         bSRName             monitored?    adminStatus cid fgwName

		Number of results: 5
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/stuck-BSR-alarms20141231_104001.csv
																												 
After that you'll see Alarms for APs with "healthy" status but still have alarms. That final listing is your "stuck" list.
																												 
		Sending email with the following information:

				 Subject:       PowerMenu Stuck Alarms Report
				 Body:          Refer to the attached CSVs for stuck alarms and list of corresponding BSR's.
				 Attach:        stuck-BSR-alarms20141231_104001.csv, suspect-BSRs20141231_104001.csv
				 Recipient:     rendicott@gmail.com

		Enter Command ('h' for help):

And the last thing the tool will show you is the email report. 

As you can see from the above check, there were only five stuck alarms at the time the check was run. 


		

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~MACRO OPERATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	

As of version 0.4.3 the tool supports sending a sequence of macro commands during the execution of the script. This allows you to quickly perform tedious
checks without having to babysit the tool. 

For example:
If you wanted to pull fresh data and then check the status of the NYC DODO SMALL CELL location and email the results you could run a sequence of commands like this:

		$ python pm.py -m "n,c,12,g,201-19,y,n,e+2,rendicott@gmail.com,+++" --fgwpw "Pa\$\$word" --apopw "Pas\$w0rd" --apapw "pa\$\$word"

So rather than waiting for the tool to prompt you with your desired actions, you can simply "pre-type" them and run through the sequence quickly.

	NOTE: The --fgwpw,--apopw, and --apapw parameters pass in the passwords ahead of time so you don't have to type them. 
	
To show you we'll break down the sequence of inputs so you understand what's going on:

n						This turns on the CSV dumping feature
c						This launches the color picker
12						This selects color '12' - 'Blue like Blood'
g						This launches the group status check.
201-19					This selects Cluster 201, Group 19 as the desired group to check
y						This confirms that we do really want to run the status check on the whole group.
n						This is us saying that we don't want to see verbose results.
e+2						This will email the last two generated CSV's to an email.
rendicott@gmail.com			This is telling the email sequence which email address to send results to. 
+++						This exits the program. 


The output from the above would look like this:

		$ python pm.py -m "n,c,12,g,201-19,y,n,e+2,rendicott@gmail.com,+++" --fgwpw "Pa\$\$word" --apopw "Pas\$w0rd" --apapw "pa\$\$word"

		 _____                       __  __
		|  __ \                     |  \/  |
		| |__) |____      _____ _ __| \  / | ___ _ __  _   _
		|  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | |
		| |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| |
		|_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_|
			   === ALU WMS Metrocell Power Menu ===
			   |     Creator: rendicott@gmail.com
			   |     Date: 2014-11-20
			   |     Version: 0.4.6
			   ====================================


		Current Directory: /home/customer/russ/pm

		Testing color support...
		starting up with loglevel 50 CRITICAL

		Detected the following macro order:
				n
				c
				12
				g
				201-19
				y
				n
				e+2
				rendicott@gmail.com
				+++
		newest file detected: /home/customer/russ/pm_foodfiles/2014-12-31-06-31-09Powermenu-Food-CTS.csv


		Auto-dump query results to CSV: True

		1. Red like Radish
		2. Green like Grass
		3. Yellow like Yolk
		4. Blue like Blood
		5. Magenta like Mimosa
		6. Cyan like Caribbean
		7. White like Whipped Cream
		8. Crimson like Chianti
		9. Highlighted Red like Radish
		10. Highlighted Green like Grass
		11. Highlighted Brown like Bear
		12. Highlighted Blue like Blood
		13. Highlighted Magenta like Mimosa
		14. Highlighted Cyan like Caribbean
		15. Highlighted Gray like Ghost
		16. Highlighted Crimson like Chianti
		17. None like Nancy

		Default is Magenta like Mimosa
		You chose Highlighted Blue like Blood
		You entered:
		Cluster:        201
		Group:          19

						 ipsecIpAddr's updated: 20141231_102848          Everything else updated: 20141231_102848
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		4113   NYCMNYM32249 1213360378 32249  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South East Corner" Monitored      10.5.131.93     201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4197   NYCMNYM32307 1214010103 32307  DODO_NYC               "DODO NYC SMALL CELL   "23rd Flr hallway near CEO off Monitored      10.2.130.124    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		4429   NYCMNYM32083 1213360281 32083  DODO_NYC               "DODO NYC SMALL CELL   "23rd Floor South West Corner" Monitored      10.2.130.229    201  19   RCPKNJ02CR9S01          158244   13141907    Indoor  UMTS       unlocked
		----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		index  bsrName      serial     bsrId  groupName              ctsEquipName           specInfo                       monitored?     ipsecIpAddr     clstrgrp  fgw            gagr     usid     faLocCode   inout   tech alarm?adminStatus

		Number of results: 3
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_105338-metrofull.csv

		Running status check for NYCMNYM32249 (1 of 3)
		Running status check for NYCMNYM32307 (2 of 3)
		Running status check for NYCMNYM32083 (3 of 3)
								 Data Timestamp: 20141231_105417
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		Monitored        10.5.131.93              unlocked    unlocked    enabled     unlocked     enabled      YES  201  19   RCPKNJ02CR9S01        NYCMNYM32249
		Monitored        10.2.130.124             unlocked    unlocked    enabled     unlocked     enabled      no   201  19   RCPKNJ02CR9S01        NYCMNYM32307
		Monitored        10.2.130.229             unlocked    unlocked    enabled     unlocked     enabled      YES  201  19   RCPKNJ02CR9S01        NYCMNYM32083
		----------------------------------------------------------------------------------------------------------------------------------------------------------
		monitoredStatus  ipsecIpAddr     gagr     adminStatus bsrAStatus  bsrOStatus  cellAStatus  cellOStatus  UEs? clstrgrp  fgw            alarm? bsrName
		Number of results: 3
																												 WROTE ABOVE RESULTS TO : /home/customer/russ/pm/20141231_105417-status.csv
		Sending email with the following information:

				 Subject:       PowerMenu Query Result
				 Body:          This report was generated by the Operations PowerMenu. Created by rendicott@gmail.com
				 Attach:        20141231_105338-metrofull.csv, 20141231_105417-status.csv
				 Recipient:     rendicott@gmail.com

		matched +++
		Good Bye!
		$



You can run any sequence of commands through the macro that you can run in interactive mode. Once you find a particular series of commands to be useful
you can write down that sequence and then just simply run it as a macro instead of waiting for prompts. 

Another Example:
Here's the commands you would issue to check for stuck alarms and then email the results:

		$ python pm.py -m "u,n,n,y,y,y,rendicott@gmail.com,y,y,+++"  --fgwpw "Pa\$\$word" --apopw "Pas\$w0rd" --apapw "pa\$\$word"


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ADVANCED INFORMATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~	
	
Running the script with the '-h' or '--help' parameter will show you all of the options you have for passing parameters to the script:

		$ python pm.py --help

		 _____                       __  __
		|  __ \                     |  \/  |
		| |__) |____      _____ _ __| \  / | ___ _ __  _   _
		|  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | |
		| |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| |
		|_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_|
			   === ALU WMS Metrocell Power Menu ===
			   |     Creator: rendicott@gmail.com
			   |     Date: 2014-11-20
			   |     Version: 0.4.6
			   ====================================


		Current Directory: /home/customer/russ/pm

		Testing color support...
		Usage: pm.py [--debug] [--printtostdout] [--food] [--logfile] [--version] [--help] [--macro] [--gagr]

		Options:
		  --version             show program's version number and exit
		  -h, --help            show this help message and exit
		  -f FILE, --food=FILE  This CSV file contains data from CTS that the
								Powermenu will integrate with data from WMS and FGWs.
								Format is "Common ID,Technology,Status,Equipment
								Name,Parent Name,Parent ID,USID,FA Location
								Code,Metrocell AP Location"
		  -m MACRO, --macro=MACRO
								Enter a string of commands separated by a comma (e.g.,
								"u,n,n,y,y,y,rendicott@gmail.com,y,y,+++" to run Stuck
								alarm check, email results, then exit)
		  -g, --gagr            Passing this option will enable GRID/GATEWAY support.
								Takes longer to load.
		  -q FGWPW, --fgwpw=FGWPW
								The admin@FGW password. If the password has "$"
								characters they must be prepended by "\". E.G.,
								"pa$$word" would be entered like "pa\$\$word"
		  -w APOPW, --apopw=APOPW
								The localOperator@AP password. If the password has "$"
								characters they must be prepended by "\". E.G.,
								"pa$$word" would be entered like "pa\$\$word"
		  -e APAPW, --apapw=APAPW
								The localAdmin@AP password. If the password has "$"
								characters they must be prepended by "\". E.G.,
								"pa$$word" would be entered like "pa\$\$word"

		  Debug Options:
			-d DEBUG, --debug=DEBUG
								Available levels are CRITICAL (3), ERROR (2), WARNING
								(1), INFO (0), DEBUG (-1)
			-p, --printtostdout
								Print all log messages to stdout
			-l FILE, --logfile=FILE
								Desired filename of log file output. Default is
								"pm.log"
		$


The most useful parameters are those surrounding the debug functionality. For example, to launch the script with full debugging output to file (default 'pm.log' in current directory)

		$ python pm.py -d -1
		
To launch with full debugging with output to file and screen:

		$ python pm.py -d -1 -p
		
To launch with lower verbosity (e.g., 'INFO') logging you can issue a command like:

		$ python pm.py -d 0 -p



----APPENDIX----
Stuff that was comments in code, now tracking here:

		'''
		The bsgOption relies on file input from a script like:
		$ cat ../grabber.py
		import os

		fgwList = [
			{ 'fgwName' : 'CRTNTX35CR9S01', 'fgwIP' : '10.24.40.171' , 'bsgDump' : ''},
			{ 'fgwName' : 'SNTDCAUJCR9S01', 'fgwIP' : '107.96.253.139' , 'bsgDump' : ''},
			{ 'fgwName' : 'SNAPCAHHCR9S01', 'fgwIP' : '10.170.70.75' , 'bsgDump' : ''},
			{ 'fgwName' : 'NWTPMOABCR9S01', 'fgwIP' : '10.174.33.171' , 'bsgDump' : ''},
			{ 'fgwName' : 'NWTPMOABCR9S02', 'fgwIP' : '10.174.33.173' , 'bsgDump' : ''},
			{ 'fgwName' : 'RCPKNJ02CR9S01', 'fgwIP' : '10.191.178.171' , 'bsgDump' : ''},
			{ 'fgwName' : 'ATLNGAACCR9S01', 'fgwIP' : '10.187.167.139' , 'bsgDump' : ''},
			{ 'fgwName' : 'LKMRFLMFCR9S01', 'fgwIP' : '10.187.167.43' , 'bsgDump' : ''}
			]

		logfile = open('logfile.log','w')
		for o in fgwList:
			logfile.write('----------------------------START ' + o['fgwName'] + '----------------------------\n')
			output = os.popen('./w.sh ' + o['fgwIP'])
			output1 = output.readlines()
			for e in output1:
					logfile.write(e)
			logfile.write('----------------------------END ' + o['fgwName'] + '----------------------------\n')
		'''

	'''
	The data structure for a complete alarm dictionary entry would look like this example:
	alarmDB = { 25: {
		'managedObjectClass': '1003', 
		'alarmedComponent': 'FGW SNTDCAUJCR9S01 FGWConfig 1 BSG 1 FGW SNTDCAUJCR9S01 Femto 62078', 
		'eventTime': '20140821113759', 
		'unknownStatus': '0', 
		'probableCause': 'operationalCondition', 
		'eventType': 'equipmentAlarm', 
		'notificationIdentifier': '11890276', 
		'bSRName': 'STTLWAM62078', 
		'additionalText': 'bsrOutOfService\\n Nature:ADAC, Specific Problem:bsrOutOfService, Additional Information from NE:bSRName=STTLWAM62078;Alarm raised in Active.BSRID:62078,, SecurityAlarmDetector:, ServiceUser:, ServiceProvider:', 
		'FemtoGroup': '56', 
		'Femto': '8926', 
		'correlatedNotifications': '', 
		'activeStatus': '1', 
		'additionalKeyString': '11890276', 
		'FemtoCluster': '1', 
		'perceivedSeverity': 'MAJOR', 
		'specificProblems': 'bsrOutOfService', 
		'managedObjectInstance': 'NW UTRAN EM FGWSNTDCAUJCR9S01', 
		'alarmDisplayInfo': '{NW/UTRAN FGW/SNTDCAUJCR9S01 FGWConfig/1 BSG/1 FGW/SNTDCAUJCR9S01 Femto/62078} {SNTDCAUJCR9S01} {}',
		'monitoredStatus': 'Not Monitored'
		}
	}
	'''

	
DATA SOURCES BEHIND THE SCENESE THAT MAKE POWERMENU RUN:

POWERMENU FOOD FILE FROM CTS:
	This was a solution I devised to retrieve data from CTS/AOTS. There's a Business Objects query that pulls data from CTS/AOTS daily and emails it to rendicott@gmail.com. The file is a CSV dump
	of data from CTS/AOTS. This file is then uploaded manually to the WMS in the /home/customer/russ/pm_foodfiles directory. On load, the pm.py script scans this directory (directory
	is configurable in the pmConfig.py file) and finds the file with the latest timestamp. It then uses that file to plug data in from CTS/AOTS to determine things like Monitored vs 'not monitored' etc.
	
	The query script in Business Objects that generates the CTS Powermenu Food is as follows:
	
			SELECT
			  EQUIPMENT_CONTAINER.COMMON_ID,
			  EQUIPMENT_CONTAINER.TECHNOLOGY,
			  DECODE(EQUIPMENT_CONTAINER.STATUS,0,'Not Monitored', 1, 'Monitored', NULL),
			  EQUIPMENT_CONTAINER.EQUIPMENT_NAME,
			  EQUIPMENT_CONTAINER.PARENT_NAME,
			  EQUIPMENT_CONTAINER.PARENT_ID,
			  EQUIPMENT_CONTAINER.USID,
			  EQUIPMENT_CONTAINER.FA_LOCATION_CODE,
			  EQUIPMENT_CONTAINER.Metrocell_AP_Location
			FROM
			  EQUIPMENT_CONTAINER
			WHERE
			  (
			   EQUIPMENT_CONTAINER.EQUIPMENT_TYPE  IN  ( 'Cell Site'  )
			   AND
			   EQUIPMENT_CONTAINER.SUB_TYPE  IN  ( 'METROCELL'  )
			  )

WMS DATA PULL JOBS
	The rest of the data for PowerMenu comes from WICL jobs running on the WMS. They dump three files into the /home/customer/russ/wicldata folder. 
	
	the RAWDATA-alarms.dat file is generated by this script:
		
		###############russ_fmgetalarms.wcl
		#fm getalarms -f dfs:../../../home/customer/russ/wicldumps/alarms.txt
		set outputfile [open dfs:../../../home/customer/russ/wicldumps/RAWDATA-alarms.dat "w"]
		puts $outputfile [FM getAlarms]
		close $outputfile

	the RAWDATA-provisioning.dat file is generated by this script
		
		################russ_getattrinbulk_provisioning.wcl
		getAttributeValueInBulk -n FemtoCluster/FemtoGroup/Femto -a serialNumber bsrId bSRName groupName administrativeState softwareVersion userSpecificInfo -f dfs:../../../home/customer/russ/wicldumps/RAWDATA-provisioning.dat
		
	the RAWDATA-fddcell.dat is generated by this script
	
		################russ_getattrinbulk_fddcell.wcl
		getattributevalueinbulk -n FemtoCluster/FemtoGroup/Femto/FddExtCellIdList -a fddExtCellLink -f dfs:../../../home/customer/russ/wicldumps/RAWDATA-fddcell.dat
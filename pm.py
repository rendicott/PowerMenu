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
This is the main script for running the PowerMenu. This module has the 
__main__ section and pulls in the other PowerMenu modules. Eventually all
of the non-menu related portions will be moved out of here to other modules.
'''

#Standard Library imports
import re
import time
import datetime
import os
import sys
import getopt
import operator
import pickle
import logging
import inspect
import gc
import getpass
import copy

# internal imports
from pmClasses import eeker # super important that this is first

import pmClasses
import pmLoaders
import pmConfig
import pmFunctions
import pmThreads

from pmConfig import sversion
from pmConfig import header_alarm
from pmConfig import header_status
from pmConfig import header_metro
from pmConfig import sep_status
from pmConfig import sep_metro
from pmConfig import sep_alarm,colorlist



#pull some statics from the pmConfig file
fgwList = pmConfig.fgwList
colorlist = pmConfig.colorlist

#global registrationsupdateflag
#global db_registrationupdatescount
registrationsupdateflag = False
db_registrationupdatescount = 0

#print the pretty logo
pmFunctions.printLogoIntro()

#it would be nice to know the current working directory as a global
print ""
try:
    env_pwd = os.getcwd()
    print "Current Directory: " + env_pwd
except Exception as e:
    print "Exception trying to get current working directory: " + str(e)
print ""

def printMagenta(string):
    print '\033[1;35m' + string + '\033[m'	
printMagenta('Testing color support...')

def helpmenu():
    ''' This function contains all of the menu context helptext and handles
    the display of the 'h' command
    '''
    fgwList = pmConfig.fgwList
    preList = pmConfig.preset_list
    def fList():
        returnstring = ""
        for i,k in enumerate(fgwList):
            if k.get('fgwName') != None:
                returnstring += ("|\t " + k.get('selector') + " - " 
                    + k.get('fgwName') + " - " + k.get('fgwDesc') + 
                    " - ClusterID: " + k.get('clusterId')
                    )
                #add a new line if not at end of list
                if i != len(fgwList)-1:
                    returnstring += "\n"
        return(returnstring)
    def al_cList():
        returnstring = ""
        for i,k in enumerate(preList):
            if preList[k].get('columnName') != None:
                currentfgwname = preList[k].get('columnName')
                returnstring += ("|\t " + k + " - " + currentfgwname)
                #add a new line if not at end of list
                if i != len(preList)-1:
                    returnstring += "\n"
        return(returnstring)
    def in_cList():
        returnstring = ""
        for i,k in enumerate(preList):
            if preList[k].get('attribute') != None:
                returnstring += ("|\t " + k + " - " + 
                                preList[k].get('attribute'))
                if i != len(preList)-1:
                    returnstring += "\n"
        return(returnstring)
    #define the main body of the help throwing in a few variables
    helptext = (
"""
===========================HELP MENU===========================================
|                     ALARM DB INTERACTIONS
|
| cmd 9+dd will list alarms for:
""" + fList() + """
|
| example: '9+01' will list all alarms for NWTPMOABCR9S01 in table format
| NOTE: by default results are filtered to not show 'unmonitored' AP's
| To show all alarms including unmonitored enter command 'f<enter>9+dd'
|
| cmd 8+dd+searchterm will search the dd column for searchterm
| default is 10 - additionalText
""" + al_cList() + """
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
|        will search the femto db for 'searchterm' in particular attribute
| List of available attributes to search is:
""" + in_cList() + """
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
"""
    )
    #and finally, display the text
    print(helptext)
    
def display_full_details(dictentry,input):
    full_format = "{0:10}{1:40}{2}"
    print ""
    for i in input[dictentry]:
        print i

#def display_entry(input,index):
def display_entry(index):
    ''' this function takes user input and looks up the inventory 
    '''
    try:
        index_int = int(index)
        full_format = "{0:10}{1:40}{2}"
        print ""
        eeker.dblock_alarmsd.acquire()
        keylist = eeker.db_alarmsd[index_int].keys()
        for i in keylist:
            print full_format.format("",i,eeker.db_alarmsd[index_int][i])
        print "---------------------"
        eeker.dblock_alarmsd.release()
    except KeyError:
        print "index '" + index + "' not found in database"
    except ValueError:
        print("sorry, you must enter the index "
                "as a number, you entered '" + index + "'"
            )
    except Exception as aoie:
        print "Exception: " + str(aoie)

def find_in_key(key,string):
    ''' this function takes a string and a desired column and then searches 
    the Alarm DICTIONARY (ugh) for that string. This needs to be converted
    to use the Alarm List of Objects (loo) instead. 
    '''
    print "you searched for '" + string + "' in column '" + key + "'"
    count = 0
    try:
        regex = re.compile(string,re.IGNORECASE)
        eeker.dblock_alarmsd.acquire()
        for k in eeker.db_alarmsd:
            line = eeker.db_alarmsd[k].get(key)
            if line != None:
                try:
                    match = re.search(regex, line)
                    if match:
                        count+=1
                        keylist = eeker.db_alarmsd[k].keys()
                        full_format = "{0:10}{1:40}{2}"
                        print ""
                        print "\t You searched for: \t " + str(match.group())
                        print ""
                        for i in keylist:
                            print full_format.format("",i,eeker.db_alarmsd[k][i])
                        print "\t---------------"
                except:
                    print("something went wrong with eeker.db_alarmsd["+k+"]["+i+"]"
                            "or something else went wrong: "
                            + str(sys.exc_info()[0])
                            )
                    continue
        eeker.dblock_alarmsd.release()
        print "done. Number of results: " + str(count)
    except TypeError:
        print("Sorry, something went wrong "
        "trying to comple the regex '" + string + "'")
    except:
        print "or something else went wrong: " + str(sys.exc_info()[0])

#def listFemtoAlarms(loo_input,fgw,fgwdesc,timeUpdated_alarms):    
def listFemtoAlarms(fgw,fgwdesc):
    ''' this function takes input from the user (Selected from preset list) 
    and then queries the Alarm db for alarms matching the particular 
    Femto Gateway.
    '''
    #def print_table(eeker,listofobjects,sortedby,resultname,result_list_count,filtered_results_count,timeUpdated_alarms):
    def print_table(listofobjects,sortedby,
                resultname,result_list_count,
                filtered_results_count):
        ''' this function is internal to listFemtoAlarms() 
        takes list of results and then calls coloredList and appends
        custom footer based on whether or not user wanted to see 'Unmonitored'
        AP's or not
        '''
        listofobjects.sort(key=operator.attrgetter(sortedby))
        t_resultList = []
        for row in listofobjects:
            t_resultList.append(row)
        # since pulling timestamp from eeker.db_alarmso, need to acquire lock
        eeker.dblock.acquire()
        timeiwant = eeker.db_alarmso.timeupdated_alarm
        eeker.dblock.release()
        pmFunctions.coloredList(t_resultList,
                                'alarm',timeiwant,'NA',False)
        if eeker.monfilter:
            print ""
            print("Alarm Count: " + str(result_list_count) + "\t\t\t"
            "Results Name: " + resultname)
            print "Dsply Count: " + str(filtered_results_count)
        else:
            print ""
            print("Alarm Count: " + str(result_list_count) + "\t\t\t"
            "Results Name: " + resultname + "\t\t\t")
        print ""
        t_resultList = None
    
    result_list = []
    result_list_filtered = []
    eeker.dblock.acquire()
    for alarm in eeker.db_alarmso:
        if alarm.fgw == fgw:
            #if it's not monitored put it in a different result list
            if (alarm.monitoredStatus != 'Not Monitored' 
                    and alarm.monitoredStatus != 'Unknown'):
                result_list_filtered.append(alarm)
            #regardless, append it to the result_list
            result_list.append(alarm)
    resultname = "Alarms for " + fgw + " - " + fgwdesc
    total_results_count = len(result_list)
    filtered_results_count = len(result_list_filtered)
    eeker.dblock.release()
    if eeker.monfilter: # means user doesn't want to see Unmonitored
        result_list = [] #blank out the unused list
        #now call print_table to handle displaying the 'Monitored' results
        print_table(result_list_filtered,'eventTime',
                    resultname,total_results_count,
                    filtered_results_count)
    else:
        result_list_filtered = [] #blank out the unused list
        #now call print_table to handle displaying ALL results
        print_table(result_list,'eventTime',
                    resultname,total_results_count,
                    filtered_results_count)

#def process_dsv_list(dsvstring,inventory):
def process_dsv_list(dsvstring):
    ''' this function takes a dash separated string and then ('b' command)
    tries to query the Metrocell inventory db for those individual common ID's
    '''
    myfunc = str(giveupthefunc())
    result_list = []
    failed_list = []
    foundflag = False
    querylist = dsvstring.split('-')
    print "Searching for " + str(len(querylist)) + " objects, hang on..."
    logging.info(myfunc + '\t' + 
                "Detected objects in query: " + str(len(querylist)))
    for femto in querylist:
        foundflag = False
        eeker.dblock.acquire()
        for record in eeker.db_femtos:
            if femto == record.bsrName:
                foundflag = True
                result_list.append(record)
        eeker.dblock.release()
        if not foundflag:
            logging.debug(myfunc + '\t' + 
                        "At end of pass, string not found "
                        "to match object.bsrName: '" + femto + "'")
            failed_list.append(femto)
    logging.debug(myfunc + '\t' + "Done Looping. Length of result_list: "
                    + str(len(result_list)))
    print "Could not find the following Metrocell objects:"
    for e in failed_list:
        print e,
    print ""
    print "Successfully found the following Metrocell objects: "
    print ""
    eeker.dblock.acquire()
    pmFunctions.coloredList(result_list,'metro','NA',eeker.db_femtos,False)
    eeker.dblock.release()



#def getStatistics(alarms,inventory):
def getStatistics():
    ''' this function compiles some data about the current PowerMenu session
    and displays some data for the user. This is good for checking to see
    how much data you have to work with
    '''
    #count all alarms for monitored APs
    eeker.dblock.acquire()
    stat_alarmcount = len(eeker.db_alarmsd)
    stat_mon_alarms = 0
    stat_unmon_alarms = 0
    stat_unknown_alarms = 0
    stat_cts_mon = 0
    stat_cts_unmon = 0
    stat_cts_unknown = 0
    for i in eeker.db_alarmsd:
        try:
            if eeker.db_alarmsd[i]['monitoredStatus'] == 'Monitored':
                stat_mon_alarms+=1
            elif eeker.db_alarmsd[i]['monitoredStatus'] == 'Not Monitored':
                stat_unmon_alarms+=1
            else:
                stat_unknown_alarms+=1
        except KeyError:
            pass
    for o in eeker.db_femtos:
        if o.monitoredStatus == 'Monitored':
            stat_cts_mon+=1
        elif o.monitoredStatus == 'Not Monitored':
            stat_cts_unmon+=1
        elif o.monitoredStatus == 'Unknown':
            stat_cts_unknown+=1
    stat_ap_count = len(eeker.db_femtos)
    stat_reg_ap_count = 0
    stat_unreg_ap_count = 0
    for i in eeker.db_femtos:
        if i.ipsecIpAddr == 'NA':
            stat_unreg_ap_count+=1
        else:
            stat_reg_ap_count+=1
            
    total_fgwlist = 0
    for e in pmConfig.fgwList:
        total_fgwlist+=sys.getsizeof(e)
        
    total_db_femtos = 0
    for e in eeker.db_femtos:
        total_db_femtos+=sys.getsizeof(e)
    
    total_db_alarmsd = 0
    for e in eeker.db_alarmsd:
        total_db_alarmsd+=sys.getsizeof(e)
    
    print "\t STATISTICS "
    print "\t ------------------------------------------"
    print "\t Number of ALARMS total: \t\t " + str(stat_alarmcount)
    print "\t Number of ALARMS ON MONITORED APs: \t " + str(stat_mon_alarms)
    print("\t Number of ALARMS ON UNMONITORED APs: \t " + 
            str(stat_unmon_alarms))
    print ""
    print "\t Number of APs: \t\t\t " + str(stat_ap_count)
    print "\t Number of known registered APs: \t " + str(stat_reg_ap_count)
    print("\t Number of known unregistered APs: \t " + 
            str(stat_unreg_ap_count))
    try:
        print "\t Number of UNMONITORED APs: \t\t " + str(stat_cts_unmon)
        print ""
        print "\t Number of MONITORED APs: \t " + str(stat_cts_mon)
        print "\t Number of APs with UNKNOWN status: " + str(stat_cts_unknown)
        print "\t ------------------------------------------"
        print("\t Size of eeker.db_cts: \t\t\t " 
                + str(sys.getsizeof(eeker.db_cts)) + "\t bytes.")
    except:
        print ""
    print "\t Size of eeker.db_alarmsd: \t\t " + str(total_db_alarmsd) + "\t bytes."
    print "\t Size of eeker.db_femtos: \t\t " + str(total_db_femtos) + "\t bytes."
    print "\t Size of fgwList: \t\t\t " + str(total_fgwlist) + "\t bytes."
    print ""
    print("\t WMS/WICL portion of invList last updated: "
            + eeker.db_femtos.timeupdated_wms)
    print("\t FGW/BSG registrations portion of invList last updated: "
            + eeker.db_femtos.timeupdated_bsg)
    print ""
    print "\t Dump results to CSV: " + str(eeker.csvdumpbool)
    print ""
    print "\t List of files created in this session: "
    f_log = pmFunctions.return_file_log()
    f_log.display()
    print ""
    eeker.dblock.release()
    
#def query_femto_db(thedb,searchstring,searchattribute):
def query_femto_db(searchstring,searchattribute):
    myfunc = str(giveupthefunc())
    '''this will search the eekeer.db_femtos database to find a user search string
    it also requires the user to pass in the attribute that they 
    wish to search (e.g., BSRName vs Serial number)'''

    #first, we'll try to compile the regex of the user's search string:
    try:
        re_usersearch1 = re.compile(searchstring,re.IGNORECASE)
        print ""
        print("Searching Femto DB for '" + searchstring 
                + "' in column '" + searchattribute + "'")
        logging.info(myfunc + '\t' + "Searching Femto DB for '"
                    + searchstring + "' in column '" + searchattribute + "'")
    except Exception as e:
        print("There was an error compiling the "
                "regex for the search string. Try again.")
        logging.critical(myfunc + '\t' + "There was an error compiling"
                        "the regex for the search string: " + str(e))
    t_resultList = []
    # now hunt through the db and find what the user wants
    eeker.dblock.acquire()
    for femto in eeker.db_femtos:
        try:
            blobstring = getattr(femto, searchattribute)
        except Exception as e:
            logging.error(myfunc + '\t' + "Error pulling attribute: " 
                        + searchattribute + " from femto: " + 
                        femto.bsrName + " : " + str(e))
        # compile a regex match
        match_usersearch = re.search(re_usersearch1,blobstring)
        if match_usersearch:
            # means we found a match for the user, append to results list
            t_resultList.append(femto)
    # now display the results
    pmFunctions.coloredList(t_resultList,'metro','NA',eeker.db_femtos,False)
    eeker.dblock.release()
    t_resultList = None
    


#def lookup_cluster_group(eeker,runbulkbool,inventory):
def lookup_cluster_group(runbulkbool):
    ''' this function prompts the user for a cluster/group and then displays
    the whole group in a table. If called with the 'runbulkbool' True then 
    it prompts to kick off status check on the whole group.
    '''
    myfunc = str(giveupthefunc())
    try:
        userclustergroup = eeker.macrolist.pop()
    except:
        userclustergroup = raw_input("Enter Cluster and Group"
                            "separated by - (example: 1-100): ")
    try:
        logging.debug(myfunc + '\t' + "chosencolor set to : '" 
                    + eeker.chosencolor + "'")
    except:
        logging.debug(myfunc + '\t' + "Exception pulling chosencolor var")
        eeker.chosencolor = ''
    # now parse the user input
    try:
        tempsplit = userclustergroup.split("-")
        usercluster = tempsplit[0]
        usergroup = tempsplit[1]
        print "You entered:"
        print "Cluster:\t" + usercluster
        print "Group:\t\t" + usergroup
        t_resultList = []
        logging.debug(myfunc + '\t' + 
                "Attempt acquire LOCK eeker.dblock")
        eeker.dblock.acquire()
        logging.debug(myfunc + '\t' + 
                "Success acquire LOCK eeker.dblock")
        for femto in eeker.db_femtos:
            if femto.groupId == usergroup:
                if femto.clusterId == usercluster:
                    # now pull a deepcopy of results so we can remove lock
                    t_resultList.append(copy.deepcopy(femto))
        # now display the results
        pmFunctions.coloredList(t_resultList,
                                'metro','NA',eeker.db_femtos,False)
        eeker.dblock.release()
    except Exception as e:
        try:
            eeker.dblock.release()
        except Exception as dor:
            logging.debug(myfunc + '\t' + 
                "Exception releasing lock, must not have had it...: " + str(dor))
        print "Something went wrong: " + str(e)
        logging.warning(myfunc + '\t' + "Got an exception"
                        "processing group lookup: " + str(e))
    
    # this section is for running bulk status check
    if runbulkbool:
        try:
            try:
                wantrunonwholegroup = eeker.macrolist.pop()
            except:
                wantrunwholegroup_string = ("Are you sure you want to "
                            "run status check on this entire group? (y/n) ")
                wantrunonwholegroup = raw_input(wantrunwholegroup_string)
            if wantrunonwholegroup == 'y':
                # now call the pull_console_dump function on the group
                # send the deepcopied list to pull_ap_console_dump()
                pmLoaders.pull_ap_console_dump(t_resultList)
                pmFunctions.netwalk_export(t_resultList)
        except Exception as e:
            logging.critical(myfunc + '\t' + 
                    "Got an exception trying to do bulk operation: " + str(e))
    else:
        t_resultList = None

#def show_alarms_of_index(eeker,inventory,alarms,loo_alarms,wantedindex):
def show_alarms_of_index(wantedindex):
    '''this function is designed to take the index number of an inventory 
    entry and display alarms associated with that AP.'''
    myfunc = str(giveupthefunc())
    print ""
    print("Displaying all alarms for inventory entry with index: " 
            + str(wantedindex))
    logging.debug(myfunc + '\t' + "Entering function we have:")
    logging.debug(myfunc + '\t' + "wantedindex = " + str(wantedindex))
    foundflag = False
    loo_alarms_mini = []
    loo_inv_mini = []
    eeker.dblock.acquire()
    for i,o in enumerate(eeker.db_femtos):
        if str(o.index) == wantedindex:
            foundflag = True
            logging.debug(myfunc + '\t' + 
                        "Found AP with bsrName = " + o.bsrName)
            logging.debug(myfunc + '\t' 
                        + "Length of AP's alarm list: " + str(len(o.alarms)))
            if o.inalarm:
                for i in o.alarms:
                    display_entry(i)
                    eeker.dblock_alarmso.acquire()
                    for h in eeker.db_alarmso:
                        if str(h.index) == str(i):
                            loo_alarms_mini.append(h)
                eeker.dblock_alarmsd.acquire()
                pmFunctions.coloredList(
                                        loo_alarms_mini,
                                        'alarm',
                                        'NA',
                                        eeker.db_alarmsd,
                                        True)
                eeker.dblock_alarmsd.release()
                eeker.dblock_alarmso.release()
                loo_inv_mini.append(o)
                pmFunctions.coloredList(loo_inv_mini,
                                        'metro','NA',eeker.db_femtos,True)
            else:
                print "\t\tOops, That AP has no alarms."
        if i == len(eeker.db_femtos)-1 and not foundflag:
            print("Couldn't find that index number in inventory: " + 
                    str(wantedindex))
    eeker.dblock.release()

def autoupdate_setfrequency():
    myfunc = str(giveupthefunc())
    print("Select frequency from list.")
    logging.debug(myfunc + " inside autoupdate_setfrequency() ")
    print
    for option in pmConfig.autoupdate_frequency_list:
        # hide the 10 second option for debug purposes
        if option.get('index') != '999':
            print(option.get('index') + ". " + option.get('description'))
    print
    try:
        #first we'll try and get a command from the macro list
        userInput = eeker.macrolist.pop()
    except:
        userInput = raw_input("Select frequency: ")
    for option in pmConfig.autoupdate_frequency_list:
        if userInput == option.get('index'):
            eeker.autoupdate_frequency_lock.acquire()
            eeker.autoupdate_frequency = option.get('time')
            eeker.autoupdate_frequency_lock.release()
    print("Auto Update frequency is now set to " + str(eeker.autoupdate_frequency) + " seconds.")
    print
    logging.debug(myfunc + " autoupdate_frequency set to " + str(eeker.autoupdate_frequency) + " seconds.")
        
def autoupdate_toggle():
    ''' This function switches the auto update functionality on and off
    '''
    eeker.autoupdate = not eeker.autoupdate
    print("auto-update is " + str(eeker.autoupdate))
    if eeker.autoupdate and not eeker.timer_running:
        eeker.timer_killswitch = False
        timer = pmThreads.Thread_timer()
        timer.start()
    elif not eeker.autoupdate:
        eeker.timer_killswitch = True
        
#def mainMenu(loo_alarms,inventory,timeUpdated_alarms):
def mainMenu():
    '''This is the main jumping off point for the entire program. 
    This is the program's "home base" where it will always jump back to 
    after running other various functions'''
    myfunc = str(giveupthefunc()) #set up the function name for logging
    global eeker # why do I have to do this?
    csvdumpbool = False #by default no queries dump to csv
    print ""
    print ""
    #we should make sure we actually have alarms data
    eeker.dblock_alarmsd.acquire()
    if len(eeker.db_alarmsd) == 0:	
        print("Oops, no data in database. Something went wrong. "
            "Did you want server data or local file?")
        logging.info(myfunc + "\t\tOops, no data in database."
            " Something went wrong. Did you want server data or local file?")
        sys.exit()    
    # go through a few variables and check to make sure we're getting them
    logging.debug(myfunc + '\t' + "Entered mainMenu with data...")
    try:
        logging.info(myfunc + '\t' + "alarmsd size: '%s'" % str(len(eeker.db_alarmsd)))
    except Exception as e:
        logging.critical(myfunc + 
                    '\t' + "Got an exception trying to load alarmsd: " + str(e))
    eeker.dblock_alarmsd.release()
    eeker.dblock.acquire()
    try:
        logging.info(myfunc + '\t' + 
                    "eeker.db_femtos size: '%s'" % str(len(eeker.db_femtos)))
    except Exception as e:
        logging.critical(myfunc + '\t' + 
                        "Got an exception trying to load eeker.db_femtos: " + str(e))
    eeker.dblock.release()

    while True: #here's where the actual interactive menu starts
        #here we ask the user for input
        try:
            #first we'll try and get a command from the macro list
            userInput = eeker.macrolist.pop()
        except:
            try:
                userInput = raw_input("Enter Command ('h' for help): ")
                if '\r' in userInput:
                    userInput = None
                if '\n' in userInput:
                    userInput = None
            except Exception as arrrg:
                userInput = None
                logging.debug(myfunc + '\t' + 
                    "Exception at main raw_input. " + 
                    "Setting userInput to 'None': " + str(arrrg))
        logging.debug(myfunc + '\t' + 
                    "Captured user input for menu: '%s' " % userInput)
        '''here we define the regular expressions to parse the user input then 
        forward data to functions. In python's regex, the '^' character 
        indicates the beginning of a line, for real regex this could be 
        accomplished with something like '([^\d\w\+]9\+)' '''
        
        cp999 = '(^9\+)(?P<preset>\d{2})'
        cp99 = re.compile(cp999)
        cp9 = re.search(cp99,userInput)
        
        cp888 = (
          '(^8\+)((((?P<column>\d{2}))(\+{1})(?P<search>.*))|(?P<search1>.*))')
        cp88 = re.compile(cp888)
        cp8 = re.search(cp88,userInput)
        
        cp777 = '(?P<prefix7>^7\+)(?P<index>\d*)'
        cp77 = re.compile(cp777)
        cp7 = re.search(cp77,userInput)
        
        cp666 = '(?P<prefix6>^6\+)(?P<cmid>.*)'
        cp66 = re.compile(cp666)
        cp6 = re.search(cp66,userInput)
        
        cp555 = '(?P<prefix5>^5\+)(?P<search>.*)'
        cp55 = re.compile(cp555)
        cp5 = re.search(cp55,userInput)
        
        cp444 = '(?P<prefix4>^4\+)(?P<cmid>.*)'
        cp44 = re.compile(cp444)
        cp4 = re.search(cp44,userInput)
        
        cp333 = (
          '(^3\+)((((?P<column>\d{2}))(\+{1})(?P<search>.*))|(?P<search1>.*))')
        cp33 = re.compile(cp333)
        cp3 = re.search(cp33,userInput)
        
        cp222 = '(?P<prefix7>^2\+)(?P<index>\d*)'
        cp22 = re.compile(cp222)
        cp2 = re.search(cp22,userInput)
        
        cp111 = '(?P<prefix1>^111)'
        cp11 = re.compile(cp111)
        cp1 = re.search(cp11,userInput)
        
        cp1112 = '(?P<prefix1>^112)'
        cp112 = re.compile(cp1112)
        cp12 = re.search(cp112,userInput)
        
        cp1113 = '(?P<prefix1>^113)'
        cp113 = re.compile(cp1113)
        cp13 = re.search(cp113,userInput)
        
        cp1114 = '(?P<prefix1>^114)'
        cp114 = re.compile(cp1114)
        cp14 = re.search(cp114,userInput)

        cpppp = '\+\+\+'
        cppp = re.compile(cpppp)
        cpp = re.search(cppp,userInput)
        
        cphhh = '(^h)'
        cphh = re.compile(cphhh)
        cph = re.search(cphh,userInput)
        
        cpiii = '(^i)'
        cpii = re.compile(cpiii)
        cpi = re.search(cpii,userInput)
        
        cpfff = '(^f)'
        cpff = re.compile(cpfff)
        cpf = re.search(cpff,userInput)
        
        cpmmm = '(^m)'
        cpmm = re.compile(cpmmm)
        cpm = re.search(cpmm,userInput)
        
        cpsss = '(^s)'
        cpss = re.compile(cpsss)
        cps = re.search(cpss,userInput)

        cpccc = '(^c)'
        cpcc = re.compile(cpccc)
        cpc = re.search(cpcc,userInput)
        
        cpbbb = '(^b)'
        cpbb = re.compile(cpbbb)
        cpb = re.search(cpbb,userInput)
        
        cpggg = '(^g)'
        cpgg = re.compile(cpggg)
        cpg = re.search(cpgg,userInput)
        
        cpuuu = '(^u)'
        cpuu = re.compile(cpuuu)
        cpu = re.search(cpuu,userInput)

        cpcsvvv = '(^n)'
        cpcsvv = re.compile(cpcsvvv)
        cpcsv = re.search(cpcsvv,userInput)

        cpeee = '(?P<nume_group>(^e\+)(?P<nume_num>\d*))|(?P<juste>^e)'
        cpee = re.compile(cpeee)
        cpe = re.search(cpee,userInput)			
        
        cpttt = '(^t)'
        cptt = re.compile(cpttt)
        cpt = re.search(cptt,userInput)
        
        cpaaa = '(^a)'
        cpaa = re.compile(cpaaa)
        cpa = re.search(cpaa,userInput)
        
        cpzzz = '(^z)'
        cpzz = re.compile(cpzzz)
        cpz = re.search(cpzz,userInput)
        
        cpqqq = '(^q)'
        cpqq = re.compile(cpqqq)
        cpq = re.search(cpqq,userInput)

        #now test for regex matches and send out to functions based on input
        if cp9:
            logging.info(myfunc + '\t' + "matched format 9+dd for FGW alarms")
            try:
                iwantthisfgw = ''
                iwantthisfgwDesc = ''
                # parse the data from the 9+XX+XXXX input
                for h in fgwList:
                    if cp9.group('preset') == h.get('selector'):
                        iwantthisfgw = h.get('fgwName')
                        iwantthisfgwDesc = h.get('fgwDesc')
                listFemtoAlarms(iwantthisfgw,iwantthisfgwDesc)
            except KeyError:
                print "Preset not found, try again"
        elif cp8:
            logging.info(myfunc + '\t' + 
                "Matched pattern 8+ for Alarm search")
            if cp8.group('column'):
                colchoice = cp8.group('column')
                listsection = 'columnName'
                filter = pmConfig.preset_list[colchoice][listsection]
                searchterm = cp8.group('search')
                try:
                    find_in_key(filter,searchterm)
                except KeyError:
                    print "syntax incorrect"
            else:
                find_in_key('additionalText',cp8.group('search1'))
            
        elif cp7:
            print "matched 7+dddddddddd"
            logging.debug(myfunc + '\t' + "Matched pattern 7+")
            #display_entry(input,index)
            display_entry(cp7.group('index'))
        elif cp6:
            cmid = cp6.group('cmid')
            pmFunctions.reboot_ap(cmid)
        elif cp5:
            '''This section is for misc selections and test patterns'''
            logging.debug(myfunc + '\t' + "Matched pattern 5+")
            if cp5.group('search') == '01':
                print "showing unmonitored aps"
                eeker.dblock.acquire()
                for o in eeker.db_femtos:
                    if o.monitoredStatus == 'Not Monitored':
                        print o.rowformat(eeker.chosencolor)
                eeker.dblock.release()
            elif cp5.group('search') == '02':
                logging.debug(myfunc + '\t' + "Matched pattern 5+02")
                t_resultList = []
                print "showing aps without ipaddr"
                eeker.dblock.acquire()
                for o in eeker.db_femtos:
                    if o.ipsecIpAddr != 'NA':
                        t_resultList.append(o)
                pmFunctions.coloredList(t_resultList,
                                        'metro','NA',eeker.db_femtos,False)
                eeker.dblock.release()
                t_resultList = None
            elif cp5.group('search') == '03':
                logging.debug(myfunc + '\t' + "Matched pattern 5+03")
                print "Showing METROCELL ROWFORMAT_FULL"
                eeker.dblock.acquire()
                pmFunctions.coloredList(eeker.db_femtos,'metrofull',
                                        'NA',eeker.db_femtos,'False')	
                eeker.dblock.release()
            elif cp5.group('search') == '04':
                logging.debug(myfunc + '\t' + "Matched pattern 5+04")
                print "Showing eeker.db_cts printself()"
                eeker.dblock.acquire()
                for o in eeker.db_cts:
                    print o.printself()
                eeker.dblock.release()
            elif cp5.group('search') == 'w':
                eeker.dblock.acquire()
                for o in eeker.alarmso:
                    print o.rowformat(eeker.chosencolor)
                eeker.dblock.release()
            elif cp5.group('search') == 's':
                t_resultList = []
                print "showing aps without ipaddr"
                eeker.dblock.acquire()
                for o in eeker.db_femtos:
                    if o.ipsecIpAddr == 'offline':
                        t_resultList.append(o)
                pmFunctions.coloredList(t_resultList,
                                        'metro','NA',eeker.db_femtos,False,True)
                eeker.dblock.release()
                t_resultList = None
            elif cp5.group('search') == 'v':
                t_resultList = []
                print "showing aps version other than BSR-04.03..."
                eeker.dblock.acquire()
                for o in eeker.db_femtos:
                    if ("BSR-04.03" not in o.swVersion and
                        len(o.swVersion) > 3):
                        t_resultList.append(o)
                pmFunctions.coloredList(t_resultList,
                                        'metro','NA',eeker.db_femtos,False,True)
                eeker.dblock.release()
                t_resultList = None
            else:
                logging.debug(myfunc + 
                            '\t\t' + "Didn't find any other 5+<search>"
                            " patterns, dumping full 5+")
                t_resultList = []
                listcount = 0
                logging.debug("5+: Attempting to acquire LOCK eeker.dblock.acquire()")
                eeker.dblock.acquire()
                logging.debug("5+: Successfully Acquired LOCK eeker.dblock.acquire()")
                for o in eeker.db_femtos:
                    t_resultList.append(o)
                pmFunctions.coloredList(t_resultList,'metro',
                                        'NA',eeker.db_femtos,False)
                eeker.dblock.release()
                logging.debug("5+: Released LOCK eeker.dblock.acquire()")
                t_resultList = None
        elif cp4:
            print "Detected status check request..."
            logging.debug(myfunc + '\t' + "Matched pattern 4+")
            temp_listofbsrobjects = []
            eeker.dblock.acquire()
            for e in eeker.db_femtos:
                if cp4.group('cmid') == e.bsrName:
                    temp_listofbsrobjects.append(e)
            eeker.dblock.release()
            pmLoaders.pull_ap_console_dump(temp_listofbsrobjects)
        elif cp3:
            logging.debug(myfunc + '\t' + "Matched pattern 3+")
            if cp3.group('column'):
                try:
                    attribute = (
                        pmConfig.preset_list[cp3.group('column')]['attribute'])
                    searchterm = cp3.group('search')
                    logging.debug(myfunc + 
                                '\t' + "Within 3+ context, launching "
                                "query_femto_db with searchterm: " + 
                                searchterm + " :: attribute: " + attribute)
                    query_femto_db(searchterm,attribute)
                except KeyError:
                    print "syntax incorrect"
            else:
                query_femto_db(cp3.group('search1'), 'groupName')
        elif cp2:
            print "matched 2+dddddddddd"
            logging.debug(myfunc + '\t' + "Matched pattern 2+")
            wantedindex = cp2.group('index')
            logging.debug(myfunc + '\t' + 
                        "Caught index # of: " + str(wantedindex))
            show_alarms_of_index(wantedindex)
        elif cps:
            logging.debug(myfunc + '\t' + "Matched pattern 's'")
            lookup_cluster_group(False)
        elif cpg:
            logging.debug(myfunc + '\t' + "Matched pattern 'g'")
            lookup_cluster_group(True)
        elif cp1:
            print "matched 111, updating alarms only"
            
            logging.debug(myfunc + '\t' + "Matched pattern '111'")
            if not eeker.updatingalready:
                eeker.updatingalready_lock.acquire()
                eeker.updatingalready = True
                eeker.updatingalready_lock.release()
                t_updatealarms = pmThreads.Thread_UpdateALARM()
                print("Updating alarms...")
                t_updatealarms.start()
                t_updatealarms.join()
            else:
                print("Oops, update thread is still running, please wait...")
            # we don't wait for a join because we want it in background
        elif cp12:
            logging.debug(myfunc + '\t' + "Matched pattern '112'")
            print "matched 112, updating registrations only"
            
            if not eeker.updatingalready:
                eeker.updatingalready_lock.acquire()
                eeker.updatingalready = True
                eeker.updatingalready_lock.release()
                t_updatebsg = pmThreads.Thread_UpdateBSG()
                print("Reloading data from femto registrations...")
                t_updatebsg.start()
                t_updatebsg.join()
            else:
                print("Oops, update thread is still running, please wait...")
        elif cp13:
            logging.debug(myfunc + '\t' + "Matched pattern '113'")
            print "matched 113"
            
            if not eeker.updatingalready:
                eeker.updatingalready_lock.acquire()
                eeker.updatingalready = True
                eeker.updatingalready_lock.release()
                t_updateall = pmThreads.Thread_UpdateALL()
                print("Reloading all data. Please wait, this takes about five minutes...")
                print("")
                t_updateall.start()
                t_updateall.join() #remove this line to multi-thread
            else:
                print("Oops, update thread is still running, please wait...")
        elif cp14:
            logging.debug(myfunc + '\t' + "Matched pattern '114'")
            print "matched 114, updating alarms and registrations only"
            
            if not eeker.updatingalready:
                eeker.updatingalready_lock.acquire()
                eeker.updatingalready = True
                eeker.updatingalready_lock.release()

                t_updatebsg = pmThreads.Thread_UpdateBSG()
                print("Reloading data from femto registrations...")
                t_updatebsg.start()
                t_updatebsg.join()

                t_updatealarms = pmThreads.Thread_UpdateALARM()
                print("Updating alarms...")
                t_updatealarms.start()
                t_updatealarms.join()

            else:
                print("Oops, update thread is still running, please wait...")
        elif cpp:
            print "matched +++"
            print "Good Bye!"
            eeker.timer_killswitch = True
            print("Waiting for threads to exit...")
            sys.exit()
        elif cpc:
            print ""
            for h in colorlist:
                print h.get('index') + ". " + h.get('example')
            print ""
            print "Default is \033[1;35mMagenta like Mimosa\033[m"
            while True:
                try:
                    colorchoice = eeker.macrolist.pop()
                except:
                    colorchoice = raw_input('Choose a color: ')
                for y in colorlist:
                    if y.get('index') == colorchoice:
                        eeker.chosencolor = y.get('code')
                        print "You chose " + y.get('example')
                        break
                break 
        elif cpb:
            logging.debug(myfunc + '\t' + "Matched cpb...")
            try:
                dsvstring = eeker.macrolist.pop()
            except:
                dsvstring = raw_input("Enter list of CommonID's separated by "
                    "'-' (e.g., 'CHCGILM02580-SPFDILM02648-SPFDILM02646'): ")
            logging.debug(myfunc + '\t' + 
                        "Trying to split string on dashes...")
            try:
                blackhole = dsvstring.split('-')
                process_dsv_list(dsvstring)
            except Exception as e:
                logging.critical(myfunc + '\t' + "Exception: " + str(e))
        elif cpa:
            print("Toggling auto-update")
            autoupdate_toggle()
        elif cpz:
            autoupdate_setfrequency()
        elif cpu:
            print "Detected pattern: 'u'"
            pmFunctions.find_stuck_alarms()
        elif cpcsv:
            eeker.csvdumpbool = not eeker.csvdumpbool
            print "Auto-dump query results to CSV: " + str(eeker.csvdumpbool)
        elif cpq:
            print "Launching query builder..."
            pmFunctions.querybuilder()
        elif cpe:
            if cpe.group('nume_group'):
                try:
                    numdesired = int(cpe.group('nume_num'))
                    pmFunctions.email_result(None,None,
                                                    None,numdesired)
                except ValueError:
                    print "Oops, value after 'e+' must be a number"
            else:
                pmFunctions.email_result(None,None,
                                                    None,None)
        elif cpt:
            print "Detected pattern: 't'"
            print "Change value for AP check procedure timeout..."
            print ""
            for h in pmConfig.timeoutlist:
                print("\t" + h.get('index') + ". " 
                        + h.get('timeout') + " seconds.")
            print ""
            while True:
                try:
                    timeoutchoice = eeker.macrolist.pop()
                except:
                    timeoutchoice = raw_input("Choose an AP check timeout "
                                    "value (default is 8 seconds): ")
                for y in pmConfig.timeoutlist:
                    if y.get('index') == timeoutchoice:
                        eeker.femtostatus_timeout = y.get('timeout')
                        print "You chose " + y.get('timeout') + " seconds."
                        print ""
                        break
                print("Exiting submenu timeout is set to: " + 
                        eeker.femtostatus_timeout + " seconds.")
                break 
        elif cph:
            helpmenu()
        elif cpi:
            logging.debug(myfunc + '\t' + "Matched pattern 'i'")
            print "\t ====CURRENT SESSION INFORMATION===="
            getStatistics()
        elif cpf:
            eeker.fullformat = not eeker.fullformat
            print "FullFormat toggle is: " + str(eeker.fullformat)
        elif cpm:
            eeker.monfilter = not eeker.monfilter
            print "Unmonitored filter is: " + str(eeker.monfilter)
        else:
            print "found no menu matches, try again"



def setuplogging(loglevel,printtostdout,logfile):
    #pretty self explanatory. Takes options and sets up logging.
    print "starting up with loglevel",loglevel,logging.getLevelName(loglevel)
    logging.basicConfig(filename=logfile,
                        filemode='w',level=loglevel, 
                        format='%(asctime)s:%(levelname)s:%(message)s')
    if printtostdout:
        soh = logging.StreamHandler(sys.stdout)
        soh.setLevel(loglevel)
        logger = logging.getLogger()
        logger.addHandler(soh)

def giveupthefunc():
    #This function grabs the name of the current function
    # this is used in most of the debugging/info/warning messages
    # so I know where an operation failed
    '''This code block comes from user "KindAll" on StackOverflow
    http://stackoverflow.com/a/4506081'''
    frame = inspect.currentframe(1)
    code  = frame.f_code
    globs = frame.f_globals
    functype = type(lambda: 0)
    funcs = []
    for func in gc.get_referrers(code):
        if type(func) is functype:
            if getattr(func, "func_code", None) is code:
                if getattr(func, "func_globals", None) is globs:
                    funcs.append(func)
                    if len(funcs) > 1:
                        return None
    return funcs[0] if funcs else None

def main():
    '''This is the main method which starts the process of loading 
    eeker.db_femtos data. After all eeker.db_femtos/alarm/options data is loaded we can 
    launch into the actual powermenu'''
    myfunc = str(giveupthefunc()) #this pulls the function name for debugging
    #from pmClasses import eeker
    global eeker 
    #where we start to process options and run the data grabber functions
    try:
        logging.debug(myfunc + '\t' + 
            "eeker.foodfile : '"+eeker.foodfile+"' ")
    except Exception as el:
        logging.debug(myfunc + '\t' + 
            "Exception capturing eeker.foodfile var: " + str(el))
    try:
        eeker.macrolist #first we'll see if we have a macro list
    except:
        logging.debug(myfunc + '\t' + 
            "'eeker.macrolist' undefined, setting to blank")
        eeker.macrolist = []
    '''Now we'll create our first eeker.db_femtos. SuperList is a subclass of list
    I set this up so that we can have a list with additional properties like 
    the timestamp when it was created
    '''

    # kick off the thread that processes CTS food and creates db
    t_cts = pmThreads.Thread_LoadCTS()
    t_cts.start()
    t_cts.join()
    #first, initialize alarms dictionary
    t_alarm = pmThreads.Thread_initALARMSD()
    t_alarm.start()
    t_alarm.join()
    
    # now initialize the db_femto
    t_femto = pmThreads.Thread_initDB()
    t_femto.start()
    t_femto.join()

    #now try loading superlist of alarm objects from disk
    t_alarmso = pmThreads.Thread_initALARMSO()
    t_alarmso.start()
    t_alarmso.join()
    '''Finally we have enough data to run the actual interactive menu'''
    mainMenu()


if __name__ == '__main__':
    '''This main section is mostly for parsing arguments to the 
    script and setting up debugging'''
    from optparse import OptionParser
    '''set up an additional option group just for debugging parameters'''
    from optparse import OptionGroup
    usage = ("%prog [--debug] [--printtostdout] [--food] "
        "[--logfile] [--version] [--help] [--macro] [--gagr]"
        "[--apapw] [--apopw] [--fgwpw] [--apnopw] [--apnapw]")
    #set up the parser object
    parser = OptionParser(usage, version='%prog ' + sversion) 
    #adding option for "foodfile" which is the CTS/AOTS data
    parser.add_option('-f','--food', 
                    type='string',
                    metavar='FILE',
                    help=("This CSV file contains data from CTS that the "
                        "Powermenu will integrate with data from WMS and "
                        "FGWs.\nFormat is "
                        "'Common ID,Technology,Status,Equipment Name,"
                        "Parent Name,Parent ID,USID,FA Location Code,"
                        "Metrocell AP Location'"),default=None)
    #this parameter is for passing a macro sequence into the menu program
    parser.add_option('-m','--macro',
                    type='string',
                    help=('Enter a string of commands separated by a comma '
                        '(e.g., "u,n,n,y,y,y,rendicott@gmail.com,y,y,+++" to run '
                        'Stuck alarm check, email results, then exit)'),
                    default=None)
    #this parameter is for setting grid/gateway support, makes loading slow
    parser.add_option('-g','--gagr', 
                    action='store_true',
                    help=('Passing this option will enable GRID/GATEWAY '
                            'support. Takes longer to load.'),
                    default=None)
    #this parameter is for setting use case support from granite file, makes loading slow
    parser.add_option('-u','--ucgran', 
                    type='string',
                    metavar='FILE',
                    help=('Passing this option will enable USE CASE '
                            'support. Takes longer to load.'),
                    default=None)
    #this is for passing the FemtoGateway password
    parser.add_option('-q','--fgwpw', 
                    type='string',
                    help=('The admin@FGW password. If the password has "$" '
                    'characters they must be prepended by "\\". E.G., '
                    '"pa$$word" would be entered like "pa\$\$word" '),
                    default=None)
    #this is for passing the operator password in for the Metrocell
    parser.add_option('-w','--apopw', 
                    type='string',
                    help=('The old localOperator@AP password. If the password '
                        'has "$" characters they must be prepended by "\\". '
                        'E.G., "pa$$word" would be entered like "pa\$\$word"'),
                    default=None)
    #this is for passing the admin password for the Metrocell
    parser.add_option('-e','--apapw', 
                    type='string',
                    help=('The old localAdmin@AP password. If the password has '
                    '"$" characters they must be prepended by "\\". E.G., '
                    '"pa$$word" would be entered like "pa\$\$word" '),
                    default=None)
    #this is for passing the operator password in for the Metrocell
    parser.add_option('-x','--apnopw', 
                    type='string',
                    help=('The new 14.02 localOperator@AP password. If the password '
                        'has "$" characters they must be prepended by "\\". '
                        'E.G., "pa$$word" would be entered like "pa\$\$word"'),
                    default=None)
    #this is for passing the admin password for the Metrocell
    parser.add_option('-y','--apnapw', 
                    type='string',
                    help=('The new 14.02 localAdmin@AP password. If the password has '
                    '"$" characters they must be prepended by "\\". E.G., '
                    '"pa$$word" would be entered like "pa\$\$word" '),
                    default=None)					
    parser.add_option('-b','--bsgdump',
                    action='store_true',
                    help=('Passing this option will enable dumping of'
                          ' bsg_get_bsr_registrations to disk in the current'
                          ' directory. Files will be in format: '
                          + pmConfig.bsgdump_fname_prefix + 'FGWNAME.dat'),
                    default=None)
    parser_debug = OptionGroup(parser,'Debug Options')
    parser_debug.add_option('-d','--debug',type='string',
            help=('Available levels are CRITICAL (3), ERROR (2), '
                    'WARNING (1), INFO (0), DEBUG (-1)'),
            default='CRITICAL')
    parser_debug.add_option('-p','--printtostdout',action='store_true',
            default=False,help='Print all log messages to stdout')
    parser_debug.add_option('-l','--logfile',type='string',metavar='FILE',
            help=('Desired filename of log file output. Default '
                    'is "'+pmConfig.defaultlogfilename+'"')
            ,default=pmConfig.defaultlogfilename)
    parser_debug.add_option('-o','--offline',action='store_true',
                    help=('Instead of connecting to each FGW and running'
                    ' bsg_get_bsr_registrations the program looks for .dat'
                    ' files in the configred pmConfig.bsgdump_offline_pull_dir'
                    ' directory and tries to load'
                    ' registration data from there. USE AT YOUR OWN RISK!'),
                    default=None)
    #officially adds the debuggin option group
    parser.add_option_group(parser_debug) 
    options,args = parser.parse_args() #here's where the options get parsed
    
    try: #now try and get the debugging options
        loglevel = getattr(logging,options.debug)
    except AttributeError: #set the log level
        loglevel = {3:logging.CRITICAL,
                2:logging.ERROR,
                1:logging.WARNING,
                0:logging.INFO,
                -1:logging.DEBUG,
                }[int(options.debug)]
    
    try:
        open(options.logfile,'w') #try and open the default log file
    except:
        print "Unable to open log file '%s' for writing." % options.logfile
        logging.debug(
            "Unable to open log file '%s' for writing." % options.logfile)
        
    setuplogging(loglevel,options.printtostdout,options.logfile)

    '''by default we'll set foodOption false which means no manual 
    file and scan for instead'''
    foodOption = False 
    #if passing the gagr option in we'll set the gagr flag in the options class
    if options.gagr: 
        eeker.gagroption = True
    try:
        with open(options.ucgran,'rb') as f: 
            eeker.ucgran_data = f.readlines()
        eeker.ucgranoption = True
    except Exception as ex_ucgraninput:
        logging.debug(
            "Exception processing use case Granite input file: " + 
            str(ex_ucgraninput))
    print("option 'USE CASE': " + str(eeker.ucgranoption))
    if options.bsgdump:
        # by defalut it's set FALSE in pmConfig and then pulled in with Cfg
        #  object creation, here we'll reset it if it's passed as parameter
        eeker.bsgdump_bool = True
    if options.offline:
        # by default this is false in the Cfg() class
        eeker.bsg_offline_bool = True
    else:
        eeker.bsg_offiline_bool = False
    logging.debug("offline_bool = " + str(eeker.bsg_offline_bool))
    logging.debug("gagroption = " + str(eeker.gagroption))
    #if the macro option isn't blank we'll set up the macro list
    if options.macro != None: 
        try:
            eeker.macrolist = [] #set up a blank macro list
            #first set a string from the options that were passed in
            macrostring = options.macro 
            #now split it on commas into a list
            eeker.macrolist = macrostring.split(',') 
            logging.debug("Caught macro string: " + macrostring)
            print ""
            print "Detected the following macro order: "
            for o in eeker.macrolist:
                print '\t', o
            #now we'll reverse so 'popping' will take from the top
            eeker.macrolist.reverse() 
            logging.debug("Running on macro list: " + str(eeker.macrolist))
        except Exception as ex:
            print "Exception parsing macro list, ignoring."
            logging.error("Exception parsing macro list: " + str(ex))
            #if there was any problem parsing then we'll just go into manual mode
            eeker.macrolist = [] 
    try:
        open(options.food) #try opening the foodfile
        foodfile = options.food
        logging.info("Successfully opened food file '%s'" % foodfile)
        foodOption = True #if so we'll set the foodOption true
    except Exception as e:
        logging.error(
            "Exception opening PARAMETER PASSED food file: " + 
            str(options.food) + " - " + str(e))
        '''now try scanning the configured foodfile directory to find 
        the latest food file:'''
        from pmConfig import foodFilesDir #this is a variable from pmConfig
        logging.debug(
            "Now trying to find latest foodfile inside " + str(foodFilesDir))
        try:
            #run the 'findfood' function in pmLoaders
            foodfile = pmLoaders.findfood(foodFilesDir) 
            foodOption = True
        except Exception as eeer:
            logging.debug(
                "Exception running pmLoaders.findfood(), setting"
                " foodfile blank: " + str(eeer))
            foodfile = ''
            foodOption = False
    # now set global foodfile
    eeker.foodfile = foodfile
    #now we'll try and process the password parameters
    if options.fgwpw == None: #if these tests fail just set them to blank
        options.fgwpw = ''
    if options.apopw == None:
        options.apopw = ''
    if options.apapw == None:
        options.apapw = ''
    if options.apnapw == None:
        options.apnapw = ''
    if options.apnopw == None:
        options.apnopw = ''
    '''either way, send them out to the 'procpass' function 
    to massage the passwords'''
    pmLoaders.procpass(options.fgwpw,options.apopw,options.apapw,options.apnopw,options.apnapw)
    logging.debug("After processing passwords I have the following")
    logging.debug("\t\t fgwpw: '" + eeker.fgwpw + "'")
    logging.debug("\t\t apopw: '" + eeker.apopw + "'")
    logging.debug("\t\t apapw: '" + eeker.apapw + "'")
    logging.debug("\t\t apapw: '" + eeker.apnopw + "'")
    logging.debug("\t\t apapw: '" + eeker.apnapw + "'")
    if foodOption: 
        '''now that we've set up everything, call main and pass 
        eeker with all options'''
        main() 
    else:
        #otherwise bomb if we have no food file
        print("You must provide a food file.") 
        sys.exit()
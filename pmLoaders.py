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
This PowerMenu module is all about loading and processing data from the various
external systems. It's mostly comprised of code that populates the inventory
and alarm databases and processes data coming back from AP checks.
'''
#standard library
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
import csv
from subprocess import Popen, PIPE
import xml.etree.ElementTree as ET

#internal modules
from pmClasses import eeker # super important that this is first

import pmConfig
import pmClasses
import pmFunctions


#pull static fgw list from pmConfig
fgwList = pmConfig.fgwList

#initiate the primary key
primaryKey = 0

def primaryKeyGenerator():
    global primaryKey
    primaryKey+=1
    return primaryKey	


def giveupthefunc():
    #This function grabs the name of the current function
    # this is used in most of the debugging/info/warning messages
    # so I know where an operation failed
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

def runoscommand(commandstringraw,subool=None):
    funcname = str(giveupthefunc())
    if subool == None:
        subool = False
    logging.info(funcname + '\t' + pmConfig.rob + commandstringraw)
    if subool:
        commandlist = commandstringraw.split(' ')
        command = subprocess.Popen(commandlist,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        outputstr, errors = command.communicate()
        logging.debug(funcname + '\t' +
            "Done running command, now list interpretation...")
        outputlis = [x for x in outputstr.split('\n')]
        return outputlis
    else:
        # make sure we're returning a list
        return os.popen(commandstringraw).readlines()

'''This function allows us to load the data from the WICL getAlarms 
command or from a file in the end it will return a list of dictionaries 
with all of the alarm info. '''
def loadAlarmData(loo_ctsEntry,silent=None):
    if silent == None:
        silent = False
    myfunc = str(giveupthefunc())
    #first we'll set up a timestamp for this load data operation
    global macrolist
    logging.debug(myfunc + '\t' + 
            "Entering function we have loo_ctsEntry of length: " + 
            str(len(loo_ctsEntry)))
    timeUpdated_alarms = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    try:
        wiclData_raw = open(pmConfig.fromfiles_alarms)
        input = wiclData_raw.readlines()
    except Exception as eee:
        if not silent:
            print "Exception opening file: '" + pmConfig.fromfiles_alarms + "'"
            print "Exception is: " + str(eee)
        logging.error(myfunc + '\t' + 
            "Exception opening file '" + pmConfig.fromfiles_alarms + "'")
        logging.error(myfunc + '\t' + "Exception is: " + str(eee))
    #now we have some input to work with
    
    try:
        input
    except NameError:
        if not silent:
            print "No alarm data found from file input or command."
        sys.exit()
    '''
    first we need to read the input data and find the starting blocks
    we know from examining the file that the data always starts 
    with a single open curly bracket
    So we'll search through the file and use a regular expression
    to find the lines with a single open curly bracket and save that 
    location as an index in the "anchors" list
    '''
    anchors = []
    for i,line in enumerate(input):
        regex = '{\s'
        regex1 = re.compile(regex)
        match = re.search(regex1,line)
        if match:
            anchors.append(i)
    #now anchors is a full list of the starting points for each block

    alarmDB = {}
    #since alarmDB is a dictionary, set up a starting index key
    alarmDBindex = 0
    #This first regex grabs most of the major fields
    regexCommon = '({)(?P<field>\w*)(\s\")(?P<data>[^\"]*)'
    regexCommon1 = re.compile(regexCommon)
    #This second regex grabs fields like commonID, operationStatus, etc.
    regexCommonID = '(\:|\s|\,)(?P<field2>\w*)=(?P<data2>\w*)'
    regexCommonID1 = re.compile(regexCommonID)
    '''This third regex will grab clusterID,groupId, and femtoID. Have to 
    break up the regex into three parts so it fits on 79 char lines'''
    rCID_p1 = '({)(alarmedComponent ")(?P<cluster>FemtoCluster)'
    rCID_p2 = '\s(?P<clusterd>\d*)\s(?P<fgroup>FemtoGroup)\s(?P<fgroupd>\d*)'
    rCID_p3 = '\s(?P<femto>Femto)\s(?P<femtod>\d*)'
    regexClusterID = (rCID_p1 + rCID_p2 + rCID_p3)
    regexClusterID1 = re.compile(regexClusterID)
    
    #loop through the list of known anchor points (e.g., "{" in the file)
    for point in anchors:
        #set up a temporary dictionary to hold matches for each line/alarm
        temp_dict = {}
        '''now that we found a starting point, we'll process the next 
        20 lines as a single entity'''
        for j in range(point,point+20):
            #search each line and find the various regex matches
            match_common = re.search(regexCommon1,input[j])
            match_commonID = re.search(regexCommonID1,input[j])
            match_clusterID = re.search(regexClusterID1,input[j])
            if match_common:
                field = match_common.group('field')
                datad = match_common.group('data')
                temp_dict[field] = datad
            if match_commonID:
                field = match_commonID.group('field2')
                datad = match_commonID.group('data2')
                temp_dict[field] = datad
                '''now that we have the commonID we can search through 
                the loo_ctsEntry list'''
                flag = False
                for k in loo_ctsEntry:
                    if k.cmid == datad:
                        temp_dict['monitoredStatus'] = k.status
                        flag = True
                #flag false means didn't find Common ID in loo
                if flag == False:
                    temp_dict['monitoredStatus'] = 'Unknown'
            if match_clusterID:
                #process matches for cluster ID
                cluster_key = match_clusterID.group('cluster')
                cluster_v = match_clusterID.group('clusterd')
                temp_dict[cluster_key] = cluster_v
                #process matches for group ID
                fgroup_key = match_clusterID.group('fgroup')
                fgroup_v = match_clusterID.group('fgroupd')
                temp_dict[fgroup_key] = fgroup_v
                #process matches for femto ID
                femto_key = match_clusterID.group('femto')
                femto_v = match_clusterID.group('femtod')
                temp_dict[femto_key] = femto_v
        #add the results to the database in a single line with keyed values
        alarmDB[alarmDBindex] = temp_dict
        #increase the DB's index counter
        alarmDBindex+=1
    
    '''
    now we need to get a little more advanced. Since the cluster/group/femto 
    info is only in the HDM alarms we'll need to find the WMS alarm for the 
    same commonID and updated the cluster/group/femto fields. This operation 
    costs 0.026s on a DB with 605 entries.
    '''

    #first, lets find the HDM alarms with the data we want:
    for k in alarmDB:
        #first, scan the DB for the FemtoCluster key
        result = alarmDB[k].get('FemtoCluster')
        #If a result is found we need to start cross referencing
        if result != None:
            #now we'll pull the CommonID from this line
            temp_commonID = alarmDB[k].get('bSRName')
            temp_cluster = alarmDB[k].get('FemtoCluster')
            temp_group = alarmDB[k].get('FemtoGroup')
            temp_femto = alarmDB[k].get('Femto')
            if temp_commonID != None:
                #now we need to scan the DB for all instances of that commonID
                for i in alarmDB:
                    temp_commonID_working = alarmDB[i].get('bSRName')
                    #if we find a common ID...
                    if temp_commonID_working != None:
                        #compare it with the one we found that had cluster info
                        if temp_commonID_working == temp_commonID:
                            '''pull the missing data from the first match 
                            and add it to the current working line'''
                            alarmDB[i]['FemtoCluster'] = temp_cluster
                            alarmDB[i]['FemtoGroup'] = temp_group
                            alarmDB[i]['Femto'] = temp_femto

    #For kicks, let's print out the size of the list in characters.
    alarmDB_size = 0
    for e in alarmDB:
        alarmDB_size+=len(alarmDB[e])
    logging.info(myfunc + '\t' + 
        "Size of alarmDB: " + str(alarmDB_size) + " characters.")
    #and finally we have a nice pretty dictionary full of each alarm
    
    if not silent:
        print "Writing alarmDB to file for later use..."
    with open('DATABASE-ALARMS.pkl','wb') as f:
        pickle.dump(alarmDB,f)
    
    logging.info(myfunc + '\t' + "Done pulling alarms. End of function")
    return alarmDB,timeUpdated_alarms
    
def pull_wicl_inventory():
    ''' This function simply handles the opening of the wicl xml file
    and returns the readlines() to the caller. Used primarily by the 
    buildInv_WICL function.
    
    '''
    myfunc = str(giveupthefunc())
    try:
        wiclraw = open(pmConfig.fromfiles_provisioning)
    except Exception as e:
        logging.debug(myfunc + '\t' + 
            "Exception opening provisioning file: '" + 
            pmConfig.fromfiles_provisioning + "'")
        logging.debug(myfunc + '\t' + "Exception is: " + str(e))
        wiclraw = ''
    return wiclraw.readlines()	

def pull_fddcell_xml():
    ''' This function simply handles the opening of the fddcell xml file
    and returns the readlines() to the caller. Used primarily by the 
    buildInv_WICL function.
    
    '''
    myfunc = str(giveupthefunc())
    try:
        fddcellraw = open(pmConfig.fromfiles_fddcell)
    except Exception as e:
        logging.debug(myfunc + '\t' + 
                "Exception opening fddcell file: '" + 
                pmConfig.fromfiles_fddcell + "'")
        logging.debug(myfunc + '\t' + "Exception is: " + str(e))
        fddcellraw = ''
    return fddcellraw.readlines()	



def usecase_loaddata(db_femtos):
    ''' 
    Processes the raw data fed in from the Granite file.
    Creates list of objects and removes duplicates.
    searches through the provided db_femtos and updates usecase
    returns full db_femtos
    '''
    def parse_ucgran():
        ''' This function handles parsing the Granite CSV which contains
        CommonID/BSRName to Use Case mappings.
        '''
        myfunc = str(giveupthefunc())
        logging.debug(myfunc + '\t' +
            "Entering parse_ucgran() we have eeker.ucgran_data of length: " +
            str(len(eeker.ucgran_data)))
        full = []
        for line in eeker.ucgran_data:
            liner = line.replace('"','')
            splitter = liner.split(',')
            # create the object
            tempo = pmClasses.UCEntry(splitter[0],splitter[1])

            full.append(tempo)
        logging.debug(myfunc + '\t' +
            "Before removing duplicates: " + str(len(full)))
        # blank out the uneeded raw list
        eeker.ucgran_data = []
        # now remove duplicates (only possible due to UCEntry class)
        eeker.ucgran_obdata = set(full)
        logging.debug(myfunc + '\t' +
            "After removing duplicates: " + str(len(eeker.ucgran_obdata)))
    def usecase_query(femto):
        ''' Given a particular commonID/bsrName this function
        will query the ucgran_obdata and return the usecase
        '''
        myfunc = str(giveupthefunc())
        usecase = ''
        logging.debug(myfunc + '\t' + "processing " + femto.bsrName)
        try:
            for obj in eeker.ucgran_obdata:
                if obj == femto:
                    usecase = obj.uc
                    break
        except Exception as ex_uccreate:
            logging.debug(myfunc + '\t' +
                "Exception proccessing ucgran_obdata: " + 
                str(ex_uccreate))
        return usecase
    
    if eeker.ucgranoption:
        print("Now parsing Granite input file for USE CASE info...")
        try:
            parse_ucgran()
        except Exception as ex_ucgranparse:
            logging.debug(myfunc + '\t' + 
                "Exception running parse_ucgran(): " + str(ex_ucgranparse))
        count = 0
        for femto in db_femtos:
            femto.usecase = usecase_query(femto)
            count += 1
            if count % 100 == 0:
                print("."),
        print("")

    return db_femtos


def buildInv_WICL(supresswrite,updatebool,inventory,loo_ctsEntry,silent=None):
    '''now we'll create a function that will process the inventory 
    data from a file. This takes an existing inventory database and a boolean
    that indicates whether or not this an update (should always be update
    since buildInv_WICL creates the base inventory). It also takes about
    list of objects for CTS entries and the config bundle (eeker).
    It takes all of this and then pulls the XML file from disk that has the
    WICL information (configured in pmConfig) and updates the existing
    inventory db with more information. 
    
    '''
    buildInvWICL_starttime = time.time() # start time for performance debugging
    if silent == None:
        silent = False
    myfunc = str(giveupthefunc())
    # first run some debug messages and check that we have the parameters
    logging.debug(myfunc + '\t' + "Starting buildInv_WICL function...")
    try:
        logging.debug(myfunc + '\t' + 
            "At beginning of function I have inventory of size: " 
            + str(len(inventory)))
    except Exception as e:
        logging.critical(myfunc + '\t' + 
            "Exception testing the data from inventory argument: " 
            + str(e))
    try:
        logging.debug(myfunc + '\t' + 
            "At beginning of function I have loo_ctsEntry len: " + 
            str(len(loo_ctsEntry)))
    except Exception as ff:
        logging.critical(myfunc + '\t' + 
            "Exception referencing loo_ctsEntry: " + 
            str(ff))
    try:
        logging.debug(myfunc + '\t' + 
            "At beginning of function I have updatebool of: " + 
            str(updatebool))
    except Exception as e:
        logging.critical(myfunc + '\t' + 
            "Exception testing updatebool: " + str(e))
        logging.debug(myfunc + '\t\t' + "Setting updatebool False")
        updatebool = False
    #Debug Counters
    db_updatecount = 0
    db_createcount = 0
    db_xmlfemtocount = 0
    db_nomatchcount = 0 
    
    #let's see if the invList has been created yet:
    if updatebool:
        logging.debug(myfunc + '\t' + 
            "Function was passed updatebool " + 
            str(updatebool) + " therefore updating existing inventory")
    else:
        # this code should never really run as all buildInv_WICL calls are
        # to an existing DB built from buildInv_BSG
        inventory = pmClasses.SuperList()
        logging.debug(myfunc + '\t' + "Function was passed updatebool " + 
            str(updatebool) + " therefore creating new inventory")
    #either way we need to update the WMS timestamp

    inventory.timeupdated_wms = (
            datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    import xml.etree.ElementTree as ET
    
    #Define a function that will just generate femto (Metrocell) objects
    def femto_create(t_femtoId, t_serialNumber, t_bSRName, t_bsrId, 
                    t_groupName, t_softwareVersion, t_userSpecificInfo, 
                    t_gagr, t_clusterId, t_administrativeState, 
                    db_createcount, t_groupId):
        ''' This function creates Metrocell objects from the data parsed
        from the WICL XML. This codes is really only run if there is no 
        existing object in the inventory db to update. This code would be
        used to create Metrocell objects that are provisioned on the WMS
        but are not registered on the FGW from the bsg_get_bsr_registrations
        
        It's passed all of the info needed to build a Metrocell object
        and then creates it and appends it to the existing inventory.
        It also returns a counter so we can track how many femtos were created
        that didn't exist previously.
        
        '''
        femto = pmClasses.Metrocell(index=primaryKeyGenerator(), 
                                    femtoId = t_femtoId, 
                                    serial = t_serialNumber, 
                                    bsrName = t_bSRName, 
                                    bsrId = t_bsrId,
                                    groupName = t_groupName,
                                    swVersion = t_softwareVersion,
                                    specInfo = t_userSpecificInfo,
                                    monitoredStatus = 'Monitored',
                                    ipsecIpAddr = None,
                                    groupId = t_groupId,
                                    fgw = None,
                                    gagr = t_gagr,
                                    clusterId = t_clusterId,
                                    adminStatus = t_administrativeState
                                    )
        db_createcount += 1
        inventory.append(femto)
        return db_createcount

    def parse_fddcell():
        ''' This function handles the parsing of the fddcell XML to support
        the Powermenu 'gagr' option. This code slows down the load time
        significantly as it adds more nested loops. 
        
        '''
        thisfunc = str(giveupthefunc())
        logging.debug(thisfunc + '\t' + 
            "Starting parse_fddcell function to parse fddcell XML")
        if not silent:
            print("Now parsing fddcell XML to determine GRID/GATEWAY. XML File: " + 
                pmConfig.fromfiles_fddcell )
        '''now start parsing the fddcell info, this was moved from the main 
        provisioning data after the mid 2014 WMS upgrade
        
        first let's build a quick list of dictionaries to hold the data 
        we parse from the xml'''
        fddtemptable = []
        fddcellxml = pull_fddcell_xml()
        logging.debug(thisfunc + '\t' + 
            "At end of pull_fddcell_xml we have xml of length: " + 
            str(len(fddcellxml)))
        xmlstartline = 0
        xmlendline = 0
        re_xmlstart_11 = '(\<snapshot\>)'
        re_xmlend_11 = '(\<\/snapshot\>)'
        re_xmlstart_1 = re.compile(re_xmlstart_11)
        re_xmlend_1 = re.compile(re_xmlend_11)
        for i,line in enumerate(fddcellxml):
            match_xmlstart = re.search(re_xmlstart_1,line)
            match_xmlend = re.search(re_xmlend_1,line)
            if match_xmlstart:
                xmlstartline = i
            if match_xmlend:
                xmlendline = i

        xml_list = []
        for i in range(xmlstartline,xmlendline+1):
            xml_list.append(fddcellxml[i])

        xml_string = ''.join(xml_list)

        tree = ET.fromstring(xml_string)
        '''let's build a little counter so we can see some progress every 
        100 lines processed'''
        process_counter = 0
        for cluster in tree._children:
            cid = ''
            #print cluster.tag,cluster.attrib['id'] #CLUSTER ID
            cid = cluster.attrib['id']
            for group in cluster:
                gid = ''
                gid = group.attrib['id']
                #print '\t',group.tag,group.attrib['id']
                for femto in group:
                    fid = ''
                    gagr = ''
                    #print '\t\t',femto.tag,femto.attrib['id']
                    fid = femto.attrib['id']
                    if len(list(femto)) > 0:
                        gagr = 'GATEWAY'
                    else:
                        gagr = 'GRID'
                    fddtemptable.append(
                        {'cluster':cid,'group':gid,'fid':fid,'gagr':gagr})
                    process_counter += 1
                '''now test the process_counter to see if it's divisible 
                by 100, if so, tick a dot'''
                if not silent:
                    if process_counter % 100 == 0:
                        print '.',
        logging.debug(thisfunc + '\t' + 
            "At end of fddcell parse, fddtemptable is length: " + 
            str(len(fddtemptable)))
        if not silent:
            print ''
        return fddtemptable
        #now blank out the temp table
        fddtemptable = []
    
    #running the parse_fddcell to build temp table of gagr
    if eeker.gagroption:
        lod_fdd = parse_fddcell()
    #kick off the command to pull WICL provisioning data
    if not silent:
        print("Now parsing provisioning XML to build inventory. XML file: " + 
            pmConfig.fromfiles_provisioning)
    # now get data from the function that handles the file opening
    rawdata1 = pull_wicl_inventory()
    try:
        rawdata1
        logging.debug(myfunc + '\t' + 
            "Successfully got some sort of data in 'rawdata1'")
    except Exception as e:
        logging.critical(myfunc + '\t' + 
            "Exception pulling WICL data: " + str(e))
    #start parsing the XML
    #first we need to find where the XML starts and stops in the raw data
    logging.debug(myfunc + '\t' + "Taking raw dirty XML and isolating XML...")
    xmlstartline = 0
    xmlendline = 0
    re_xmlstart_11 = '(\<snapshot\>)'
    re_xmlend_11 = '(\<\/snapshot\>)'
    re_xmlstart_1 = re.compile(re_xmlstart_11)
    re_xmlend_1 = re.compile(re_xmlend_11)
    for i,line in enumerate(rawdata1):
        match_xmlstart = re.search(re_xmlstart_1,line)
        match_xmlend = re.search(re_xmlend_1,line)
        if match_xmlstart:
            xmlstartline = i
        if match_xmlend:
            xmlendline = i
    
    xml_list = []
    for i in range(xmlstartline,xmlendline+1):
        xml_list.append(rawdata1[i])
    logging.debug(myfunc + '\t' + 
        "I see " + str(len(xml_list)) + " lines of XML raw data.")
    xml_string = ''.join(xml_list)
    #now we have pure xml
    
    logging.debug(myfunc + '\t' + 
        "Starting to process XML with Elementtree...")
    tree = ET.fromstring(xml_string)
    '''let's build a little counter so we can see some progress 
    every 100 lines processed'''
    process_counter = 0
    for i,cluster in enumerate(tree._children):
        t_clusterId = cluster.attrib['id']
        for group in cluster:
            t_groupId = group.attrib['id']
            for femtor in group:
                femto = []
                t_femtoId = femtor.attrib['id']			
                t_administrativeState = ''
                t_bsrId = ''
                t_bSRName = ''
                t_gagr = ''
                t_groupName = ''
                t_softwareVersion = ''
                t_userSpecificInfo = ''
                t_serialNumber = ''
                #hunt through the lod_fdd to find gagr
                if eeker.gagroption:
                    for line in lod_fdd:
                        l_cl = line.get('cluster')
                        l_gr = line.get('group')
                        l_fi = line.get('fid')
                        if l_cl == t_clusterId and l_gr == t_groupId and l_fi:
                            t_gagr = line.get('gagr')
                            break
                process_counter += 1
                for a in femtor:
                    db_xmlfemtocount+=1
                    for b in a:
                        '''Will show the following in order: 
                            administrativeState, 
                            bSRName, 
                            bsrId, 
                            fddCellIdList, 
                            groupName, 
                            softwareVersion,
                            userSpecificInfo,
                            serialNumber'''
                        if b.tag == 'administrativeState':
                            t_administrativeState = b.text.rstrip('\r\n\t')
                        if b.tag == 'bSRName':
                            t_bSRName = b.text.rstrip('\r\n\t')
                        if b.tag == 'bsrId':
                            t_bsrId = b.text.rstrip('\r\n\t')
                        if b.tag == 'groupName':
                            t_groupName = b.text.rstrip('\r\n\t')
                        if b.tag == 'softwareVersion':
                            t_softwareVersion = b.text.rstrip('\r\n\t')
                        if b.tag == 'userSpecificInfo':
                            try:
                                t_userSpecificInfo = ('"' + 
                                    b.text.rstrip('\r\n\t') + '"')
                            except AttributeError:
                                t_userSpecificInfo = 'NA'
                        if b.tag == 'serialNumber':
                            t_serialNumber = b.text.rstrip('\r\n\t')
                if updatebool:
                    #update existing femto object in inventory
                    '''start a timer for the inner loop'''
                    #buildInv_WICL_starttime_innerloop_update = time.time()
                    for ig,y in enumerate(inventory):
                        foundflag = False
                        if t_serialNumber==y.serial and t_bsrId==y.bsrId:
                            foundflag = True
                            db_updatecount+=1
                            y.clusterId = cluster.attrib['id']
                            if y.fgw == 'NA':
                                for jy in fgwList:
                                    if y.clusterId == jy.get('clusterId'):
                                        y.fgw = jy.get('fgwName')
                            y.femtoId = t_femtoId
                            y.bsrName = t_bSRName
                            y.groupName = t_groupName
                            y.specInfo = t_userSpecificInfo
                            y.monitoredStatus = 'Monitored'
                            y.gagr = t_gagr
                            y.swVersion = t_softwareVersion
                            y.adminStatus = t_administrativeState
                            y.groupId = t_groupId
                            try:
                                ctsfoundflag = False
                                for u in loo_ctsEntry:
                                    if u.cmid==y.bsrName:
                                        y.monitoredStatus = u.status
                                        y.usid = u.usid
                                        y.faloc = u.faloc
                                        y.inout = u.loc
                                        y.tech = u.tech
                                        y.ctsname = u.ename
                                        ctsfoundflag = True
                                        break
                                if not ctsfoundflag:
                                    y.monitoredStatus = 'Unknown'
                            except:
                                continue
                            break
                        elif ig == len(inventory)-1 and foundflag==False:
                            #No match found so we'll create the missing femto
                            #logging.debug("\t\t\t"+t_bSRName+" NO MATCH")
                            db_nomatchcount += 1
                            db_createcount = femto_create(t_femtoId, 
                                        t_serialNumber,
                                        t_bSRName,
                                        t_bsrId,
                                        t_groupName,
                                        t_softwareVersion,
                                        t_userSpecificInfo,
                                        t_gagr,
                                        t_clusterId,
                                        t_administrativeState,
                                        db_createcount,
                                        t_groupId
                                        )                                        
                        # debug the total time for the inner loop
                        '''
                        buildInv_WICL_endtime_innerloop_update = time.time()
                        buildInv_WICL_totaltime_innerloop_update = (
                            buildInv_WICL_endtime_innerloop_update -
                            buildInv_WICL_starttime_innerloop_update )
                        logging.debug(myfunc + '\t\t\t' + 
                            "buildInv_WICL_totaltime_innerloop_update: " +
                            str(buildInv_WICL_totaltime_innerloop_update))
                        '''
                if not updatebool:
                    #just create all femtos detected in XML as new
                    #create new femto object
                    db_createcount = femto_create(t_femtoId,
                                t_serialNumber,
                                t_bSRName,
                                t_bsrId,
                                t_groupName,
                                t_softwareVersion,
                                t_userSpecificInfo,
                                t_gagr,
                                t_clusterId,
                                t_administrativeState,
                                db_createcount,
                                t_groupId
                                )
                if process_counter % 50 == 0:
                    logging.debug(myfunc + '\t' + 
                        "I'm workin' here!",)
                    if not silent:
                        print '.',
    
    if not silent:
        print ''
    logging.debug(myfunc + '\t' + 
        "Updated Femtos: " + str(db_updatecount))
    logging.debug(myfunc + '\t' + 
        "Created Femtos: " + str(db_createcount) )
    logging.info(myfunc + '\t' + 
        "Femtos detected in parsed XML: " + str(db_xmlfemtocount))
    logging.debug(myfunc + '\t' + 
        "Number of XML Femtos with no matches in bsgRegistration inventory: " + 
        str(db_nomatchcount))
    #blank out the rawdata to free up memory
    rawdata1 = ''
    
    if not supresswrite:
        '''finally, write DB to disk and return the inventory to the 
        process that called it'''
        inventory.writetodisk('DATABASE-INVENTORY.pkl','Inventory')
        
    logging.debug(myfunc + '\t' + 
        "Size of inventory at end of buildInv_WICL: " + str(len(inventory)))
    # now calculate total time required for load
    buildInv_WICL_totaltime = time.time() - buildInvWICL_starttime
    logging.debug(myfunc + '\t' +
        "Total time for buildInv_WICL function: " + 
        str(buildInv_WICL_totaltime))
    return inventory

def buildInv_BSG(
                supresswrite,
                registrationsupdateflag,
                fgwList,
                inventory,
                showupdatedbool=None,
                silent = None):
    ''' This function takes a list of Femto Gateways and their IP addresses
    and then connects to them and runs the bsg_get_bsr_registrations command
    to pull a list of all Metrocell's connected to that FGW. I then parses the
    output and builds a list of Metrocell objects. This is always run before 
    the buildInv_WICL function so it sets up the framework for the
    buildInv_WICL function to make the inventory more robust.
    
    Also it takes an input flag to determine whether or not the function is
    running as an update operation or if it's building inventory from scratch.
    
    It returns a list of Metrocell objects and the config bundle (eeker) in 
    case any config changes were made in the function.
    '''
    buildInvBSG_starttime = time.time() # start time for performance debugging
    funcname = str(giveupthefunc())
    if silent == None:
        silent = False
    #set some debug counters
    try:
        logging.debug(funcname + '\t' + 
            "At beginning of function I have inventory of size: " + 
            str(len(inventory)))
    except Exception as e:
        logging.critical(funcname + '\t' + 
            "Exception testing the data from inventory argument: " + str(e))
    try:
        logging.debug(funcname + '\t' + "supresswrite = " + str(supresswrite))
    except:
        logging.debug(funcname + '\t' + 
            "Failed to receive supresswrite. Setting False")
        supresswrite = False
    if showupdatedbool==None:
        showupdatedbool = False
    #declare here so it's accessible to inner functions
    db_registrationupdatescount = 0
    if not registrationsupdateflag:
        inventory = pmClasses.SuperList()
    #compile the regex's used for registration parsing
    re_separator_111 = (
        '(-----------------------------------------------------------)')
    re_separator_11 = re.compile(re_separator_111)
    
    re_bsrid_111 = '(BSR Id:                   <)(?P<bsrid>\d*)'
    re_bsrid_11 = re.compile(re_bsrid_111)
    
    #break the ip addy regex up into three parts so it fits on 79 char line
    re_ipsecip_111_p1 = '(IPSEC IP Address                   <)(?P<ipaddr>'
    re_ipsecip_111_p2 = '(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.)'
    re_ipsecip_111_p3 = '{3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))'
    re_ipsecip_111 = re_ipsecip_111_p1 + re_ipsecip_111_p2 + re_ipsecip_111_p3
    re_ipsecip_11 = re.compile(re_ipsecip_111)
    
    re_groupid_111 = '(BSR Group ID:                      <)(?P<groupid>\d*)'
    re_groupid_11 = re.compile(re_groupid_111)
    
    re_serial_111 = '(Factory Serial Number:             <)(?P<serial>\d*)'
    re_serial_11 = re.compile(re_serial_111)
    #let's set a list to hold AP's that updated
    onesthatupdated = []

    ''' Due to a bug I found in 0.4.8 where we know the IPSec IP addr's are
    not going to update to "offline" when an AP goes offline. Here we're going
    to go through and store the old ipsec IP and set the curren ip to offline
    until proven otherwise.
    '''
    if registrationsupdateflag:
        # assume all AP's are offline until proven otherwise
        for femto in inventory:
            femto.ipsecIpAddr_old = femto.ipsecIpAddr
            femto.ipsecIpAddr = 'offline'
    def parsebsg_createobjects(input,
                            fgw_holder,
                            registrationsupdateflag,
                            ):
        funcname = str(giveupthefunc())

        anchors = []
        if not silent:
            print "Now parsing output for " + fgw_holder
        for i,line in enumerate(input):
                match = re.search(re_separator_11,line)
                if match:
                    anchors.append(i)
        for point in anchors:
            temp_bsrid = ''
            temp_ipsecip = ''
            temp_groupid = ''
            temp_serial = ''
            
            try:
                for j in range(point,point+24):
                    match_bsrid = re.search(re_bsrid_11,input[j])
                    match_ipsecip = re.search(re_ipsecip_11,input[j])
                    match_groupid = re.search(re_groupid_11,input[j])
                    match_serial = re.search(re_serial_11,input[j])
                    if match_bsrid:
                        temp_bsrid = match_bsrid.group('bsrid')
                    if match_ipsecip:
                        temp_ipsecip = match_ipsecip.group('ipaddr')
                    if match_groupid:
                        temp_groupid = match_groupid.group('groupid')
                    if match_serial:
                        temp_serial = match_serial.group('serial')
            except IndexError:
                '''This is just to make sure the script doesn't die when 
                it finds the end of the stream'''
                if not silent:
                    print ""
            if registrationsupdateflag:
                #meaning we're updating data for existing database
                for femto in inventory:
                    if(femto.serial == temp_serial and 
                            femto.bsrId == temp_bsrid):
                        femto.fgw = fgw_holder
                        femto.groupId=temp_groupid
                        femto.ipsecIpAddr = temp_ipsecip
            else:
                #meaning we're creating a new database
                femto = pmClasses.Metrocell(index=primaryKeyGenerator(), 
                                    femtoId=None, 
                                    serial=temp_serial, 
                                    bsrName=None, 
                                    bsrId=temp_bsrid,
                                    groupName=None,
                                    swVersion=None,
                                    specInfo=None,
                                    monitoredStatus=None,
                                    ipsecIpAddr=temp_ipsecip,
                                    groupId=temp_groupid,
                                    fgw=fgw_holder,
                                    clusterId=None,
                                    gagr=None,
                                    adminStatus=None
                                    )

                inventory.append(femto)
        return inventory
    
    def process_offline_files(currfgwname):
        ''' this function takes the current fgwname as input
        and looks in the configured dir for a .dat file with
        the fgw name in the filename. If it finds it, it returns
        the data from that file as if the data was coming from a real
        fgw.
        '''
        myfunc = str(giveupthefunc())
        logging.debug(myfunc + '\t' + "Inside process_offline_files() ")
        dir_prefix = eeker.bsgdump_offline_pull_dir
        try:
            filelist = os.listdir(dir_prefix)
            #strip out directories from the list
            filelist = filter(
                lambda x: not os.path.isdir(dir_prefix + x), filelist)
            
            # now define the regex that will find the filename with the 
            #  current fgwname
            
            re_fgwname = re.compile('(.*' + currfgwname + '.*)')
            
            # this is a quick and dirty way since it can't handle when
            #  there are multiple files with the match
            for o in filelist:
                match = re.search(re_fgwname,o)
                if match:
                    filename = match.group()
            
            
            fullpath = dir_prefix + filename
        except Exception as er:
            logging.debug(myfunc + '\t' + 
                "Exception trying to find fgw file in " + 
                str(dir_prefix) + " : " + str(er))
            fullpath = ''
        if not silent:
            print "\t\tFGW file detected: " + str(fullpath)
        logging.debug(myfunc + '\t' + 
            "FGW dat Fullpath detected as : " + str(fullpath) )
        try:
            file = open(fullpath)
        except Exception as ex:
            logging.debug(myfunc + '\t' +
                "Exception trying to open fgw file: " + str(ex))
            file = None
        return file.readlines()
        logging.debug(myfunc + '\t' + "Exiting process_offline_files() ")
    
    for e in fgwList:
        logging.debug(funcname + '\t' + 
            "Working on dict entry: " + str(e))
        ''' First we loop through the list of Femto Gateways '''
        try:
            if not silent:
                print "Running check for " + e.get('fgwName')
        except Exception as o:
            logging.debug(funcname + '\t' +
                "Exception pulling 'fgwName' from dict entry?" + str(o))
        ''' Build a command line string based on the FGW IP and the 
        configured Expect script name and input password for FGW'''
        commandstringraw = (pmConfig.fgw_bsgScript + 
            " " + e['fgwIP'] + " " + eeker.fgwpw)
        input = ''
        '''Now we have to handle a bug when SSH keys change, the response 
        back from the server has the word 'nasty' in it so we 
        can search for that'''
        re_nasty_111 = ('NASTY')
        re_nasty_11 = re.compile(re_nasty_111)
        
        # let's go ahead and run the command
        # first let's check to see if we're in offline mode
        if eeker.bsg_offline_bool:
            # if so try and load .dat files from configured directory
            # we know we're looking for a bsg dump for the e['fgwName']
            # fgw so we'll pass that to the offline file processor function
            e['bsgDump'] = process_offline_files(e.get('fgwName'))
            #set the 'bsgDump' key of the FGW to be the filemode of the output
        else:
            # otherwise, if not 'offline' then reach out to fgw and run command
            e['bsgDump'] = runoscommand(commandstringraw)
        
        # examine the output from the OS command and assign the massive output
        #  to the 'bsgDump' key on the fgwList dictionary. This way the output
        #  always stays tied to a particular fgw.
        input = e['bsgDump']
        logging.debug(funcname + '\t' + 
            "Type of data in e['bsgDump'] : " + str(type(input)))
        logging.debug(funcname + '\t' + 
            "searching output for 'nasty' for known_hosts SSH key corruption")
        
        # first try and dump output to disk if configured to do so
        if eeker.bsgdump_bool:
            try:
                filename = (eeker.bsgdump_fname_prefix + 
                            e.get('fgwName') + '.dat')
                with open(filename,'wb') as f:
                    for line in input:
                        f.write(line)
            except Exception as r:
                logging.critical(funcname + '\t' +
                    "Error writing bsgdump to disk: " + str(r))
        for line in input:
            # we'll look at every line of the OS output
            match_nasty = re.search(re_nasty_11,line)
            if match_nasty:
                # if we catch a bad SSH key match...
                if not silent:
                    print("Oops, looks like we have a bad SSH key."
                        "Cleaning up known_hosts...")
                logging.warning(funcname + '\t' + 
                    "Found a match, trying to delete the known_hosts file")
                # try to clean up the keys with the OS 'rm' command
                try:
                    knownhostscommand = 'rm $HOME/.ssh/known_hosts'
                    logging.info(funcname + '\t' + 
                        pmConfig.rob + knownhostscommand)
                    ##################################
                    runoscommand(knownhostscommand)
                    ##################################
                    logging.debug(funcname + '\t' + 
                        "Now trying to run the command again...")
                    if not silent:
                        print "Now trying the command again..."
                    logging.info(funcname + '\t' + pmConfig.rob + command)
                    #####################################
                    e['bsgDump'] = runoscommand(commandstringraw)
                    #########################
                    
                    # reset the 'input' variable to hopefully be good input
                    input = e['bsgDump']
                    
                    break
                except Exception as orrr:
                    logging.critical(funcname + '\t' + 
                        "Exception trying to delete the known_hosts file: " + 
                        str(orrr))
        #pull the human readable name of the current FGW
        fgw_holder = e.get('fgwName')
        logging.debug(funcname + '\t' + 
            "Entering the " + 
            fgw_holder + 
            " section we have db_registrationupdatescount = " + 
            str(db_registrationupdatescount))
        '''finally, we have enough good data massaged to send to the function 
        that does the real parsing'''
        logging.debug(funcname + '\t' + 
            "Before entering parsebsg_createobjects, we have " +
            "'input' of len: " + str(len(input)))
        inventory = parsebsg_createobjects(input,
                                                fgw_holder,
                                                registrationsupdateflag)
        logging.debug(funcname + '\t' + "Leaving the " + 
            fgw_holder + 
            " section we have db_registrationupdatescount = " + 
            str(db_registrationupdatescount))
        logging.debug(funcname + '\t' + "Leaving the " + 
            fgw_holder + 
            " section we have db size = " + 
            str(len(inventory)))
    
    # possibly dump to disk and clean up to save memory
    for e in fgwList:
        e['bsgDump'] = ''

    if registrationsupdateflag:
        for femto in inventory:
            if femto.ipsecIpAddr_old != femto.ipsecIpAddr:
                db_registrationupdatescount += 1
                onesthatupdated.append(femto)
        if not silent:
            print("Number of AP's with new IP's since last load: " + 
                str(db_registrationupdatescount))
            rightnow = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            pmFunctions.coloredList(
                                    onesthatupdated,
                                    'metro',
                                    rightnow,
                                    'NA',
                                    False)

    inventory.timeupdated_bsg = (
                datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    if not supresswrite:
        logging.info(funcname + '\t' + 
            "Attempting to write inventory to disk...")
        inventory.writetodisk('DATABASE-INVENTORY.pkl','Inventory')
    logging.debug(funcname + '\t' + 
        "Size of inventory after processing BSG registrations: " + 
        str(len(inventory)))
    return inventory
    
    # now calculate total time required for load
    buildInv_BSG_totaltime = time.time() - buildInvBSG_starttime
    logging.debug(myfunc + '\t' +
        "Total time for buildInv_BSG function: " + 
        str(buildInv_BSG_totaltime))
    #set the update flag back to false
    registrationsupdateflag = False
    
#def pull_ap_console_dump(listofbsrobjects,inventory,askverbose=None):    
def pull_ap_console_dump(listofbsrobjects,askverbose=None):
    ''' this function takes a list of Metrocell objects and searches an
    inventory (also a list of bsr objects) for those provided objects. Then
    it reaches out and performs status checks through an SSH Expect script.
    
    Also figures out which AP the user wants to query 
    then SSH's to it to pull additional status data.
    
    '''
    myfunc = str(giveupthefunc())
    if askverbose==None:
        askverbose=True
    logging.debug(myfunc + '\t' + "started 'pull_ap_console_dump' function")
    logging.debug(myfunc + '\t' + 
        "Detected eeker.apcheck_verbosebool as: " + 
        str(eeker.apcheck_verbosebool))
    logging.debug(myfunc + '\t' + "Detected askverbose as: " + str(askverbose))
    logging.debug(myfunc + '\t' + 
        "Received listofbsrobjects of length: " + str(len(listofbsrobjects)))
    try:
        logging.debug(myfunc + '\t' + 
            "Entering function we have chosencolor as: '" + 
            eeker.chosencolor + "'")
    except:
        logging.debug(myfunc + '\t' + 
            "Exception receiving chosencolor parameter")
        eeker.chosencolor = ''
    
    #Now takes a list of Metrocell objects instead for bulk operations
    def parse_ap_console_dump(inputraw,Metroobj):
        '''This function takes raw input from SSH>console>menu to an AP 
        and parses it then it updates the passed in Metrocell object with 
        the parsed data'''
        thisfunc = "parse_ap_console_dump(): "
        logging.debug("parse_ap_console_dump: Beginning function...")
        try:
            # first try and read the output from the Popen command
            inputt = inputraw
        except IOError:
            print "IOError reading " + str(inputt)
        #do some bad SSH key detection on the FGW to AP connection
        skipbool = False # "Skip Bool" for flagging bad SSH key
        tobool = False # "Timeout Bool" for flagging timeout
        ''' Bad SSH key output says something like "We detected someone 
        trying to do something NASTY" so "NASTY" is a good string to search 
        for to try and catch this condition'''
        re_nasty_111 = ('NASTY')
        re_nasty_11 = re.compile(re_nasty_111)
        # The EXP-apcheck.exp script is written to spit out the phrase
        #  "Timed Out!" when it times out so we can catch that here
        re_to_111 = ('Timed Out!')
        re_to_11 = re.compile(re_to_111)
        for line in inputt:
            # check to see if we caught any flags
            match_nasty = re.search(re_nasty_11,line)
            match_timeout = re.search(re_to_11,line)
            if match_nasty:
                print("\tOops, looks like we have a bad SSH key. "
                    "Clearing known_hosts and running again...")
                skipbool = True
            if match_timeout:
                print "\t Timed Out when trying to contact AP!"
                tobool = True

        if not skipbool:
            ''' Now we start to process the meat of what's coming back from the AP
            console status check
            '''
            #split ip regex up into three parts so it fits on 79 char line
            re_ipaddr_p1 = '(?P<ipaddr>(?:(?:25[0-5]|2[0-4]'
            re_ipaddr_p2 = '[0-9]|[01]?[0-9][0-9]?)\.){3}(?:25'
            re_ipaddr_p3 = '[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))'
            re_ipaddr = re_ipaddr_p1 + re_ipaddr_p2 + re_ipaddr_p3 

            
            '''required regex separator will never fit on 79 char line so 
            we build it here. When it's done it's just a long string of
            (-----------) that's 111 chars long'''
            sepbuild = []
            for i in range(111):
                sepbuild.append('-')
            re_statussep_111 = '(' + ''.join(sepbuild) + ')'
            re_statussep_11 = re.compile(re_statussep_111)
            
            ''' spot the bsr Admin and Operation status '''
            #split this one into multipart so fit on 79 char line
            re_bsrStatus_111_p1 = '(BSR   - AST : )(?P<bsrAStatus>\w*)'
            re_bsrStatus_111_p2 = '(  OST :  )(?P<bsrOStatus>\w*)'
            re_bsrStatus_111 = re_bsrStatus_111_p1 + re_bsrStatus_111_p2
            re_bsrStatus_11 = re.compile(re_bsrStatus_111)
            
            ''' spot the cell Admin and Operation status '''            
            #split this one into multipart so fit on 79 char line
            re_cellStatus_111_p1 = '(Cell  - AST : )(?P<cellAStatus>\w*)'
            re_cellStatus_111_p2 = '(  OST :    )(?P<cellOStatus>\w*)'
            re_cellStatus_111 = re_cellStatus_111_p1 + re_cellStatus_111_p2
            re_cellStatus_11 = re.compile(re_cellStatus_111)
            
            ''' Try to spot the first non private IP (gateway usually) '''
            re_firstnonprivateip_111 = '(.*firstNonPrivateIP: )' + re_ipaddr
            re_firstnonprivateip_11 = re.compile(re_firstnonprivateip_111)
            
            ''' spot the list of neighbor metrocells '''
            re_neighborsep_111 = '(UMTS FEMTO CELL NUM :)'
            re_neighborsep_11 = re.compile(re_neighborsep_111)
            
            ''' spot the list of connected IMSI's (cell phones) '''
            re_imsi_111 = '(IMSI\: )(?P<imsi>\d*)'
            re_imsi_11 = re.compile(re_imsi_111)

            ''' define the mac address regex '''
            re_mac = re.compile('([0-9A-F]{2}[:]){5}([0-9A-F]{2})',re.IGNORECASE)

            re_rootmarker = re.compile('(root@)')
            re_ifconfig = re.compile('(ifconfig)')
            re_route = re.compile('(route -e)')
            re_dhcps = re.compile('(DHCPACK from )(?P<dhcps>.*)')

            ap_ipaddr = ''
            ap_netmask = ''
            def parse_ifconfig(text):
                ''' Takes the ifconfig section of the AP dump and parses it
                into object properties.
                '''
                logging.debug(thisfunc + '\t' + 
                    "--IFCONFIG SECTION BEING PARSED--")
                for line in text:
                    logging.debug(thisfunc + '\t\t' + line)
                re_ap_ipaddr = re.compile('(addr:)(?P<ipaddr>.*)')
                re_ap_netmask = re.compile('(Mask:)(?P<mask>.*)')
                for index,line in enumerate(text):
                    # if we hit the loopback section, just break out
                    if 'Link encap:Local Loopback' in line:
                        break
                    match_ap_ipaddr = re.search(re_ap_ipaddr,line)
                    if match_ap_ipaddr:
                        # split the line by spaces
                        chunks = text[index].split()
                        logging.debug(thisfunc + '\t' +
                            "\tIFCONFIG CHUNKS = " + str(chunks))
                        for chunk in chunks:
                            chunk_match_ap_ipaddr = re.search(re_ap_ipaddr,chunk)
                            chunk_match_ap_netmask = re.search(re_ap_netmask,chunk)
                            if chunk_match_ap_ipaddr:
                                ap_ipaddr = chunk_match_ap_ipaddr.group('ipaddr')
                            if chunk_match_ap_netmask:
                                ap_netmask = chunk_match_ap_netmask.group('mask')
                logging.debug(thisfunc + '\t' +
                    "DISCOVERED AP IP ADDRESS: " + ap_ipaddr)
                logging.debug(thisfunc + '\t' +
                    "DISCOVERED AP IP NETMASK: " + ap_netmask)
                return(ap_ipaddr,ap_netmask)

            ap_defaultroute = ''
            def parse_route(text):
                ''' Takes the route -e section of the AP dump and parses it
                into object properties.
                '''
                logging.debug(thisfunc + '\t' + 
                    "--ROUTE SECTION BEING PARSED--")
                for line in text:
                    logging.debug(thisfunc + '\t\t' + line)
                for index,line in enumerate(text):
                    if 'default' in line:
                        chunks = text[index].split()
                        logging.debug(thisfunc + '\t' +
                            '\tDEFAULT ROUTE CHUNK: ' + str(chunks))
                        # doit():                 DEFAULT ROUTE CHUNK: ['default', '12.227.39.129', '0.0.0.0', 'UG', '0', '0', '0', 'eth0']
                        try:
                            ap_defaultroute = chunks[1]
                        except Exception as rtre:
                            logging.debug("Exception setting ap_defaultroute: " +
                                str(rtre))
                return(ap_defaultroute)

            ''' Now define the holder variables that we'll fill with matches '''
            metro_det_bsrAStatus = ''
            metro_det_bsrOStatus = ''
            metro_det_cellAStatus = ''
            metro_det_cellOStatus = ''
            metro_det_firstnonprivateip = ''
            metro_det_neighbors = []
            metro_det_imsi = []
            metro_det_mac = ''
            #create a list to hold the LCell up/down lines from the AP's log
            metro_list_updown = [] 
            # search the first 50 lines for the MAC address
            for index,line in enumerate(inputt):
                match_mac = re.search(re_mac,line)
                if match_mac:
                    metro_det_mac = match_mac.group()
                if index > 50:
                    break

            # search for the DHCPACK server
            logging.debug(thisfunc + '\t' + 
                "\tDISCOVERING DHCP SERVERS...")
            ap_dhcps = ''
            l_dhcps = []
            for index,line in enumerate(inputt):
                match_dhcps = re.search(re_dhcps,line)
                if match_dhcps:
                    l_dhcps.append(match_dhcps.group('dhcps').rstrip('\r\n '))
            # now we have a list of all of the DHCP server IP's found in inputt
            for d in l_dhcps:
                logging.debug(thisfunc + '\t' + 
                    "\t\t\tDHCPS: " + d)
            # now we count frequency of a specific IP
            try:
                from itertools import groupby
                counter_dhcps = [(key,len(list(group))) for key, group in groupby(l_dhcps)]
                
                logging.debug(thisfunc + '\t' +
                    "Top DHCP Servers: counter_dhcps: = " + str(counter_dhcps))
                
                for thing in counter_dhcps:
                    ap_dhcps = thing[0]
                    break
                
                logging.debug(thisfunc + '\t' + 
                    "Selected most common DHCPS of '" + str(ap_dhcps) + "'")
                
            except Exception as yrt:
                logging.debug(thisfunc + '\t' + "Exception: " + str(yrt))


            # search through and find the ifconfig section
            logging.debug(thisfunc + '\t' + 
                "Discovering ifconfig chunk in inputt...")
            ifconfig_startline = 0
            ifconfig_stopline = 0

            for index,line in enumerate(inputt):
                match_ifconfig = re.search(re_ifconfig,line)
                if match_ifconfig:
                    # means we found the line where ifconfig starts
                    ifconfig_startline = index
                    for i in range(index+1,index+100):
                        match_rootmarker = re.search(re_rootmarker,inputt[i])
                        if match_rootmarker:
                            # means we found the line where ifconfig stops
                            ifconfig_stopline = i
                            break
                    break
            logging.debug(thisfunc + '\t' +
                "Discovered ifconfig chunk between lines: " +
                str(ifconfig_startline) + " and " + str(ifconfig_stopline))
            # now send the ifconfig section to the parse_ifconfig() func
            ifconfig_textblock = inputt[ifconfig_startline:ifconfig_stopline]
            try:
                (ap_ipaddr,ap_netmask) = parse_ifconfig(ifconfig_textblock)
            except:
                ap_ipaddr = ''
                ap_netmask = ''


            # search through and find the route section
            logging.debug(thisfunc + '\t' + 
                "Discovering route chunk in inputt...")
            route_startline = 0
            route_stopline = 0
            try:
                for index,line in enumerate(inputt):
                    match_route = re.search(re_route,line)
                    if match_route:
                        # means we found the line where route starts
                        route_startline = index
                        for i in range(index+1,index+100):
                            match_rootmarker = re.search(re_rootmarker,inputt[i])
                            if match_rootmarker:
                                # means we found the line where route stops
                                route_stopline = i
                                break
                        break
            except Exception as ex_rout:
                logging.debug(thisfunc + '\t' +
                    "Exception processing route parsing: " + str(ex_rout))
            logging.debug(thisfunc + '\t' +
                "Discovered route chunk between lines: " +
                str(route_startline) + " and " + str(route_stopline))
            # now send the route section to the parse_route() func
            route_textblock = inputt[route_startline:route_stopline]
            try:
                ap_defaultroute = parse_route(route_textblock)
            except:
                ap_defaultroute = ''



            # now go through the rest of it and get the rest
            for u,i in enumerate(inputt):
                '''find lines that talk about cell being up/down and append 
                them to list'''
                if "Cell is now" in i:
                    metro_list_updown.append(i)
                #finds my echo line for local AP time
                if "LOCAL AP TIME IS" in i: 
                    metro_list_updown.append(i)
                match_statussep = re.search(re_statussep_11,i)
                match_bsrStatus = re.search(re_bsrStatus_11,i)
                match_cellStatus = re.search(re_cellStatus_11,i)
                match_firstnonprivateip = re.search(re_firstnonprivateip_11,i)
                match_neighborsep = re.search(re_neighborsep_11,i)
                match_imsi = re.search(re_imsi_11,i)
                if match_bsrStatus:
                    metro_det_bsrAStatus = match_bsrStatus.group('bsrAStatus')
                    metro_det_bsrOStatus = match_bsrStatus.group('bsrOStatus')
                if match_cellStatus:
                    metro_det_cellAStatus = (
                            match_cellStatus.group('cellAStatus'))
                    metro_det_cellOStatus = (
                            match_cellStatus.group('cellOStatus'))
                '''if we find the UE phrase we know the data we want 
                is 2 lines below that'''
                if match_firstnonprivateip:
                    metro_det_firstnonprivateip = (
                        match_firstnonprivateip.group('ipaddr'))
                if match_neighborsep:
                    metro_det_neighbors.append(inputt[u+10])
                if match_imsi:
                    metro_det_imsi.append(match_imsi.group('imsi'))

                    
            #Now we'll clean up the neighbors list:
            re_nbsrid_111 = '(: )(?P<bsrid>\d*)'
            re_nbsrid_11 = re.compile(re_nbsrid_111)
            for t,e in enumerate(metro_det_neighbors):
                match_nbsrid = re.search(re_nbsrid_11,e)
                if match_nbsrid:
                    metro_det_neighbors[t] = (match_nbsrid.group('bsrid'))
            Metroobj.bsrAStatus = metro_det_bsrAStatus
            Metroobj.bsrOStatus = metro_det_bsrOStatus
            Metroobj.cellAStatus = metro_det_cellAStatus
            Metroobj.cellOStatus = metro_det_cellOStatus
            Metroobj.ueStatus = metro_det_imsi
            Metroobj.firstnonprivateip = metro_det_firstnonprivateip
            Metroobj.neighbors = metro_det_neighbors
            Metroobj.mac = metro_det_mac
            Metroobj.fpip = metro_det_firstnonprivateip
            Metroobj.hostname = Metroobj.bsrName
            Metroobj.defaultroute = ap_defaultroute
            Metroobj.ipaddr = ap_ipaddr
            Metroobj.netmask = ap_netmask
            Metroobj.dhcps = ap_dhcps
            metro_list_updown.sort()  #sort the list before assigning to object
            metro_list_updown.reverse()
            Metroobj.updown = metro_list_updown
            # if we detected timeout then we put that in the object properties
            # so it shows up as TIMEOUT in the output results
            if tobool:
                Metroobj.bsrAStatus = 'TIMEOUT'
                Metroobj.bsrOStatus = 'TIMEOUT'
                Metroobj.cellAStatus = 'TIMEOUT'
                Metroobj.cellOStatus = 'TIMEOUT'
        # return the object we've been working on and whether or not we caught
        # a bad SSH key
        logging.debug("parse_ap_console_dump: Ending function...")
        return Metroobj,skipbool
        
    #let's try and collect enough info to build our command
    t_resultlist = []
    listsize = len(listofbsrobjects)
    # now loop through the smaller input list of desired checks
    for index,thefemto in enumerate(listofbsrobjects):
        # first check to see if we have an ipsecIpAddr
        if thefemto.ipsecIpAddr == 'NA':
            # if not, we can't do anything
            print ""
            print "I don't have enough info for that command."
            print "bsrName = " + thefemto.bsrName
            print "fgw = " + thefemto.fgw
            print "ipsecIpAddr = " + thefemto.ipsecIpAddr
            t_resultlist.append(thefemto)
            break
        # if we have an IP, loop through the list of femto gateways
        # to find the IP of the FGW
        for f in fgwList:
            # if the FGW property of the Metrocell object is the same
            #  as the FGW in the fgwList then pull the FGW IP
            if f['fgwName'] == thefemto.fgw:
                fip = f['fgwIP']
                # now we have enough info to build the check status cmd
                # this is what feeds the expect script
                ''' First we need to check to see if it's 14.2 AP for new
                passwords. Otherwise use the old passwords '''
                if '14' in thefemto.swVersion:
                    femtostatus_cmdstringraw = (pmConfig.femtostatus_script_new + 
                        ' ' + fip + ' ' + thefemto.ipsecIpAddr + ' ' + 
                        eeker.fgwpw + ' ' + eeker.apnopw + ' ' + 
                        eeker.apnapw + ' ' + eeker.femtostatus_timeout)
                    logging.debug(myfunc + '\t' +
                        "Detected '14' in swVersion field, using new pwds")
                else:
                    femtostatus_cmdstringraw = (pmConfig.femtostatus_script + 
                        ' ' + fip + ' ' + thefemto.ipsecIpAddr + ' ' + 
                        eeker.fgwpw + ' ' + eeker.apopw + ' ' + 
                        eeker.apapw + ' ' + eeker.femtostatus_timeout)
                    logging.debug(myfunc + '\t' +
                        "Did not detect '14' in swVersion field, using old pwds")
                print("\nRunning status check for " + 
                    thefemto.bsrName + " (" + 
                    str(index+1) + " of " + str(listsize) + ")"),
                logging.info(myfunc + '\t' + 
                    pmConfig.rob + femtostatus_cmdstringraw)
                '''set skpbool flag for skipping the check in the 
                parse_ap_console_dump function. This will allow 
                us to bail out of the check and clear SSH keys
                if we run into bad SSH keys'''
                skipbool = False
                #####################################################
                # now run the actual OS command and return an object
                # and a potential 'skipbool' flag
                #####################################################
                output = runoscommand(femtostatus_cmdstringraw)
                #####################################################
                logging.debug(myfunc + '\t' +
                    "OS command finished, getting ready to " +
                    "launch parse_ap_console_dump")
                (scannedobj,
                    skipbool) = parse_ap_console_dump(
                        output,thefemto)
                # attach the raw data output to the metrocell object
                # this way we can use it later if needed
                thefemto.list_rawdata = copy.deepcopy(output)
                logging.debug(myfunc + '\t' + 
                    "Returned from parse_ap_console_dump")
                ####################################################
                '''skipbool means detected bad known_hosts ssh key 
                so we'll clear it using the EXP-kh.exp script'''
                if skipbool:
                    try:
                        knownhostscommand = 'rm $HOME/.ssh/known_hosts'
                        logging.info(myfunc + '\t' + 
                            pmConfig.rob + knownhostscommand)
                        os.popen(knownhostscommand)
                        knownhosts_cmd = (
                            pmConfig.knownhosts_script + 
                            ' ' + fip + ' ' + eeker.fgwpw)
                        logging.info(myfunc + 
                            '\t' + pmConfig.rob + knownhosts_cmd)
                        os.popen(knownhosts_cmd)
                        ###########################
                        outputstr, errors = command.communicate()
                        outputlis = [x for x in outputstr.split('\n')]
                        (scannedobj,
                            skipbool) = parse_ap_console_dump(
                                outputlis,thefemto)
                        ###########################
                    except Exception as kh:
                        logging.debug(myfunc + '\t' 
                            + "err running FGW known_hosts removal : " 
                            + str(kh))
                '''now just do a quick sanity check and set a 
                'healthy' boolean '''
                if (scannedobj.cellAStatus == 'unlocked' and 
                        scannedobj.cellOStatus == 'enabled' and 
                        scannedobj.bsrAStatus == 'unlocked' and 
                        scannedobj.bsrOStatus == 'enabled' and 
                        scannedobj.adminStatus == 'unlocked'):
                    scannedobj.healthy = True
                else:
                    scannedobj.healthy = False
                try:
                    logging.debug(myfunc + '\t' + 
                        "Scanned AP, " + scannedobj.bsrName + 
                        " is healthy: " + str(scannedobj.healthy))
                except:
                    logging.error(myfunc + '\t' + 
                        "Could not pull 'healthy' attribute for " + 
                        scannedobj.bsrName)
                t_resultlist.append(scannedobj)
                break
    logging.debug(myfunc + '\t' + 
        "Now I have t_resultlist of length: " + str(len(t_resultlist)))
    # check the passed in config bundle (eeker) for verbosity setting
    if eeker.apcheck_verbosebool:
        for bsr in t_resultlist:
            bsr.status()
    else:
        #means verbosity is turned off
        nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        # print results to screen  using coloredList
        pmFunctions.coloredList(t_resultlist,'status',nowtime,'NA',False)
        if askverbose:
            try:
                wantseeverbose = eeker.macrolist.pop()
            except:
                print("(To collect syslog files from the previous check " +
                        "use 'y+'. To generate NetWalk XML for member " +
                        "Metrocells enter 'w'. For syslogs and NetWalk " +
                        "export use 'w+')")
                wantseeverbose = raw_input(
                    "Would you like to see verbose results? (y / y+ / w / w+ / n) ")
            if wantseeverbose == 'y':
                for bsr in t_resultlist:
                    bsr.status()
                    print "\t\t---------------------------"
            if wantseeverbose == 'y+':
                for bsr in t_resultlist:
                    bsr.status()
                    print "\t\t---------------------------"
                print("\t\tWriting syslogs to disk and zipping archive...")
                logging.debug(myfunc + '\t' +
                    "Attempting to run syslog_write_to_disk()...")
                pmFunctions.syslog_write_to_disk(t_resultlist)
            if wantseeverbose == 'w':
                print("\t\tGenerating NetWalk XML...")
                logging.debug(myfunc + '\t' +
                    "Attempting to run pmFunctions.netwalk_export()...")
                pmFunctions.netwalk_export(t_resultlist)
            if wantseeverbose == 'w+':
                print("\t\tGenerating NetWalk XML and writing "
                        "syslogs archive to disk...")
                logging.debug(myfunc + '\t' +
                    "Attempting to run pmFunctions.netwalk_export()...")
                pmFunctions.netwalk_export(t_resultlist)
                logging.debug(myfunc + '\t' +
                    "Attempting to run syslog_write_to_disk()...")
                pmFunctions.syslog_write_to_disk(t_resultlist)
    # now copy t_resultlist objects back to main DB 
    # need to acquire lock first
    logging.debug(myfunc + '\t' +
        "Attempt Acquire LOCK eeker.dblock...")
    eeker.dblock.acquire()
    logging.debug(myfunc + '\t' +
        "Success Acquire LOCK eeker.dblock...")
    for bsr in t_resultlist:
        for i,obj in enumerate(eeker.db_femtos):
            if bsr.bsrName == obj.bsrName:
                # remove the matching entry from main DB 
                eeker.db_femtos.pop(i)
                # append updated entry to main DB
                eeker.db_femtos.append(bsr)
    eeker.dblock.release()
    logging.debug(myfunc + '\t' +
        "Released LOCK eeker.dblock...")
    # blank out temp tables
    for obj in t_resultlist:
        obj.list_radata = []
    t_resultlist = None
    listofbsrobjects = None 

def objectify_alarms(listofalarmdicts,
                    loo_inventory,
                    fgwList,
                    timeupdated,
                    silent = None
                    ):
    
    ''' This function will take a list of alarm dictionarie's and convert 
    it to alarm objects. This will make alarms easier to work with and 
    begin the process of phasing out the dictionaries.
    '''
    myfunc = str(giveupthefunc())
    if silent == None:
        silent = False
    if not silent:
        print "Now converting Alarm dictionary to list of Alarm objects..."
    logging.debug(myfunc + '\t' + "Entered the 'objectify_alarms' function...")
    loo_alarms = pmClasses.SuperList()
    loo_alarms.timeupdated_alarm = timeupdated
    #compile some regexes ahead of the loop
    re_fgw_FGW_111 = '(FGW\ )(?P<fgw>\w*\d*)'
    re_fgw_FGW_11 = re.compile(re_fgw_FGW_111)
    re_fgw_FemtoCluster_111 = '(FemtoCluster\ )(?P<cid>\d*)'
    re_fgw_FemtoCluster_11 = re.compile(re_fgw_FemtoCluster_111)
    #now loop through list of dictionaries and create objects
    process_counter = 0
    '''first, blank out all of the Metrocell.alarms[] list before going 
    into the alarms loop'''
    logging.debug(myfunc + '\t' + "Begin blank out Metrocell.alarms[]...")
    for ap in loo_inventory:
        ap.inalarm = False
        ap.alarms = []
    logging.debug(myfunc + '\t' + "End blank out Metrocell.alarms[]...")
    for alarm in listofalarmdicts:
        t_aobject = pmClasses.Alarm(
                        alarm,
                        listofalarmdicts[alarm].get('alarmedComponent'),
                        listofalarmdicts[alarm].get('eventTime'),
                        listofalarmdicts[alarm].get('notificationIdentifier'),
                        listofalarmdicts[alarm].get('bSRName'),
                        listofalarmdicts[alarm].get('additionalText'),
                        listofalarmdicts[alarm].get('specificProblems'),
                        listofalarmdicts[alarm].get('monitoredStatus')
                        )
        #Now try and interpret the alarmedComponent field to detect FGW/Cluster
        match_fgw = re.search(re_fgw_FGW_11,t_aobject.alarmedComponent)
        match_femtocluster = re.search(
            re_fgw_FemtoCluster_11,t_aobject.alarmedComponent)
        if match_fgw:
            t_aobject.fgw = match_fgw.group('fgw')
            for line in fgwList:
                if line.get('fgwName') == t_aobject.fgw:
                    t_aobject.cid = line.get('clusterId')
        if match_femtocluster:
            t_aobject.cid = match_femtocluster.group('cid')
            for line in fgwList:
                if line.get('clusterId') == t_aobject.cid:
                    t_aobject.fgw = line.get('fgwName')
        #clean up visuals
        if t_aobject.bSRName == 'NA':
            t_aobject.bSRName = ''
        if t_aobject.monitoredStatus == None:
            t_aobject.monitoredStatus = ''
        
        for u in loo_inventory:
            if u.bsrName == t_aobject.bSRName:
                t_aobject.adminStatus = u.adminStatus
                u.inalarm = True
                try:
                    '''
                    logging.debug(myfunc + '\t\t' + 
                        "Appending alarm index " + str(t_aobject.index) + 
                        " to BSR '" + u.bsrName + "'")
                    logging.debug(myfunc + '\t\t\t' + 
                        "Alarm is " + t_aobject.specificProblems)
                    '''
                    u.alarms.append(t_aobject.index)
                except Exception as ao:
                    logging.debug(myfunc + '\t' + 
                        "Exception adding alarm index to Metrocell.alarms[] : " 
                        + str(ao))
                if t_aobject.adminStatus == 'NA': #clean up visuals
                    t_aobject.adminStatus = ''
        loo_alarms.append(t_aobject)
        process_counter += 1
        if not silent:
            if process_counter % 50 == 0:
                print '.',
    if not silent:
        print ''
    try:
        if not silent:
            print "Writing alarmDBo to file for later use..."
        loo_alarms.writetodisk('DATABASE-ALARMSo.pkl','Alarms')
    except Exception as e:
        logging.critical(myfunc + '\t' + 
            "Exception writing DATABASE-ALARMSo.pkl to disk: " + str(e))
    try:
        if not silent:
            print "Writing inventory to file for later use..."
        loo_inventory.writetodisk('DATABASE-INVENTORY.pkl','Inventory')
    except Exception as e:
        logging.critical(myfunc + '\t' + 
            "Exception writing DATABASE-INVENTORY.pkl to disk: " + str(e))
    logging.debug(myfunc + '\t' + "End of 'objectify_alarms' function.")
    return loo_alarms,loo_inventory
        
def eatfood():
    ''' this function takes a eeker.foodfile path and opens it to try and process it as
    a "food" file full of CTS/AOTS data. This will help give the other
    loader functions more info to add to the inventory database as it's 
    building the database from the WMS and FGW build functions.
    
    It returns a list of Cts objects.
    '''
    myfunc = str(giveupthefunc())
    #pmClasses.Cts_Entry(cmid,tech,status,ename,pname,pid,usid,faloc,loc)
    loo_ctsEntry = []
    try:
        with open(eeker.foodfile,'rb') as csvfile:
            csvreader = csv.reader(csvfile)
            for line in csvreader:
                #line = liner.rstrip('\n\r\t')
                #lister = line.split(',')
                cmid = line[0]
                tech = line[1]
                status = line[2]
                ename = line[3]
                pname = line[4]
                pid = line[5]
                usid = line[6]
                faloc = line[7]
                loc = line[8]
                tempCts = pmClasses.Cts_Entry(
                        cmid,
                        tech,
                        status,
                        ename,
                        pname,
                        pid,
                        usid,
                        faloc,
                        loc)
                loo_ctsEntry.append(tempCts)
        logging.info(myfunc + '\t' + 
            "At end of function we have loo_ctsEntry of length: " + 
            str(len(loo_ctsEntry)))
        return loo_ctsEntry
    except Exception as e:
        logging.debug(myfunc + '\t' + 
            "Exception processing food data: " + str(e))
        
def findfood(dir_prefix):
    ''' this function takes a directory as input and searches it for the file
    with the most recent timestamp. It returns the full filepath of the file
    with the most recent timestamp.
    '''
    myfunc = str(giveupthefunc())
    logging.debug(myfunc + '\t' + "Inside findfood() ")
    try:
        #code snippet borrowed courtesy of "schauerlich" on Ubuntu forums
        # http://ubuntuforums.org/showthread.php?t=1526010
        filelist = os.listdir(dir_prefix)
        filelist = filter(
            lambda x: not os.path.isdir(dir_prefix + x), filelist)
        newest = max(filelist, key=lambda x: os.stat(dir_prefix + x).st_mtime)
        fullpath = dir_prefix + newest
    except Exception as er:
        logging.debug(myfunc + '\t' + 
            "Exception trying to find newest file in " + 
            str(dir_prefix) + " : " + str(er))
        fullpath = ''
    print "newest file detected: " + str(fullpath)
    logging.debug(myfunc + '\t' + "Fullpath detected as : " + str(fullpath) )
    return fullpath
    logging.debug(myfunc + '\t' + "Exiting findfood() ")
    
def procpass(p1,p2,p3,p4,p5):
    # p1 = fgwpw
    # p2 = apopw
    # p3 = apapw
    # p4 = apnopw
    # p5 = apnapw
    ''' this function takes three strings to check if they're blank and 
    if they are the function prompts for user input twice per password to 
    verify. Then it takes those strings and tweaks them so it can pass
    them off to Expect scripts with the proper escape chars for \ chars.
    '''
    myfunc = str(giveupthefunc())
    logging.debug(myfunc + "\t\tI'm inside the procpass function")
    
    #Uncomment this to spit out raw passwords in debug 
    '''
    try:
        logging.debug(myfunc + 
            "I was passed the following raw password strings:")
        logging.debug(myfunc + "\t\t p1: '" + p1 + "'")
        logging.debug(myfunc + "\t\t p2: '" + p2 + "'")
        logging.debug(myfunc + "\t\t p3: '" + p3 + "'")
    except Exception as a:
        logging.debug(myfunc + 
            "Exception trying to log raw password strings data to debug file")
    '''
    
    def ask_pass_verify(question):
        print ""
        while True:
            entry1 = ''
            entry2 = ''
            entry1 = getpass.getpass(question)
            entry2 = getpass.getpass("Enter again for verification: ")
            if entry1 == entry2:
                logging.debug(myfunc + "ask_pass_verify: For section: '" + 
                    question + "' there's a password match")
                return entry2
                break
            elif entry1 != entry2:
                print("Passwords do not match! "
                    "Try again (type 'exit' to quit)")
                print ""
            if entry1 == 'exit':
                break
            if entry2 == 'exit':
                break
            
            
    
    def proc_spec_char(passw):		
        '''takes a rawinput password and replaces special characters 
        with escape characters'''
        chunker = []
        for o in passw:
            chunker.append(o)
        newer = []
        for o in chunker:
            if o == '$':
                repl = '\$'
            elif o == '+':
                repl = '\+'
            elif o == '=':
                repl = '\='
            elif o == ';':
                repl = '\;'
            elif o == '&':
                repl = '\&'
            elif o == ')':
                repl = '\)'
            elif o == '(':
                repl = '\('
            else:
                repl = o
            newer.append(repl)
        return ''.join(newer)
    while True:
        if p1 == '':
            p1 = ask_pass_verify(
                "Enter the password for the admin@FGW user: ")
            if(
                    p1 == 'exit' or 
                    p2 == 'exit' or 
                    p3 == 'exit' or 
                    p4 == 'exit' or
                    p5 == 'exit'):
                break
        if p2 == '':
            p2 = ask_pass_verify(
                "Enter the password for the old localOperator@AP user: ")
            if(
                    p1 == 'exit' or 
                    p2 == 'exit' or 
                    p3 == 'exit' or 
                    p4 == 'exit' or
                    p5 == 'exit'):
                break
        if p3 == '':
            p3 = ask_pass_verify(
                "Enter the password for the old localAdmin@AP user: ")
            if(
                    p1 == 'exit' or 
                    p2 == 'exit' or 
                    p3 == 'exit' or 
                    p4 == 'exit' or
                    p5 == 'exit'):
                break
        if p4 == '':
            p4 = ask_pass_verify(
                "Enter the password for the new 14.2 localOperator@AP user: ")
            if(
                    p1 == 'exit' or 
                    p2 == 'exit' or 
                    p3 == 'exit' or 
                    p4 == 'exit' or
                    p5 == 'exit'):
                break
        if p5 == '':
            p5 = ask_pass_verify(
                "Enter the password for the new 14.2 localAdmin@AP user: ")
            if(
                    p1 == 'exit' or 
                    p2 == 'exit' or 
                    p3 == 'exit' or 
                    p4 == 'exit' or
                    p5 == 'exit'):
                break
        else:
            break
    
    eeker.fgwpw = proc_spec_char(p1)
    eeker.apopw = proc_spec_char(p2)
    eeker.apapw = proc_spec_char(p3)
    eeker.apnopw = proc_spec_char(p4)
    eeker.apnapw = proc_spec_char(p5)

'''
def mr_clean():
    # Loops through the db_femtos database and cleans up tabs,newlines,
    # and returns. 
    # 

    myfunc = str(giveupthefunc())
    logging.debug(myfunc + '\t' + "Starting cleanup job...")

    def pull_properties(obj):
        # Takes an object and returns a list of properties
        # as long as they're not "magic" or methods.
        # 
        props = [x for x in dir(obj) if(
                not x.startswith('__') and 
                not callable(getattr(obj,x)))]
        return props

    def validate_props(obj,props):
        for o in props: t = type(getattr(a,o))
            if t is str:
                print "I'm working on a string"
            elif t is list:
                print "I'm working on a list"
            else:
                print "I'm ignoring this one."

    eeker.dblock.acquire()
    for obj in eeker.db_femtos:
        props = pull_properties(obj)
        validate_props(obj,props)
'''

import threading
import time
import logging
import pickle
import copy
import re
import inspect

from pmClasses import eeker # super important that this is first
import pmConfig
import pmLoaders
import pmFunctions
import pmClasses

def varname(p):
    ''' takes variable and returns the name of the variable. Not currently being used
    but figured I'd keep it around since it seems handy. Requires import re, inspect
    Shamefully stolen from 'Constantin' on so
    http://stackoverflow.com/questions/592746/how-can-you-print-a-variable-name-in-python
    '''
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
        if m:
          return m.group(1)

def popLockAndDropIt(rlist,lock,caller):
    ''' Takes a list and a specific lock
    obtains the lock, copies the list to new list
    and returns a deepcopy of the list
    also takes 'caller' which is a description 
    for writing the debug lines
    '''
    myfunc = str(pmLoaders.giveupthefunc())
    logging.debug(myfunc + '\t' +
        "BEGIN popLockAndDropIt() called by " + str(caller))
    logging.debug(myfunc + '\t' +
        "atos = active to standby copy, stoa = standby to active copy")
    # set up some performance timers
    tstart = time.time()
    # regardless, acquire lock
    logging.debug(myfunc + '\t' +
            "Attempt Acquire LOCK with ID: " + str(id(lock)))
    lock.acquire()
    logging.debug(myfunc + '\t' +
            "Acquired LOCK with ID: " + str(id(lock)))
    try:
        # detect what tpe of list we got (e.g.,regular vs SuperList)
        typestring = str(type(rlist)).lower()
        logging.debug(myfunc + '\t' + 
            "Type of list I received = " + typestring)
        if 'superlist' in typestring:
            logging.debug(myfunc + '\t' + 
                "I found 'superlist' in typestring")
            rlist_copy = pmClasses.SuperList()
            # perform the deep copy method for SuperList
            for obj in rlist:
                rlist_copy.append(copy.deepcopy(obj))
            # try and copy timestamps over as well
            try:
                rlist_copy.timeupdated_bsg = rlist.timeupdated_bsg
            except Exception as uu:
                logging.debug(myfunc + '\t' +
                    "Exception copying timeupdated_bsg " + str(caller))
            try:
                rlist_copy.timeupdated_wms = rlist.timeupdated_wms
            except Exception as uu:
                logging.debug(myfunc + '\t' +
                    "Exception copying timeupdated_wms " + str(caller))
            try:
                rlist_copy.timeupdated_alarm = rlist.timeupdated_alarm
            except Exception as uu:
                logging.debug(myfunc + '\t' +
                    "Exception copying timeupdated_alarm " + str(caller))                
        elif 'dict' in typestring:
            logging.debug(myfunc + '\t' + 
                "I found 'dict' in typestring")
            rlist_copy = {}
            # perform the deep copy method for dict
            rlist_copy = dict(rlist)
        else: # means regular list probably
            logging.debug(myfunc + '\t' + 
                "I didn't find 'superlist' or 'dict' in typestring")
            rlist_copy = []
            # perform the deep copy method for list
            rlist_copy = list(rlist)
    except Exception as that:
        logging.debug(myfunc + '\t' +
            "Exception: " + str(that))
        # either way, release lock
        lock.release()
        logging.debug(myfunc + '\t' +
                "Released LOCK with ID: " + str(id(lock)))
    # either way, release lock
    try:
        lock.release()
    except Exception as are:
        logging.debug(myfunc + '\t' +
            "Exception releasing LOCK with ID: " + str(id(lock)) + ": " +str(are))
    logging.debug(myfunc + '\t' +
            "Released LOCK with ID: " + str(id(lock)))
    ttotal = time.time() - tstart
    logging.debug(myfunc + '\t' + 
        "Total copy time: " + str(ttotal))
    logging.debug(myfunc + '\t' + 
        "At end of function I'm returning rlist_copy of type: " + str(type(rlist_copy)))
    logging.debug(myfunc + '\t' + 
        "END popLockAndDropIt() called by " + str(caller))

    return rlist_copy


def initALARMSD(silent = None):
    myfunc = str(pmLoaders.giveupthefunc())
    logging.debug(myfunc + '\t' + "Beginning initALARMSD() function")
    if silent == None:
        silent = False
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = True
    eeker.updatingalready_lock.release()
    
    # copy current alarm dict to standby
    db_alarmsd_standby = {} # create blank temp dict
    timeUpdated_alarms_standby = ''
    # run loadAlarmData and return db to standby db
    (db_alarmsd_standby,
        timeUpdated_alarms_standby) = pmLoaders.loadAlarmData(eeker.db_cts,silent)
    # copy standby to active
    eeker.db_alarmsd = popLockAndDropIt(db_alarmsd_standby,
                                        eeker.dblock_alarmsd,
                                        'initALARMSD__db_alarmsd_stoa')
    eeker.timeUpdated_alarms = timeUpdated_alarms_standby
    db_alarmsd_standby = {} # blank out the temp dict
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = False
    eeker.updatingalready_lock.release()
    logging.debug(myfunc + '\t' + "Exiting initALARMSD() function")
    
def initALARMSO(silent = None):
    myfunc = str(pmLoaders.giveupthefunc())
    logging.debug(myfunc + '\t' + "Beginning initALARMSO() function")
    if silent == None:
        silent = False
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = True
    eeker.updatingalready_lock.release()
    
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_femtos = " + 
            str(type(eeker.db_femtos)))
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_alarmso = " + 
            str(type(eeker.db_alarmso)))
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_alarmsd = " + 
            str(type(eeker.db_alarmsd))) 

    # grab a copy of eeker.db_femtos
    db_femtos_standby = popLockAndDropIt(eeker.db_femtos,
                                        eeker.dblock,
                                        'initALARMSO__db_femtos_atos')
    # grab a copy of eeker.db_alarmso and eeker.db_alarmsd
    db_alarmso_standby = popLockAndDropIt(eeker.db_alarmso,
                                        eeker.dblock_alarmso,
                                        'initALARMSO__db_alarmso_atos')
    db_alarmsd_standby = popLockAndDropIt(eeker.db_alarmsd,
                                        eeker.dblock_alarmsd,
                                        'initALARMSO__db_alarmsd_atos')


    (db_alarmso_standby,
        db_femtos_standby) = pmLoaders.objectify_alarms(db_alarmsd_standby,
                                                        db_femtos_standby,
                                                        pmConfig.fgwList,
                                                        eeker.timeUpdated_alarms,
                                                        silent)

    # now copy standby back to active

    eeker.db_femtos = popLockAndDropIt(db_femtos_standby,
                                        eeker.dblock,
                                        'initALARMSO__db_femtos_stoa')
    eeker.db_alarmso = popLockAndDropIt(db_alarmso_standby,
                                        eeker.dblock_alarmso,
                                        'initALARMSO__db_alarmso_stoa')
    # no need to copy db_alarmsd back since nothing changed.
    '''
    eeker.db_alarmso.timeupdated_alarm = db_alarmso_standby.timeupdated_alarm
    eeker.db_femtos.timeupdated_bsg = db_femtos_standby.timeupdated_bsg
    eeker.db_femtos.timeupdated_wms = db_femtos_standby.timeupdated_wms
    '''
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_femtos = " + 
            str(type(eeker.db_femtos)))
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_alarmso = " + 
            str(type(eeker.db_alarmso)))
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_alarmsd = " + 
            str(type(eeker.db_alarmsd))) 
    db_alarmso_standby = None
    db_femtos_standby = None
    
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = False
    eeker.updatingalready_lock.release()
    logging.debug(myfunc + '\t' + "Exiting initALARMSO() function")

def initFEMTOS(silent = None):
    ''' This function only to be run when blowing away entire eeker.db_femtos
    only called by Thread_UpdateALL and Thread_initDB
    '''
    myfunc = str(pmLoaders.giveupthefunc())
    logging.debug(myfunc + '\t' + "Beginning initFEMTOS() function")
        
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_femtos = " + 
            str(type(eeker.db_femtos)))
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_alarmso = " + 
            str(type(eeker.db_alarmso)))
    logging.debug(myfunc + '\t' + "At beginning of func: Type of eeker.db_alarmsd = " + 
            str(type(eeker.db_alarmsd))) 

    if silent == None:
        silent = False
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = True
    eeker.updatingalready_lock.release()
    #will stop csv writing to disk no matter what (e.g., eeker.csvdumpbool)
    supresswrite = True 
    #set this so we know we're loading all fresh instead of refreshing
    registrationsupdateflag = False
    showupdatedbool = False
    # since registrationsupdateflag is set, buildInv_BSG will blow away existing
    #  and create new anyways, so it doesn't matter what we pass it as long as it's
    #  iterable, so we'll just make a blank list
    db_femtos_standby = pmClasses.SuperList()

    logging.info(myfunc + '\t' + "Kicking off 'buildInv_BSG' function...")

    '''Here we'll run the buildInv_BSG function and pass in the config 
    class object and a few other options including the 
    current blank inventory db, it will return a SuperList()'''
    db_femtos_standby = pmLoaders.buildInv_BSG(supresswrite,
                                    registrationsupdateflag,
                                    pmConfig.fgwList,
                                    db_femtos_standby, # dummy list
                                    showupdatedbool,
                                    silent)
    logging.info(myfunc + '\t' + "Kicking off 'buildInv_WICL' function...")
    updateWICLbool = True
    '''Now that the BSG portion has been run we can run the WICL 
    portion which is now loading from a file on disk location 
    specified in pmConfig'''
    db_femtos_standby = pmLoaders.buildInv_WICL(supresswrite,updateWICLbool,
                                        db_femtos_standby,eeker.db_cts,silent)
    # update use cases if that option is set
    if eeker.ucgranoption:
        logging.info(myfunc + '\t' + "Kicking off 'usecase_loaddata()' function...")
        db_femtos_standby = pmLoaders.usecase_loaddata(db_femtos_standby)

    '''At this point we have an db_femtos_standby inventory DB made up of 
    running the two build functions--BSG then WICL'''
    # acquire locks and copy standby to active
    eeker.db_femtos = popLockAndDropIt(db_femtos_standby,
                                        eeker.dblock,
                                        'initFEMTOS__db_femtos_stoa')
    '''
    # copy over timestamps from standby to active
    eeker.db_femtos.timeupdated_bsg = db_femtos_standby.timeupdated_bsg
    eeker.db_femtos.timeupdated_wms = db_femtos_standby.timeupdated_wms
    '''
    db_alarmso_standby = None
    db_femtos_standby = None
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_femtos = " + 
            str(type(eeker.db_femtos)))
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_alarmso = " + 
            str(type(eeker.db_alarmso)))
    logging.debug(myfunc + '\t' + "At end of func: Type of eeker.db_alarmsd = " + 
            str(type(eeker.db_alarmsd))) 
    eeker.updatingalready_lock.acquire()
    eeker.updatingalready = False
    eeker.updatingalready_lock.release()
    logging.debug(myfunc + '\t' + "Exiting initFEMTOS() function")
        
class Thread_UpdateALL(threading.Thread):
    def run(self):
        # this means we're basically starting from scratch
        logging.debug("Thread_UpdateALL: STARTING")
        initALARMSD(eeker.bool_silentupdates)
        initFEMTOS(eeker.bool_silentupdates)
        initALARMSO(eeker.bool_silentupdates)
        logging.debug("Thread_UpdateALL: At end of thread: Type of eeker.db_femtos = " + 
                str(type(eeker.db_femtos)))
        logging.debug("Thread_UpdateALL: At end of thread: Type of eeker.db_alarmso = " + 
                str(type(eeker.db_alarmso)))
        logging.debug("Thread_UpdateALL: At end of thread: Type of eeker.db_alarmsd = " + 
                str(type(eeker.db_alarmsd)))                        
        logging.debug("Thread_UpdateALL: STOPPING")
        return
        
class Thread_UpdateBSG(threading.Thread):
    def run(self):
        logging.debug("Thread_UpdateBSG: STARTING")
        eeker.updatingalready_lock.acquire()
        eeker.updatingalready = True
        eeker.updatingalready_lock.release()
        registrationsupdateflag = True
        supresswrite = False
        logging.debug("Thread_UpdateBSG: At beginning of thread: Type of eeker.db_femtos = " + 
                str(type(eeker.db_femtos)))
        logging.debug("Thread_UpdateBSG: At beginning of thread: Type of eeker.db_alarmso = " + 
                str(type(eeker.db_alarmso)))
        logging.debug("Thread_UpdateBSG: At beginning of thread: Type of eeker.db_alarmsd = " + 
                str(type(eeker.db_alarmsd)))         
        # obtain a copy of active eeker.db_femtos
        logging.debug("Thread_UpdateBSG:\t" + 
            "before entering popLockAndDropIt, eeker.db_femtos.timeupdated_bsg = " + 
            str(eeker.db_femtos.timeupdated_bsg))
        db_femtos_standby = popLockAndDropIt(eeker.db_femtos,
                                            eeker.dblock,
                                            'Thread_UpdateBSG__db_femtos_atos')

        logging.info("Thread_initDB" + '\t' + "Kicking off 'buildInv_BSG' function...")
        '''Here we'll run the buildInv_BSG function and pass in the config 
        class object and a few other options including the 
        current blank inventory db'''
        showupdatedbool = True
        # kick off buildInv_BSG with showupdatedbool = True, silent = 
        logging.debug("Thread_UpdateBSG:\t" + 
            "before entering buildInv_BSG, db_femtos_standby.timeupdated_bsg = " + 
            str(db_femtos_standby.timeupdated_bsg))
        db_femtos_standby = pmLoaders.buildInv_BSG(supresswrite,
                                        registrationsupdateflag,
                                        pmConfig.fgwList,
                                        db_femtos_standby,
                                        showupdatedbool,
                                        eeker.bool_silentupdates)
        logging.debug("Thread_UpdateBSG:\t" + 
            "after leaving buildInv_BSG, db_femtos_standby.timeupdated_bsg = " + 
            str(db_femtos_standby.timeupdated_bsg))
        # acquire locks and copy standby to active
        eeker.db_femtos = popLockAndDropIt(db_femtos_standby,
                                                    eeker.dblock,
                                                    'Thread_UpdateBSG__db_femtos_stoa')
        logging.debug("Thread_UpdateBSG:\t" + 
            "after leaving popLockAndDropIt, eeker.db_femtos.timeupdated_bsg = " + 
            str(eeker.db_femtos.timeupdated_bsg))
        '''
        eeker.db_femtos.timeupdated_bsg = db_femtos_standby.timeupdated_bsg
        '''
        
        db_femtos_standby = None
        
        logging.debug("Thread_UpdateBSG: At end of thread: Type of eeker.db_femtos = " + 
                str(type(eeker.db_femtos)))
        logging.debug("Thread_UpdateBSG: At end of thread: Type of eeker.db_alarmso = " + 
                str(type(eeker.db_alarmso)))
        logging.debug("Thread_UpdateBSG: At end of thread: Type of eeker.db_alarmsd = " + 
                str(type(eeker.db_alarmsd))) 

        eeker.updatingalready_lock.acquire()
        eeker.updatingalready = False
        eeker.updatingalready_lock.release()
        logging.debug("Thread_UpdateBSG: STOPPING")
        return
        
class Thread_UpdateALARM(threading.Thread):
    def run(self):
        logging.debug("Thread_UpdateALARM: STARTING")
        logging.debug("Reloading data from WMS export: " + pmConfig.fromfiles_alarms)
        try:
            initALARMSD(eeker.bool_silentupdates)
        except Exception as e:
            try:
                eeker.dblock_alarmsd.release()
            except Exception as ox:
                logging.debug("Thread_UpdateALARM: Exception trying to release eeker.dblock_alarmsd: " + str(ox))
            logging.critical("Thread_UpdateALARM: " + '\t' + "Exception: " + str(e))
        #now we also need to updated the loo_alarms
        try:
            initALARMSO(eeker.bool_silentupdates)
        except Exception as e:
            try:
                eeker.dblock.release()
            except Exception as ox:
                logging.debug("Thread_UpdateALARM: Exception trying to release eeker.dblock: " + str(ox))
            logging.critical("Thread_UpdateALARM: " + '\t' + "Exception trying to objectify_alarms: " + str(e))
        logging.debug("Thread_UpdateALARM: STOPPING")
        return

class Thread_initDB(threading.Thread):
    def run(self):
        logging.debug("Thread_initDB: STARTING")
        try:
            logging.info("Thread_initDB" + '\t' + "Trying load data from PKL databases...")
            with open('DATABASE-INVENTORY.pkl', 'rb') as f:
                '''Next we'll try and load inventory db from disk. If successful 
                we'll set it up as the inventory db we'll be working with
                once again, hopefully we can trust the data from disk'''
                eeker.dblock.acquire()
                eeker.db_femtos = pickle.load(f)
                eeker.dblock.release()
                '''next we'll debug some statistics from the loaded file
                this is just some sanity checking for development purposes'''
                logging.info("Thread_initDB" + '\t' + 
                            "Success. Size of eeker.db_femtos = %s" % str(len(eeker.db_femtos)))
                logging.info("Thread_initDB" + '\t' + 
                            "eeker.db_femtos WMS/WICL content last updated: " + 
                            eeker.db_femtos.timeupdated_wms)
                logging.info("Thread_initDB" + '\t' + 
                            "eeker.db_femtos BSG registrations last updated: " + 
                            eeker.db_femtos.timeupdated_bsg)
        except Exception as e:
            '''If we failed to load from disk then we need to load fresh'''
            logging.critical("Thread_initDB" + '\t' + 
                        "Caught exception loading eeker.db_femtos PKL file: " + str(e))
            logging.warning("Thread_initDB" + '\t' + 
                        "Couldn't load from DB PKL files. Loading new...")
            initFEMTOS()
        logging.debug("Thread_initDB: STOPPING")

        
class Thread_LoadCTS(threading.Thread):
    def run(self):
        logging.debug("Thread_LoadCTS: STARTING")
        eeker.db_cts = pmLoaders.eatfood()
        logging.debug("Thread_LoadCTS: STOPPING")
        
class Thread_initALARMSO(threading.Thread):
    def run(self):
        logging.debug("Thread_initALARMSO: STARTING")
        try:
            #this would be the eeker.alarmso as opposed to the alarm dict
            with open('DATABASE-ALARMSo.pkl', 'rb') as f: 
                eeker.db_alarmso = pickle.load(f)
                logging.info("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso PKL: Success. Size of eeker.db_alarmso = " + 
                        str(len(eeker.db_alarmso)))
                logging.debug("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso PKL: Type of eeker.db_alarmso = " + 
                        str(type(eeker.db_alarmso)))
                logging.debug("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso PKL: Timestamp of eeker.db_alarmso = " + 
                        eeker.db_alarmso.timeupdated_alarm)
        except Exception as e:
            logging.critical("Thread_initALARMSO" + '\t' + 
                            "Exception loading eeker.db_alarmso pickle: " + str(e))
            logging.debug("Thread_initALARMSO" + '\t' + 
                            "Starting the 'objectify_alarms' function....")
            try:
                '''failing to load from disk means fresh pull of alarms from file 
                configured in pmConfig. The eeker.db_alarmso is built from the existing 
                alarm dictionary. Need to fix this later and 
                get rid of the dictionary'''
                initALARMSO()
            except Exception as r:
                logging.debg("Thread_initALARMSO" + '\t' +
                    "Exception running initALARMSO(): " + str(r))
        # finally we check to see if we have data
        try:
            logging.debug("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso FRESH: Length of eeker.db_alarmso : " + 
                        str(len(eeker.db_alarmso)))
            logging.debug("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso FRESH: Type of eeker.db_alarmso = " + 
                        str(type(eeker.db_alarmso)))
            logging.debug("Thread_initALARMSO" + '\t' + 
                        "eeker.db_alarmso FRESH: Timestamp of eeker.db_alarmso = " + 
                        eeker.db_alarmso.timeupdated_alarm)
        except Exception as ee:
            logging.debug("Thread_initALARMSO" + '\t' + 
                        "Tried to pull stats on eeker.db_alarmso but got exception: " + 
                        str(ee))
            #worst case scenario we just blank out the alarms 
            eeker.dblock.acquire()
            eeker.db_alarmso = pmClasses.SuperList()
            eeker.dblock.release()
        logging.debug("Thread_initALARMSO: STOPPING")

class Thread_initALARMSD(threading.Thread):
    def run(self):
        logging.debug("Thread_initALARMSD: STARTING")
        try:
            with open('DATABASE-ALARMS.pkl', 'rb') as f:
                '''If we can load from disk we'll set the alarmish db with data 
                from file. Hopefully we can trust the data coming from the file'''
                eeker.dblock_alarmsd.acquire()
                eeker.db_alarmsd = pickle.load(f)
                eeker.dblock_alarmsd.release()
                logging.info("Thread_initALARMSD" + '\t' + 
                    "Success. Size of eeker.db_alarmsd = %s" % str(len(eeker.db_alarmsd)))
        except Exception as e:
            logging.critical("Thread_initALARMSD" + '\t' + 
                "Exception loading db_alarmsd pickle: " + str(e))
            '''If loading from disk fails we know we need to create a new alarm 
            database/dict. We'll pass in the eeker.db_cts which is the data we got 
            from the foodfile and we'll get an alarm db in return along 
            with an update timestamp'''
            initALARMSD()
        logging.debug("Thread_initALARMSD: STOPPING")
        return

class Thread_timer(threading.Thread):
    def run(self):
        logging.debug("Thread_timer: STARTING")
        eeker.timer_counter_lock.acquire()
        eeker.timer_counter = 0
        logging.debug("Thread_timer: counter initialized = " + str(eeker.timer_counter))
        eeker.timer_counter_lock.release()        
        eeker.timer_running_lock.acquire()
        eeker.timer_running = True
        logging.debug("Thread_timer RUNNING!")
        eeker.timer_running_lock.release()
        while 1:
            if not eeker.timer_killswitch and eeker.autoupdate:
                if eeker.timer_counter > (eeker.autoupdate_frequency / 3):
                    logging.debug("Thread_timer: counter over 200*3sec, kicking off refresh...")
                    eeker.updatingalready_lock.acquire()
                    eeker.updatingalready = True
                    eeker.updatingalready_lock.release()
                    
                    t_updateALL = Thread_UpdateALL()
                    t_updateALL.start()
                    t_updateALL.join()
                    
                    eeker.updatingalready_lock.acquire()
                    eeker.updatingalready = False
                    eeker.updatingalready_lock.release()
                    
                    #reset counter back to zero
                    eeker.timer_counter_lock.acquire()
                    eeker.timer_counter = 0
                    eeker.timer_counter_lock.release()
                else:
                    eeker.timer_counter_lock.acquire()
                    eeker.timer_counter += 1
                    eeker.autoupdate_frequency_lock.acquire()
                    logging.debug("Thread_timer: counter = " + str(eeker.timer_counter) + " of " + str(eeker.autoupdate_frequency / 3))
                    eeker.autoupdate_frequency_lock.release()
                    eeker.timer_counter_lock.release()
                    time.sleep(3)
            else:
                eeker.timer_running_lock.acquire()
                eeker.timer_running = False
                logging.debug("Thread_timer STOPPING!")
                eeker.timer_running_lock.release()  
                break
        logging.debug("Thread_timer: STOPPING")
        return
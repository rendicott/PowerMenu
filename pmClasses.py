'''
This PowerMenu module defines the object Classes required for PowerMenu 
operation.
'''
# standard library imports
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
import threading
import random

# internal imports
import pmConfig
from pmConfig import display_format_alarm,display_format_metrocell_status
from pmConfig import display_format_metrocell,display_format_metrocell_full



def get_random_number(numLen):
    num = ''
    for i in range(numLen):
        num += random.choice('0123456789')
    return num

#define a list of files created in this session
class FileLog(list):
    def __init__(self):
        self.length = 0
    def size(self):
        return len(self)
    def getlast(self,number=None):
        #returns the last x items from the list, 
        # if no number given, returns the last item from the list
        
        #default to '1' if no number given
        if number==None:
            number=1
        #validate that what was given is an integer
        try:
            num = int(number)
        except ValueError:
            # print "Exception with number passed into FileLog class 
            # 'getlast' method. Not an integer. Defaulting to '1'"
            num=1
        #now we need to check and make sure the num isn't longer than the list
        if num > len(self):
            num = len(self)
        results = []
        if num < len(self):
            if len(self) > 1:
                gobackcount = len(self)-(num+1)
                results = self[:gobackcount:-1]
            elif len(self) == 1:
                results = self[::-1]
        elif num == len(self):
            results = list(self)
        return results
    def display(self):
        for fileo in self:
            print "\t\t ------------------------------------"
            print "\t\t Filename: " + fileo.filename
            print "\t\t Abs Path: " + fileo.abspath
            print "\t\t Timestamp: " + fileo.datecreated
        print ""
        print "\t\tLength of file_log = " + str(len(self))
        
class SuperList(list):
    """Subclass the list type so we can add properties and methods. This list
    will hold both types of major objects (Alarm and Metrocell) and provide
    methods to do things like look up the last time the SuperList was updated
    and methods to write the list to disk using pickle. 
    
    """
    def __init__(self):
        self.timeupdated_bsg = ''
        self.timeupdated_wms = ''
        self.timeupdated_alarm = ''
    def writetodisk(self,filename,label=None):
        if label == None:
            label = 'SuperList'
        try:
            #print "\tWriting "+ label +" pickle to disk"
            logging.info('\t' + 
                "Writing Superlist pickle to disk. Type/Label: "+label)
            with open(filename,'wb') as f:
                pickle.dump(self,f)
        except Exception as e:
            logging.critical('\t' + 
                "Got an exception when trying to write the "
                "Superlist pickle to disk: " + str(e))
    def isolderthan(hours):
        ''' returns true if self.timeupdated is older than 
        called hours. Limited to .timeupdated_wms for now
        '''
        

#define an object class structure for an Alarm
class Alarm:
    """This object is intended to represent an alarm on from the WMS. It's
    primarily made up of basic alarm properties and methods to display the
    alarm object on request.
    
    """
    def __init__(self,
                index,
                alarmedComponent,
                eventTime,
                notificationIdentifier,
                bSRName,
                additionalText,
                specificProblems,
                monitoredStatus
                ):
        self.index = index
        self.alarmedComponent = alarmedComponent
        self.eventTime = eventTime
        self.notificationIdentifier = notificationIdentifier
        self.monitoredStatus = monitoredStatus
        self.adminStatus = ''
        if bSRName != None:
            self.bSRName = bSRName
        else:
            self.bSRName = 'NA'
        self.additionalText = additionalText
        self.specificProblems = specificProblems
        self.fgw = ''
        self.cid = ''
    #define the default format for "printing" an alarm
    def rowformat(self,chosencolor):
        return display_format_alarm.format(
                        str(self.index),
                        self.notificationIdentifier,
                        self.specificProblems[:30],
                        self.eventTime,
                        self.alarmedComponent,
                        self.bSRName,
                        self.monitoredStatus,
                        self.adminStatus,
                        self.cid,
                        self.fgw
                        )
    def csvformat(self):
        fieldlist = [self.notificationIdentifier,self.specificProblems,
                self.eventTime,self.alarmedComponent,self.bSRName,
                self.monitoredStatus,self.adminStatus,self.cid,self.fgw]
        return ','.join(fieldlist)


                            
class Metrocell:
    def __init__(self,
                index,
                femtoId,
                serial,
                bsrName,
                bsrId,
                groupName,
                swVersion,
                specInfo,
                monitoredStatus,
                ipsecIpAddr,
                clusterId,
                groupId,
                fgw,
                gagr, #property to note grid/gateway
                adminStatus
                ):
        self.index = index
        if femtoId != None:
            self.femtoId = femtoId
        else:
            self.femtoId = 'NA'
        if serial != None:
            self.serial = serial
        else:
            self.serial = 'NA'
        if bsrName != None:
            self.bsrName = bsrName
        else:
            self.bsrName = 'NA'
        if groupId != None:
            self.groupId = groupId
        else:
            self.groupId = 'NA'
        if clusterId != None:
            self.clusterId = clusterId
        else:
            self.clusterId = 'NA'
        if bsrId != None:
            self.bsrId = bsrId
        else:
            self.bsrId = 'NA'
        if groupName != None:
            self.groupName = groupName
        else:
            self.groupName = 'NA'
        if swVersion != None:
            self.swVersion = swVersion
        else:
            self.swVersion = 'NA'
        if specInfo != None:
            self.specInfo = specInfo
        else:
            self.specInfo = 'NA'
        if monitoredStatus != None:
            self.monitoredStatus = monitoredStatus
        else:
            self.monitoredStatus = 'NA'
        if ipsecIpAddr != None:
            self.ipsecIpAddr = ipsecIpAddr
        else:
            self.ipsecIpAddr = 'NA'
        if fgw != None:
            self.fgw = fgw
        else:
            self.fgw = 'NA'
        if gagr != None:
            self.gagr = 'NA'
        else:
            self.gagr = gagr
        if adminStatus != None:
            self.adminStatus = adminStatus
        else:
            self.adminStatus = 'NA'
        #BEGIN DETAIL SECTION, NOT DECLARED ON INIT
        self.bsrAStatus = 'NA'
        self.bsrOStatus = 'NA'
        self.cellAStatus = 'NA'
        self.cellOStatus = 'NA'
        self.ueStatus = []
        self.firstnonprivateip = 'NA'
        self.neighbors = []
        self.usecase = ''
        #assume Metrocell is unhealthy until proven otherwise
        self.healthy = False
        self.inalarm = False
        self.alarms = []
        self.usid = ''
        self.faloc = ''
        self.inout = ''
        self.tech = ''
        self.ctsname = ''
        self.updown = []
        self.list_rawdata = []
        # adding properties for netwalk export
        self.hostname = self.bsrName
        self.mac = ''
        self.fpip = self.firstnonprivateip
        self.defaultroute = ''
        self.ipaddr = ''
        self.netmask = ''
        self.dhcps = ''
        self.ipsecIpAddr_old = '' # adding old and new to handle updates
        self.ipsecIpAddr_new = ''
    def __eq__(self, other):
        return self.bsrName==other.bsrName
    def __hash__(self):
        return hash(('bsrName', self.bsrName))
    #define the default format for "printing" an Metrocell
    def rowformat(self,chosencolor):
        marker = ''
        if self.adminStatus == 'locked' and chosencolor != '':
            c_adminStatus = '\033[1;31m' + self.adminStatus + '\033[m'
        else:
            c_adminStatus = self.adminStatus
        if self.ipsecIpAddr == 'NA':
            c_ipsecIpAddr = 'offline'
        else:
            c_ipsecIpAddr = self.ipsecIpAddr
        if self.inalarm:
            marker = '  * '
        return display_format_metrocell.format(
                            str(self.index),
                            self.bsrName[0:13],
                            self.serial[0:10],
                            self.bsrId,
                            self.groupName[2:23],
                            self.specInfo[0:30],
                            self.monitoredStatus,
                            c_ipsecIpAddr,
                            self.clusterId,
                            self.groupId,
                            self.fgw,
                            self.gagr,
                            c_adminStatus,
                            marker
                            )
    def rowformat_full(self,chosencolor):
        marker = ''
        if self.adminStatus == 'locked' and chosencolor != '':
            c_adminStatus = '\033[1;31m' + self.adminStatus + '\033[m'
        else:
            c_adminStatus = self.adminStatus
        if self.ipsecIpAddr == 'NA':
            c_ipsecIpAddr = 'offline'
        else:
            c_ipsecIpAddr = self.ipsecIpAddr
        if self.inalarm:
            marker = '  * '
        return display_format_metrocell_full.format(
                            str(self.index),
                            self.bsrName[0:13],
                            self.serial[0:10],
                            self.bsrId,
                            self.groupName[2:23],
                            self.ctsname[0:20],
                            self.specInfo[0:30],
                            self.monitoredStatus,
                            c_ipsecIpAddr,
                            self.clusterId,
                            self.groupId,
                            self.fgw[0:15],
                            self.gagr,
                            self.usid[0:7],
                            self.faloc,
                            self.inout,
                            self.tech,
                            marker,
                            self.usecase[0:4],
                            self.swVersion,
                            c_adminStatus,
                            )
    def status(self):
        if self.cellAStatus == 'unlocked':
            cellAStatus = '\033[1;32munlocked\033[m'
        else:
            cellAStatus = self.cellAStatus
        if self.cellOStatus == 'enabled':
            cellOStatus = '\033[1;32menabled\033[m'
        else:
            cellOStatus = self.cellOStatus
        if self.bsrAStatus == 'unlocked':
            bsrAStatus = '\033[1;32munlocked\033[m'
        else:
            bsrAStatus = self.bsrAStatus
        if self.bsrOStatus == 'enabled':
            bsrOStatus = '\033[1;32menabled\033[m'
        else:
            bsrOStatus = self.bsrOStatus

        print ""
        print "\t\t---"+self.bsrName+"---"
        print "\t\tLCell: " + cellAStatus + "/" + cellOStatus
        print "\t\tBSR: " + bsrAStatus + "/" + bsrOStatus
        print "\t\tueStatus IMSI list: " 
        for imsi in self.ueStatus:
            print "\t\t\t" + imsi,
        print ""
        print "\t\tFirst NonPrivate IP: " + self.firstnonprivateip
        print "\t\tNeighbor bsrIds:"
        print "\t\t\t",
        for bsr in self.neighbors:
            print bsr,
        print ""
        # adding a section here to show the LCell 
        # up/down time on the 'verbose' view of an AP check
        print "\t\tLCell Up/Down Log (covers roughly the last three days):" 
        print(
            "\t\t\t===NOTE: ALL TIMESTAMPS ARE FOR THE AP'S LOCAL TIME ZONE===")
        for h in self.updown:
            print '\t\t\t' + h.strip('\r\n')
        print ""
    def rowstatus(self,chosencolor):
        #do some health checks to determine print color
        try:
            chosencolor
        except:
            chosencolor = ''
        if chosencolor != '':
            if (self.cellAStatus == 'unlocked' and 
                    self.cellOStatus == 'enabled' and 
                    self.bsrAStatus == 'unlocked' and 
                    self.bsrOStatus == 'enabled' and 
                    self.adminStatus == 'unlocked'):
                c_bsrName = '\033[1;32m' + self.bsrName + '\033[m'
            elif (self.cellOStatus == 'enabled' and 
                    self.bsrAStatus == 'unlocked' and 
                    self.bsrOStatus == 'enabled' and 
                    self.adminStatus == 'unlocked'):
                c_bsrName = '\033[1;33m' + self.bsrName + '\033[m'
            else:
                c_bsrName = '\033[1;31m' + self.bsrName + '\033[m'
        else:
            c_bsrName = self.bsrName
        try:
            if len(self.ueStatus) >= 1:
                    ueconnected = 'YES'
            else:
                ueconnected = 'no'
        except Exception as e:
            logging.error("\tself.ueStatus error or not defined: " + str(e))
            ueconnected = 'no'
        #now just determine overall status as a boolean 'healthy'
        if (self.cellAStatus == 'unlocked' and 
                self.cellOStatus == 'enabled' and 
                self.bsrAStatus == 'unlocked' and 
                self.bsrOStatus == 'enabled' and 
                self.adminStatus == 'unlocked'):
            self.healthy = True
        alarmer = ''
        if self.inalarm:
            alarmer = '*'
        return display_format_metrocell_status.format(
                            self.monitoredStatus,
                            self.ipsecIpAddr,
                            self.gagr,
                            self.adminStatus,
                            self.bsrAStatus,
                            self.bsrOStatus,
                            self.cellAStatus,
                            self.cellOStatus,
                            ueconnected,
                            self.clusterId,
                            self.groupId,
                            self.fgw,
                            alarmer,
                            c_bsrName,
                            self.mac,
                            self.ipaddr,
                            self.fpip,
                            self.defaultroute,
                            self.netmask,
                            self.dhcps
                            )
    def csvformat(self):
        try:
            if len(self.ueStatus) >= 1:
                    ueconnected = 'YES'
            else:
                ueconnected = 'no'
        except Exception as e:
            logging.error("\tself.ueStatus error or not defined: " + str(e))
            ueconnected = 'no'
        fieldlist = [self.bsrName,self.serial,self.bsrId,self.groupName,
                    self.specInfo,self.monitoredStatus,self.ipsecIpAddr,
                    self.clusterId,self.groupId,self.fgw,self.gagr,
                    self.adminStatus ,self.bsrAStatus,self.bsrOStatus,
                    self.cellAStatus,self.cellOStatus,ueconnected]
        return (','.join(fieldlist))
    def csvformat_full(self):
        marker = ''
        try:
            if len(self.ueStatus) >= 1:
                    ueconnected = 'YES'
            else:
                ueconnected = 'no'
        except Exception as e:
            logging.error("\tself.ueStatus error or not defined: " + str(e))
            ueconnected = 'no'
        if self.inalarm:
            marker = '  * '
        try:
            gagr = self.gagr
            if gagr == None:
                gagr = ''
        except:
            gagr = ''
        fieldlist = [str(self.index),self.bsrName,self.serial,
                        self.bsrId,self.groupName,self.ctsname,self.specInfo,
                        self.monitoredStatus,self.ipsecIpAddr,self.clusterId,
                        self.groupId,self.fgw,gagr,self.usid,self.faloc,
                        self.inout,self.tech,marker,self.usecase[0:4],self.swVersion,
                        self.adminStatus]
        return (','.join(fieldlist))
    def csvformat_status(self):
        try:
            if len(self.ueStatus) >= 1:
                    ueconnected = 'YES'
            else:
                ueconnected = 'no'
        except Exception as e:
            logging.error("\tself.ueStatus error or not defined: " + str(e))
            ueconnected = 'no'
        fieldlist = [self.monitoredStatus,self.ipsecIpAddr,self.gagr,
                    self.adminStatus ,self.bsrAStatus,self.bsrOStatus,
                    self.cellAStatus,self.cellOStatus,ueconnected,self.bsrName,
                    self.mac,self.ipaddr,self.fpip,self.defaultroute,self.netmask,self.dhcps]
        return (','.join(fieldlist))
    def genxml(self):
        ''' Returns the MetroCell serialized as XML
        Specifically formatted for NetWalk exports
        '''
        import xml.etree.ElementTree as ET
        guid = get_random_number(10)
        x_metro = ET.Element('member',attrib={'id':guid})
        
        x_metro_hostname = ET.SubElement(x_metro,'hostname')
        x_metro_hostname.text = self.hostname

        x_metro_ipaddr = ET.SubElement(x_metro,'ipaddr')
        x_metro_ipaddr.text = self.ipaddr

        x_metro_netmask = ET.SubElement(x_metro,'netmask')
        x_metro_netmask.text = self.netmask

        x_metro_defaultroute = ET.SubElement(x_metro,'defaultroute')
        x_metro_defaultroute.text = self.defaultroute

        x_metro_dhcps = ET.SubElement(x_metro,'dhcps')
        x_metro_dhcps.text = self.dhcps

        x_metro_mac = ET.SubElement(x_metro,'mac')
        x_metro_mac.text = self.mac

        x_metro_custom = ET.SubElement(x_metro,'custom',attrib={'tag':'metrocell'})
        x_metro_custom_fpip = ET.SubElement(x_metro_custom,'fpip')
        x_metro_custom_fpip.text = self.fpip
        
        return(x_metro)

class File_Log_Entry:
    def __init__(self,abspath,filename,datecreated):
        self.abspath = abspath
        self.filename = filename
        self.datecreated = datecreated

class Cts_Entry:
    def __init__(self,cmid,tech,status,ename,pname,pid,usid,faloc,loc):
        self.cmid = cmid
        self.tech = tech
        self.status = status
        self.ename = ename
        self.pname = pname
        self.pid = pid
        self.usid = usid
        self.faloc = faloc
        self.loc = loc
    def printself(self):
        return(self.cmid,self.tech,self.status,self.ename,
                self.pname,self.pid,self.usid,self.faloc,self.loc)

class UCEntry():
    ''' Class to hold data parsed from the Granite feed
    for Use Case information. 
    '''
    def __init__(self,bsrName,uc):
        self.bsrName = bsrName
        self.uc = uc
    def __eq__(self, other):
        return self.bsrName==other.bsrName
    def __hash__(self):
        return hash(('bsrName', self.bsrName))
    def __repr__(self):
        return(self.bsrName + '\t\t' + self.uc)

class Cfg(object):
    def __init__(self):
        self.ready = False # set up readyness to combat race cond
        self.gagroption = False
        self.ucgranoption = False
        self.ucgran_data = []
        self.ucgran_obdata = []
        self.fullformat = True
        self.chosencolor = ''
        self.csvdumpbool = False
        self.macrolist = []
        self.monfilter = True
        self.fgwpw = '' #the fgw password
        self.apopw = '' #the AP localOperator password
        self.apapw = '' #the AP localAdmin password
        self.femtostatus_timeout = '8' #default value, can modify in menu
        # set up the path holder for the foodfile
        self.foodfile = ''
        #whether or not show verbosity after AP checks
        self.apcheck_verbosebool = False 
        self.bsgdump_bool = pmConfig.bsgdump_bool
        self.bsgdump_fname_prefix = pmConfig.bsgdump_fname_prefix
        self.bsg_offline_bool = False
        self.bsgdump_offline_pull_dir = pmConfig.bsgdump_offline_pull_dir
        # set up the global databases
        self.db_alarmsd = {}
        self.timeUpdated_alarms = '' 
        self.db_alarmso = SuperList()
        self.db_femtos = SuperList()
        self.db_cts = []
        # set up global locks
        self.screenlock = threading.RLock()
        self.dblock = threading.RLock()
        self.dblock_alarmsd = threading.RLock()
        self.dblock_alarmso = threading.RLock()
        # set up global protection
        self.updatingalready_lock = threading.RLock()
        self.updatingalready = False
        # set up flag for auto-update
        self.autoupdate = False
        self.autoupdate_frequency = 600
        self.autoupdate_frequency_lock = threading.RLock()
        self.timer_running = False
        self.timer_running_lock = threading.RLock()
        self.timer_counter = 0
        self.timer_counter_lock = threading.RLock()
        self.timer_killswitch = False
        self.bool_silentupdates = False #by default set threaded updates to non-silent
'''create a configuration (Cfg) object to hold options instead of 
using global vars. Then we can just pass the options 
around into each function'''
eeker = Cfg() #we'll call it eeker so it's unique
eeker.ready = True
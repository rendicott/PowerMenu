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
This PowerMenu module contains misc. functions required for operation
of the PowerMenu. It's primarily for taking bulky static code out of the 
main pm.py file. 
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
import zipfile
import zlib


#internal modules imports
from pmClasses import eeker # super important that this is first

import pmConfig
import pmLoaders
import pmClasses

from pmConfig import sversion
from pmConfig import header_alarm
from pmConfig import header_status
from pmConfig import header_metro
from pmConfig import header_metrofull
from pmConfig import sep_status
from pmConfig import sep_metro
from pmConfig import sep_metrofull
from pmConfig import sep_alarm
from pmConfig import header_alarm_csv
from pmConfig import header_metro_csv
from pmConfig import header_metro_full_csv
from pmConfig import header_status_csv

#create a new list of filelog class type	
file_log = pmClasses.FileLog()

def return_file_log():
    return file_log

def printLogoIntro():
    print ""
    print " _____                       __  __                   "
    print "|  __ \                     |  \/  |                  "
    print "| |__) |____      _____ _ __| \  / | ___ _ __  _   _  "
    print "|  ___/ _ \ \ /\ / / _ \ '__| |\/| |/ _ \ '_ \| | | | "
    print "| |  | (_) \ V  V /  __/ |  | |  | |  __/ | | | |_| | "
    print "|_|   \___/ \_/\_/ \___|_|  |_|  |_|\___|_| |_|\__,_| "

    print "       === ALU WMS Metrocell Power Menu ==="
    print "       |     Creator: rendicott@gmail.com"
    print "       |     Date: 2014-11-20"
    print "       |     Version: " + pmConfig.sversion
    print "       ===================================="
    print ""

def coloredList(list,
                type,
                thetimeyouwant,
                datasourcelist,
                showfgwbool,
                suppress_csv=None):
    myfunc = str(pmLoaders.giveupthefunc())
    '''
    list: Some sort of list of results you want displayed
    type: options are "alarm, metro, metrofull, status"
        #the 'type' specifies which footer to put on the data for column names. 
    thetimeyouwant: either a timestamp string for override or 'NA'
    datasourcelist: either the inventory source or 'NA'
    showfgwbool: (True/False) whether you want full fgw name in alarmedcomponent
    suppress_csv: Boolean: Whether or not to bypass writing CSV
    '''

    #takes a list of objects and prints it in color
    if suppress_csv==None:
        suppress_csv = False
    #first define the function that just dumps the raw colored data
    def dumpdata_status(list,chosencolor):
        colorflag = True
        for item in list:
            if colorflag and chosencolor != '':
                print('\033[1;' + chosencolor + 
                    item.rowstatus(chosencolor) + '\033[m')
            if colorflag and chosencolor == '':
                print item.rowstatus(chosencolor)
            if not colorflag:
                print item.rowstatus(chosencolor)
            colorflag = not colorflag
    def dumpdata_rowformat(list,chosencolor):
        logging.debug("\t I'm inside the dumpdata_rowformat function")
        colorflag = True
        for item in list:
            if colorflag and chosencolor != '':
                print('\033[1;' + chosencolor + 
                    item.rowformat(chosencolor) + '\033[m')
            if colorflag and chosencolor == '':
                print item.rowformat(chosencolor)
            if not colorflag:
                print item.rowformat(chosencolor)
            colorflag = not colorflag
        logging.debug("\t I'm leaving the dumpdata_rowformat function")
    def dumpdata_rowformat_full(list,chosencolor):
        logging.debug("\t I'm inside the dumpdata_rowformat_full function")
        colorflag = True
        for item in list:
            if colorflag and chosencolor != '':
                print('\033[1;' + chosencolor + 
                    item.rowformat_full(chosencolor) + '\033[m')
            if colorflag and chosencolor == '':
                print item.rowformat_full(chosencolor)
            if not colorflag:
                print item.rowformat_full(chosencolor)
            colorflag = not colorflag
        logging.debug("\t I'm leaving the dumpdata_rowformat_full function")
    print ""
    try:
        if thetimeyouwant != 'NA':
            #meaning the function wanted to give a specific time
            print "\t\t\t Data Timestamp: " + thetimeyouwant
        else:
            #we'll just pull timestamps from the data source
            print("\t\t ipsecIpAddr's updated: " + 
                datasourcelist.timeupdated_bsg + 
                "\t Everything else updated: " + 
                datasourcelist.timeupdated_wms
                )
    except:
        #for some reason couldn't process function arguments for timestamp
        print "\t\t\t Data Timestamp = NA"
    '''now define the type sections, this is mainly for separators 
    and column header lists'''
    if type == 'status':
        print sep_status
        dumpdata_status(list,eeker.chosencolor)
        print sep_status
        print header_status
    elif type == 'metro':
        if eeker.fullformat:
            print sep_metrofull
            dumpdata_rowformat_full(list,eeker.chosencolor)
            print sep_metrofull
            print header_metrofull
            print ""
        else:
            print sep_metro
            dumpdata_rowformat(list,eeker.chosencolor)
            print sep_metro
            print header_metro
            print ""
    elif type == 'metrofull':
        print sep_metrofull
        dumpdata_rowformat_full(list,eeker.chosencolor)
        print sep_metrofull
        print header_metrofull
        print ""
    elif type == 'alarm':
        try:
            print sep_alarm
            dumpdata_rowformat(list,eeker.chosencolor)
            print sep_alarm
            print header_alarm
            print ""
        except ValueError:
            print("Something went wrong printing the table header row: '" + 
                str(sys.exc_info()[0]) + "'")
    else:
        print "============================================================="
        for o in list:
            print o.rowformat(eeker.chosencolor)
        print "============================================================="
    print "Number of results: " + str(len(list))
    logging.debug(myfunc + '\t' + 
        "Search returned number of results: " + str(len(list)))
    if eeker.csvdumpbool and not suppress_csv:
        #now try and write the results to csv
        logging.debug(myfunc + '\t' + 
            "Now attempting to send list to write_to_csv function")
        write_to_csv(list,tag=type)
    list = []

    
def write_to_csv(listofobj,tag=None,filename=None):
    '''Takes a list of objects and a custom tagword then writes the 
    list of objects to csv with the "timestamp-tag.csv" format. 
    (e.g, 20141027_083000-alarms.csv)'''
    myfunc = str(pmLoaders.giveupthefunc())
    global lastresultfile
    global file_log
    #handle default tag if none is given
    if tag == None:
        tag = 'generic'
    logging.debug(myfunc + '\t' + "Got list of length " + str(len(listofobj)))
    logging.debug(myfunc + '\t' + "Got tag of type: " + str(tag))
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    if filename==None:
        if eeker.fullformat and tag == 'metro':
            filename = timestamp + '-' + 'metrofull' + '.csv'
        else:
            filename = timestamp + '-' + tag + '.csv'
    else:
        filename = filename + timestamp + '.csv'

    try:	
        #first write the column headers (defined in global)
        with open(filename,'wb') as f:
            if tag == 'alarm':
                f.write(header_alarm_csv + '\r')
            elif tag == 'metro':
                if eeker.fullformat:
                    f.write(header_metro_full_csv + '\r')
                else:
                    f.write(header_metro_csv + '\r')
            elif tag == 'metrofull':
                f.write(header_metro_full_csv + '\r')
            elif tag == 'status':
                f.write(header_status_csv + '\r')
        #now loop through the list and write data to csv
            for o in listofobj:
                try:
                    if tag == 'status':
                        f.write(o.csvformat_status() + '\r')
                    elif tag == 'metro' and eeker.fullformat:
                        f.write(o.csvformat_full() + '\r')
                    else:
                        f.write(o.csvformat() + '\r')
                except Exception as ee:
                    f.write("ERROR OBJECT," + str(o) + '\r')
                    logging.error(myfunc + '\t' + 
                        "Got exception with object " + str(o) + " : " + str(ee))
        try:
            env_abspath = os.path.abspath(filename)
            print("\t\t\t\t\t\t\t\t\t\t\t\t\t WROTE ABOVE RESULTS TO : " + 
                env_abspath)
        except Exception as ee:
            logging.error(myfunc + '\t' + 
                "Exception pulling filename absolute path: " + str(ee))
            env_abspath = ''
    except Exception as e:
        logging.critical(myfunc + '\t' + "Got exception writing csv data:" + 
            str(e))
    #store the last filename in case we want to email it or something later
    file_log.append(pmClasses.File_Log_Entry(env_abspath,filename,timestamp))
    logging.debug(myfunc + '\t' + "Lenth of file_log: " + str(len(file_log)))

def email_result(subject=None,body=None,email=None,howmany=None):
    myfunc = str(pmLoaders.giveupthefunc())
    #make sure we're working with the global file_log
    global file_log
    #first check to see if there's anything in file_log
    # if not, then we can't do anything
    if len(file_log) != 0:
        if howmany==None:
            '''pull the last file log object from the file_log and add 
            it to a list'''
            filelist = file_log.getlast()
        else:
            filelist = file_log.getlast(howmany)
            '''
            >>> print stringlist[:len(stringlist)-3:-1]
            ['dog', 'lazy']
            '''
        logging.debug(myfunc + '\t' + 
            "Length of file_list: " + str(len(filelist)))
        if subject==None:
            subject="PowerMenu Query Result"
        if body==None:
            body=("This report was generated by the Operations PowerMenu."
                " Created by rendicott@gmail.com")
        if email==None:
            userinput_email = ''
            try:
                while userinput_email != 'q':
                    try:
                        userinput_email = eeker.macrolist.pop()
                    except:
                        userinput_email = raw_input(
                            "\t Enter an email address ('q' to cancel): ")
                        logging.debug(myfunc + '\t' + 
                            "Got raw userinput_email: " + 
                            str(userinput_email))
                    logging.debug(myfunc + '\t' + 
                        "Validating userinput_email with regex...")
                    re_userinput_email = re.compile('(.*)(@)(.*)(\.)(.*)')
                    userinput_email_match = re.search(
                        re_userinput_email,userinput_email)
                    logging.debug(myfunc + '\t' + 
                        "Successful regex email match? = " + 
                        str(userinput_email_match))
                    if userinput_email_match:
                        email = userinput_email_match.group()
                        break
                    else:
                        print "Bad email format detected, try again."
            except Exception as h:
                logging.critical(myfunc + '\t' + 
                    "Exception parsing email address: " + str(h))
        successflag = False
        try:
            print "Sending email with the following information: "
            print ""
            print "\t Subject: \t" + subject
            print "\t Body: \t\t" + body
            print "\t Attach: \t",
            for i,file in enumerate(filelist):
                if i == len(filelist)-1:
                    print file.filename
                else:
                    print file.filename + ",",
            logging.debug(myfunc + '\t' + 
                "Now trying to print email address to screen...")
            print "\t Recipient:\t" + email
            print ""
            try:
                '''Now we'll try and build the 'mailx' command. it's a 
                strange one, got this command structure courtesy 
                of Lee Murphy (lm3521)'''
                
                #first we have to write the body to a file
                try:
                    with open('body.txt','wb') as f:
                        #Had to add the \n or else you get weird problems
                        f.write(body + '\n')
                except Exception as ae:
                    logging.critical(myfunc + '\t' + 
                        "Exception writing 'body' to body.txt :" + str(ae))
                        
                emailcommand_part01 = '( cat body.txt;'
                emailcommand_part03 =  (' ) | mailx -s "' + 
                                        subject + '" ' + email )
                emailcommand_part02 = ''
                for file in filelist:
                    emailcommand_part02 += (' uuencode ' + file.filename + 
                                            ' ' + file.filename + ';')
                emailcommand = (emailcommand_part01 + emailcommand_part02 + 
                                emailcommand_part03)
                logging.debug(myfunc + '\t' + 
                    "Final email command is: " + emailcommand)
                try:
                    logging.debug(myfunc + '\t' + pmConfig.rob)
                    email_result_file = os.popen(emailcommand)
                    email_result = email_result_file.readlines()
                    
                    email_result_length = len(email_result)
                    
                    for i,line in enumerate(email_result):
                        print("\t\t\t email_result line (" + str(i) + " of " + 
                            str(remail_result_length) + ") :" + str(line))
                        if line != '':
                            print "Something went wrong: ", line
                            break
                        else:
                            successflag = True
                            break
                    if successflag:
                        print "Your email should arrive in the next 5 minutes."
                except Exception as ee:
                    logging.critical(myfunc + '\t' + 
                        "Exception issuing command: " + str(ee))
                    logging.debug(myfunc + '\t' + 
                        "Command was: " + emailcommand)
            except Exception as ef:
                logging.critical(myfunc + '\t' + 
                    "Got exception parsing email command parameters:" + 
                    str(ef))
        except Exception as e:
            logging.critical(myfunc + '\t' + "Exception: " + str(e))
    else:
        print("Oops, the file_log history is empty. Are you sure you have "
        "CSV dumping turned on? (HINT: 'n' to toggle, 'i' to check)")

def syslog_write_to_disk(loo_femtos):
    ''' takes a list of femto objects and then
    writes the contents of their .list_rawdata property 
    to a file on disk. 

    Then it adds those files to a compressed zip archive
    and adds the zip to the file_log so it can be emailed.  

    '''
    myfunc = str(pmLoaders.giveupthefunc())
    logging.debug(myfunc + '\t' +
        "Received loo_femtos of length: " + str(len(loo_femtos)))
    global file_log

    t_filelist = []
    for obj in loo_femtos:
        nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = nowtime + "-" + obj.bsrName + '.txt'
        t_filelist.append(filename)
        with open(filename,'wb') as f:
            for line in obj.list_rawdata:
                f.write(line)
    logging.debug(myfunc + '\t' +
        "Number of files written to disk: " + str(len(t_filelist)))
    # now zip up the files
    compression = zipfile.ZIP_DEFLATED
    nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    zipfilename = nowtime + '-bsr_syslogs.zip'
    try:
        zf = zipfile.ZipFile(zipfilename,mode='w')
        for f in t_filelist:
            zf.write(f,compress_type=compression)
        zf.close()
        logging.debug(myfunc + '\t' +
            "Wrote the following zipfile: " + zipfilename)

    except Exception as ee:
        logging.critical(myfunc + '\t' +
            "Exception trying to write zip file: " + zipfilename 
            + " - " + ee)
    # now delete the raw syslogs to save space
    try:
        for f in t_filelist:
            os.remove(f)
        logging.debug(myfunc + '\t' +
            "Deleted raw syslog txt files")
    except Exception as ee:
        logging.critical(myfunc + '\t' +
            "Exception trying to delete raw data txt files: "+ ee)
    # now go through and clear out the rawdata attached to femto object
    for o in loo_femtos:
        o.list_rawdata = []
    logging.debug(myfunc + '\t' +
        "Blanked out .list_rawdata property on all femtos in loo_femtos")
    try:
        env_abspath = os.path.abspath(zipfilename)
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t WROTE SYSLOGS TO : " + 
                env_abspath)
        print("\t\t\t\t\t\t\t\t\t\t\t\t (Use e+N function to email zip file)")
        # append zip file to file log
        file_log.append(pmClasses.File_Log_Entry(env_abspath,zipfilename,nowtime))
    except Exception as ee:
        logging.error(myfunc + '\t' + 
            "Exception pulling filename absolute path: " + str(ee))
        env_abspath = ''

def netwalk_export(resultlist):
    ''' Takes the results from a parse_ap_console_dump and builds
    the xml file and adds it to the global file log for emailing.
    '''
    myfunc = str(pmLoaders.giveupthefunc())
    # first, generate the actual XML
    xmlstring = netwalk_genxml(resultlist)
    global file_log
    #pull site groupName to use as filename
    try:
        sitename = resultlist[0].groupName
    except Exception as ex_sname:
        logging.debug(myfunc + '\t' +
            'Exception pulling sitename for xml filename: ' + str(ex_sname))
        sitename = 'GENERICSITE'
    nowtime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    xmlfilename = 'nwinput-' + sitename + "--" + nowtime + '.xml'
    xmlfilename = xmlfilename.replace(' ','_')
    logging.debug(myfunc + '\t' +
        "Generated filename: '" + xmlfilename + "'")
    # try writing the file to disk
    try:
        with open(xmlfilename,'wb') as f:
            fluffstring = '<?xml version="1.0" encoding="UTF-8"?>'
            f.write(fluffstring)
            f.write(xmlstring)
    except Exception as ex_xwrfile:
        logging.info(myfunc + '\t' +
            "Exception writing to xml file: " + str(ex_xwrfile))
    try:
        env_abspath = os.path.abspath(xmlfilename)
        print("\t\t\t\t\t\t\t\t\t\t\t\t\t WROTE XML TO : " + 
                env_abspath)
        # append xml file to file log
        file_log.append(pmClasses.File_Log_Entry(env_abspath,xmlfilename,nowtime))
    except Exception as ee:
        logging.error(myfunc + '\t' + 
            "Exception pulling filename absolute path: " + str(ee))
        env_abspath = ''

def netwalk_genxml(resultlist):
    ''' Takes results from a parse_ap_console_dump and generates
    xml for the file for the NetWalk API.
    '''
    myfunc = str(pmLoaders.giveupthefunc())
    
    def grand():
        ''' Generates random number from pmClasses func'''
        return(str(pmClasses.get_random_number(10)))

    authpossibilities = [   {
                            'u':    'scs_admin',
                            'p':    'INSERTPASSWORDHERE',
                            },
                            {
                            'u':    'scr_admin',
                            'p':    'INSERTPASSWORDHERE',
                            },
                            {
                            'u':    'admin',
                            'p':    'INSERTPASSWORDHERE',
                            },
                            {
                            'u':    'admin',
                            'p':    'INSERTPASSWORDHERE',
                            },
                        ]

    try:
        sitename = resultlist[0].groupName
    except Exception as ex_sname:
        logging.debug(myfunc + '\t' +
            'Exception pulling sitename for xml generation: ' + str(ex_sname))
        sitename = 'GENERICSITE'

    import xml.etree.ElementTree as ET
    # generate the entire netwalk-input xml root structure
    try:
        x_root = ET.Element('root')
        
        x_tgt = ET.SubElement(x_root,'target',attrib={'id':grand()})
        # find unique fpips in resultlist
        for fpip in set(map((lambda x: x.fpip),resultlist)):
            if fpip == '0.0.0.0' or fpip == '':
                break
            x_tgt_ent = ET.SubElement(x_tgt,'entrypoint',attrib={'id':grand()})
            x_tgt_ent_attr = ET.SubElement(x_tgt_ent,'attributes')
            x_tgt_ent_attr_ipaddr = ET.SubElement(x_tgt_ent_attr,'ipaddr')
            x_tgt_ent_attr_port = ET.SubElement(x_tgt_ent_attr,'port')
            x_tgt_ent_attr_hostname = ET.SubElement(x_tgt_ent_attr,'hostname')
            x_tgt_ent_attr_ipaddr.text = fpip
            x_tgt_ent_attr_port.text = '22'
            x_tgt_ent_attr_hostname.text = 'SCSR--' + sitename + '-' + grand()

        x_tgt_auth = ET.SubElement(x_tgt,'auth')
        for poss in authpossibilities:
            x_tgt_auth_poss = ET.SubElement(x_tgt_auth,'possibility',attrib={'id':grand()})
            x_tgt_auth_poss_u = ET.SubElement(x_tgt_auth_poss,'username')
            x_tgt_auth_poss_p = ET.SubElement(x_tgt_auth_poss,'password')
            x_tgt_auth_poss_u.text = poss.get('u')
            x_tgt_auth_poss_p.text = poss.get('p')

        # Now create the members section and generate the member xml from resultlist
        x_tgt_members = ET.SubElement(x_tgt,'members')
        for metrocell in resultlist:
            try:
                x_tgt_members.append(metrocell.genxml())
            except Exception as mex:
                logging.debug(myfunc + '\t' +
                    "Exception Metrocell.genxml(): " + str(mex))

    except Exception as nwex:
        logging.debug(myfunc + '\t' +
            "Exception netwalk_export() gen XML: " + str(nwex))

    # finally, return the xml as string
    try:
        xmlstring = ET.tostring(x_root)
        return(xmlstring)
        msg = ":::::::::::BEGIN GENERATED XML STRING:::::::::::::::\n\r"
        msg += xmlstring
        msg += "\n\r:::::::::::END GENERATED XML STRING:::::::::::::::"
        logging.debug(myfunc + '\t' + msg)
    except Exception as exroot:
        logging.debug(myfunc + '\t' + 
            "Exception returning x_root string: " + str(exroot))
    logging.debug(myfunc + '\t' +
        "::::::::::::::EXITING NETWALK_EXPORT:::::::::::")

#def find_stuck_alarms(inventorydb,loo_alarmdb):
def find_stuck_alarms():
    myfunc = str(pmLoaders.giveupthefunc())

    monfilter = True
    bsroosfilter = True
    flipbackcsvdump = False
    rundetailed = True
    verbosebool = False
    emailbool = False
    
    '''Below is a list of types of Metrocell AP alarms that are detectable 
    and undetectable by this function'''
    list_detectable = ['bsrOutOfService',
                        'ipsecTunnelFailureNoResponse',
                        'sctpAssocAssociationDownAlarm',
                        'associationEstablishmentFailure',
                        'noResponseFromBGWY',
                        'csCnConnectivityLost',]
    list_undetectable = ['lmcFailure','securityViolation']
    
    def sifthealthy(stucklist,bsrlist):
        myfunc_i = str(pmLoaders.giveupthefunc())
        for obj in bsrlist:
            try:
                obj.healthy
            except:
                continue
            if not obj.healthy:
                for i,alarm in enumerate(stucklist):
                    try:
                        if obj.bsrName == alarm.bSRName:
                            stucklist.remove(alarm)
                    except Exception as f:
                        logging.debug(myfunc_i + '\t' + 
                            ("SIFTHEALTHY: Exception after cycling through "
                            "alarm list and removing alarms for ") + 
                            obj.bsrName + " : " + str(f))
        return stucklist
    
    try:
        wantseenotmon = eeker.macrolist.pop()
    except:
        wantseenotmon = raw_input(
            "Do you want to see 'Not Monitored' AP's? (y/n): ")
    if wantseenotmon == 'y':
        monfilter = False
    print ""
    print "Types of stuck BSR alarms I can detect:"
    for o in list_detectable:
        print "\t DETECTABLE: " + o
    print ""
    print "Types of stuck BSR alarms I can't verify: "
    for p in list_undetectable:
        print "\t UNDETECTABLE: " + p
    print ""
    try:
        wantlimitbsroos = eeker.macrolist.pop()
    except:
        wantlimitbsroos = raw_input(
            "Do you want to limit search to 'bsrOutOfService' "
            "alarms only? (y/n): ")
    if wantlimitbsroos == 'n':
        bsroosfilter = False
    try:
        wantseeverbose = eeker.macrolist.pop()
    except:
        wantseeverbose = raw_input(
            "Do you want to see verbose results? (y/n): ")
    if wantseeverbose == 'y':
        verbosebool = True
    if not eeker.csvdumpbool:
        try:
            fliponcsv = eeker.macrolist.pop()
        except:
            fliponcsv = raw_input(
                "I noticed you had CSV output turned off. Do you want "
                "to output results to CSV? (y/n) ")
        if fliponcsv == 'y':
            flipbackcsvdump = True
            eeker.csvdumpbool = True
    '''now check to see if user wants email. Since we can't email 
    unless csvdump is on, we have to check for it before asking.'''
    if eeker.csvdumpbool:
        try:
            wantemail = eeker.macrolist.pop()
        except:
            wantemail = raw_input("Do you want to email the results? (y/n) ")
        if wantemail == 'y':
            try:
                email_addy = eeker.macrolist.pop()
            except:
                email_addy = raw_input("\tEnter a single email address: ")
            emailbool = True
    print ""
    print "Ok, checking for stuck alarms, this might take a bit..."
    logging.info(myfunc + '\t' + "checking for stuck alarms...")
    bsroosList = []
    print("NOTE: AP's with administrativeState = 'locked' are "
            "filtered from this check.")
    eeker.dblock_alarmso.acquire()
    for k in eeker.db_alarmso:
        if k.adminStatus != 'locked':
            if monfilter and bsroosfilter:
                if (k.specificProblems == 'bsrOutOfService' and 
                    k.monitoredStatus == 'Monitored'):
                        bsroosList.append(k)
            if not monfilter and bsroosfilter:
                if k.specificProblems == 'bsrOutOfService':
                    bsroosList.append(k)
            #oos filter is off so we want all bsr related alarms
            if not monfilter and not bsroosfilter:
                if k.bSRName != '':
                    bsroosList.append(k)
            if monfilter and not bsroosfilter:
                if k.bSRName != '' and k.monitoredStatus == 'Monitored':
                    for alarmtext in list_detectable:
                        if k.specificProblems == alarmtext:
                            bsroosList.append(k)
    eeker.dblock_alarmso.acquire()
    print ""
    if verbosebool:
        try:
            wantseebsralarms = eeker.macrolist.pop()
        except:
            wantseebsralarms = raw_input(
                "Do you want to see list of BSR alarms? (y/n) ")
        if wantseebsralarms == 'y':
            eeker.dblock_alarmso.acquire()
            coloredList(
                        bsroosList,
                        'alarm',
                        eeker.db_alarmso.timeupdated_alarm,
                        'NA',
                        True)
            eeker.dblock_alarmso.release()
    logging.info(myfunc + '\t' + 
        "Number of BSR OOS with alarm: " + str(len(bsroosList)))
    objbsroosList = []
    stuckalarmList = []
    re_ipsecip_111 = '\.'
    re_ipsecip_11 = re.compile(re_ipsecip_111)
    print ""
    print("Now checking status of alarmed AP's, "
            "this could take up to 60 seconds...")
    print ""
    for bsroos in bsroosList:
        mybsr = bsroos.bSRName
        eeker.dblock.acquire()
        for bsr in eeker.db_femtos:
            match_ip = re.search(re_ipsecip_11,bsr.ipsecIpAddr)
            if mybsr == bsr.bsrName:
                if monfilter:
                    if (match_ip and 
                            bsr.monitoredStatus == 'Monitored' and 
                            bsr.adminStatus == 'unlocked'):
                        objbsroosList.append(bsr)
                        stuckalarmList.append(bsroos)
                        print ".",
                if not monfilter:
                    if match_ip and bsr.adminStatus == 'unlocked':
                        objbsroosList.append(bsr)
                        stuckalarmList.append(bsroos)
                        print ".",
        eeker.dblock.release()
    logging.info(myfunc + '\t' + 
        "Number of BSRs with ipSecIpAddr's but still have alarm: " + 
        str(len(objbsroosList)))
    
    print "Showing list of BSR's that have Alarms but appear to be online..."
    print ""
    coloredList(objbsroosList,'metro','NA',eeker.db_femtos,False)

    sortedby='eventTime'
    stuckalarmList.sort(key=operator.attrgetter(sortedby))
    if verbosebool:
        print "Showing initial list of likely stuck alarms..."
        eeker.dblock_alarmso.acquire()
        coloredList(
                    stuckalarmList,
                    'alarm',
                    eeker.db_alarmso.timeupdated_alarm,
                    'NA',
                    True)
        eeker.dblock_alarmso.release()
        
        
    if verbosebool:
        try:
            wantdetailedstatus = eeker.macrolist.pop()
        except:
            question_detailed = ("Do you want to run detailed status "
                        "checks on the list of APs that may have "
                        "stuck alarms? (y/n) ")
            wantdetailedstatus = raw_input(question_detailed)
        if wantdetailedstatus == 'y':
            pmLoaders.pull_ap_console_dump(
                                            objbsroosList,
                                            False
                                            )
            #now write bsr list to csv without displaying on screen
            logging.info(myfunc + '\t' + 
                "Now attempting to send list to write_to_csv function")
            write_to_csv(objbsroosList,'metro','suspect-BSRs')
        else:
            rundetailed = False
    else:
        print("Now running detailed status check on APs with "
                "potential stuck alarms...")
        pmLoaders.pull_ap_console_dump(
                                       objbsroosList,
                                       False
                                       )
        #now write bsr list to csv without displaying on screen
        logging.info(myfunc + '\t' + 
            "Now attempting to send list to write_to_csv function")
        write_to_csv(objbsroosList,'metro','suspect-BSRs')
        
    if rundetailed:
        print ""
        print "Now doing final comparison of AP's to OOS alarms..."
        logging.debug(myfunc + '\t' + 
            "Before entering SIFTHEALTHY, length of 'stuckalarmList' = " + 
            str(len(stuckalarmList)))
        logging.debug(myfunc + '\t' + 
            "Before entering SIFTHEALTHY, length of 'objbsroosList' = " + 
            str(len(objbsroosList)))
        stuckalarmList02 = sifthealthy(stuckalarmList,objbsroosList)
        logging.debug(myfunc + '\t' + 
            "After SIFTHEALTHY, length of 'stuckalarmList02' = " + 
            str(len(stuckalarmList02)))
        logging.debug(myfunc + '\t' + 
            "After SIFTHEALTHY, length of 'objbsroosList' = " + 
            str(len(objbsroosList)))
        print ""
        print "Showing final list of stuck alarms..."
        print ""
        eeker.dblock_alarmso.acquire()
        coloredList(
                    stuckalarmList02,
                    'alarm',
                    eeker.db_alarmso.timeupdated_alarm,
                    'NA',
                    True,
                    True)
        eeker.dblock_alarmso.release()
        write_to_csv(stuckalarmList02,'alarm','stuck-BSR-alarms')
    else:
        print("You chose not to run detailed checks. In that case, "
                "here's the best guess: ")
        eeker.dblock_alarmso.acquire()
        coloredList(
                    stuckalarmList,
                    'alarm',
                    eeker.db_alarmso.timeupdated_alarm,
                    'NA',
                    True,
                    True)
        eeker.dblock_alarmso.release()
        write_to_csv(stuckalarmList,'alarm','stuck-BSR-alarms')
    if emailbool:		
        body = ("Refer to the attached CSVs for stuck alarms "
                "and list of corresponding BSR's.")
        email_result('PowerMenu Stuck Alarms Report',
                    body,
                    email_addy,
                    2)
    '''since we suppressed the writing of the stuck alarms csv through 
    coloredList we'll write one manually with our own custom filename
    flip the CSV dump back off if it was off entering the function'''
    if flipbackcsvdump:
        eeker.csvdumpbool = False
    #empty out unused lists
    bsroosList = []
    objbsroosList = []
    stuckalarmList = []
    
#def reboot_ap(cmid,inventory):    
def reboot_ap(cmid):
    myfunc = str(pmLoaders.giveupthefunc())
    print "Entering AP Reboot function."
    logging.debug(myfunc + '\t' + "Got cmid of: '" + cmid + "'")
    from pmConfig import femtostatus_script,reboot_script
    fgwname = ''
    mobject = ''
    fgwip = ''
    mip = ''
    scannedser = ''
    eeker.dblock.acquire()
    for o in eeker.db_femtos:
        if o.bsrName == cmid:
            '''take this Metrocell object and hold it in case we need 
            more info from it'''
            mobject = o
            break
    try:
        fgwname = mobject.fgw
        logging.debug(myfunc + '\t' + "Got fgw of: '" + fgwname + "'")
        #cycle through fgwList to find IP
        for i in pmConfig.fgwList:
            if i.get('fgwName') == fgwname:
                fgwip = i.get('fgwIP')
                break
        mip = mobject.ipsecIpAddr
        logging.debug(myfunc + '\t' + "Got mip of: '" + mip + "'")
        print "Checking to see if I have enough info.....",
        if mip != 'NA':
            ''' First we need to check to see if it's 14.2 AP for new
                passwords. Otherwise use the old passwords '''
            if '14' in mobject.swVersion:
                command_c = (femtostatus_script + ' ' + 
                        fgwip + ' ' + mip + ' ' + eeker.fgwpw + ' ' + 
                        eeker.apnopw + ' ' + eeker.apnapw + ' ' + 
                        eeker.femtostatus_timeout)
                command_r = (reboot_script + ' ' + fgwip + ' ' + mip + ' ' + 
                        eeker.fgwpw + ' ' + eeker.apnopw + ' ' + 
                        eeker.apnapw + ' ' + eeker.femtostatus_timeout)
                logging.debug(myfunc + '\t' +
                "Detected '14' in swVersion field, using new pwds")
            else:
                command_c = (femtostatus_script + ' ' + 
                        fgwip + ' ' + mip + ' ' + eeker.fgwpw + ' ' + 
                        eeker.apopw + ' ' + eeker.apapw + ' ' + 
                        eeker.femtostatus_timeout)
                command_r = (reboot_script + ' ' + fgwip + ' ' + mip + ' ' + 
                        eeker.fgwpw + ' ' + eeker.apopw + ' ' + 
                        eeker.apapw + ' ' + eeker.femtostatus_timeout)
                logging.debug(myfunc + '\t' +
                    "Did not detect '14' in swVersion field, using old pwds")

            print("\tFirst I'll connect to the AP and check "
                    "it's serial number...")
            try:
                logging.info(myfunc + '\t' + pmConfig.rob + command_c)
                #print command_c
                command_c_output = pmLoaders.runoscommand(command_c)
                re_serial_111 = '(    FSN )(?P<serial>\d*)'
                re_serial_11 = re.compile(re_serial_111)
                for o in command_c_output:
                    match_serial = re.search(re_serial_11,o)
                    if match_serial:
                        scannedser = match_serial.group('serial')
                logging.debug(myfunc + '\t' + 
                    "Detected serial from expect script: " + scannedser)
            except Exception as aoe:
                logging.debug(myfunc + '\t' + 
                    "Exception running checker script: " + str(aoe))
            logging.debug(myfunc + '\t' + 
                "Serial from existing inventory: " + mobject.serial)	
            print("\tI connected to the AP and saw that it "
                    "has serial number:\t" + scannedser)
            print("\tThe serial I have in my database "
                    "for that AP is:\t\t" + mobject.serial)
            if scannedser == mobject.serial:
                print "\tI feel confident in running the reboot command."
                print ""
                try:
                    reboot_areyousure =("\tAre you absolutely sure you "
                                    "want to reboot '" + mobject.bsrName + 
                                    "'? (y/n) ")
                    try:
                        suretoreboot = macrolist.pop()
                    except:
                        suretoreboot = raw_input(reboot_areyousure)
                    if suretoreboot == 'y':
                        logging.info(myfunc + '\t' + pmConfig.rob + command_r)
                        #print command_r
                        output = pmLoaders.runoscommand(command_r)
                        print ""
                        for line in output:
                            print '\t\t\t\t' + line.strip('\n')
                        print ""
                        print "\t\tI sent the reboot command! "
                        print("\t\tIn about 10 minutes refresh BSR "
                            "ipSecIpAddr registrations with command '112'")
                        print("\t\tAfter that you should be "
                            "able to status the AP")
                except Exception as oor:
                    logging.debug(myfunc + '\t' + 
                        "Exception running reboot script: " + str(oor))
            else:
                print "\tSerials do not match, too risky to run reboot command"
        else:
            print "FAILED"
            listy = []
            listy.append(mobject)
            coloredList(listy,'metro','NA',eeker.db_femtos,True)
            print ""
            print("That AP appears to be offline. I have no "
                "ipSecIPAddr to try and connect to.")
    except Exception as hoho:
        logging.debug(myfunc + '\t' + 
            "Exception running reboot function: " + str(hoho))
        print "Something went wrong. Are you sure you entered a real commonID?"
    
def querybuilder():
    funcname = str(pmLoaders.giveupthefunc())
    print("\t\t This function allows you to build custom queries " + 
            "on the database. You'll be asked a series of questions regarding the " +
            "Metrocell display fields. You'll eithe provide a 'yes/no' answer or " + 
            "provide a regular expression pattern for the specific field.")
    print("")
    print("\t\tTIPS:")
    print("\t\t\tTo match everything except swVersion '14.02' use the regular expression 'BSR-(?!14.02).*'")
    print("\t\t\tTo match only 'Monitored' AP's use '^monitored'")
    print("\t\t\tWildcard character is '.*' EXAMPLE: '.*visa.*' to show anything with 'visa' in the name.")
    print("")
    print("\t\tProvide '+++' to any question to exit the query builder.")
    print("")
    field_bsrName = {'displayname':'bsrName',
                        'fieldname':'bsrName',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_groupName = {'displayname':'groupName',
                        'fieldname':'groupName',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_usecase = {'displayname':'usecase',
                        'fieldname':'usecase',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_ctsname = {'displayname':'ctsEquipName',
                        'fieldname':'ctsname',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_monitoredStatus = {'displayname':'Monitored?',
                        'fieldname':'monitoredStatus',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_ipsecIpAddr = {'displayname':'ipsecIpAddr',
                        'fieldname':'ipsecIpAddr',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': True}
    field_clusterId = {'displayname':'clstr',
                        'fieldname':'clusterId',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_groupId = {'displayname':'grp',
                        'fieldname':'groupId',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_fgw = {'displayname':'fgw',
                        'fieldname':'fgw',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_usid = {'displayname':'usid',
                        'fieldname':'usid',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_swVersion = {'displayname':'swVersion',
                        'fieldname':'swVersion',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_adminStatus = {'displayname':'adminStatus',
                        'fieldname':'adminStatus',
                        'pattern':'',
                        'pattern_re':'',
                        'bool': False}
    field_inalarm = {'displayname':'alarm?',
                        'fieldname':'inalarm',
                        'pattern:':'',
                        'pattern_re':'',
                        'bool': True}

    lod_fields = [field_bsrName,
                            field_groupName,
                            field_usecase,
                            field_ctsname,
                            field_monitoredStatus,
                            field_ipsecIpAddr,
                            field_clusterId,
                            field_groupId,
                            field_fgw,
                            field_usid,
                            field_swVersion,
                            field_adminStatus,
                            field_inalarm]
    # now go through and collect data for the regex pattern fields
    exitflag = False

    for field in lod_fields:
        if not field.get('bool'):
            try:
                field['pattern'] = eeker.macrolist.pop()
            except:
                field['pattern'] = raw_input("\t\t\t Regex pattern for '" + 
                        field.get('displayname') + "' field. (enter for all): ")
            if field.get('pattern') == '+++':
                exitflag = True
                break
            elif field.get('pattern') == '':
                field['pattern'] = '.*'
            try:
                field['pattern_re'] = re.compile(field.get('pattern'),re.IGNORECASE)
            except:
                logging.debug('\t' + funcname +
                    "Error compiling regex for field['displayname']: " +
                    field.get('displayname'))
                field['pattern'] = '.*'

    # Handle the remaining yes/no questions
    print ""
    bool_onlyalarmed = False
    if not exitflag:
        try:
            field_inalarm['pattern'] = eeker.macrolist.pop()
        except:
            field_inalarm['pattern'] = raw_input("\t\tDo you want to only display AP's with alarms? (y/n): ")
        if field_inalarm['pattern'] == '+++':
            exitflag = True
        if field_inalarm['pattern'] == 'y':
            bool_onlyalarmed = True
        else:
            bool_onlyalarmed = False
    bool_onlyoffline = False
    if not exitflag:
        try:
            field_ipsecIpAddr['pattern'] = eeker.macrolist.pop()
        except:
            field_ipsecIpAddr['pattern'] = raw_input("\t\tDo you want to only display AP's that are offline? (y/n): ")
        if field_ipsecIpAddr['pattern'] == '+++':
            exitflag = True
        if field_ipsecIpAddr['pattern'] == 'y':
            bool_onlyoffline = True
        else:
            bool_onlyoffline = False

    # now we have a list of dictionaries with the fields we want and the desired search patterns
    # now build a result list based on the query
    def matches(obj_femto):
        match_groupName = re.search(field_groupName['pattern_re'],obj_femto.groupName)
        match_usecase = re.search(field_usecase['pattern_re'],obj_femto.usecase)
        match_ctsname = re.search(field_ctsname['pattern_re'],obj_femto.ctsname)
        match_monitoredStatus = re.search(field_monitoredStatus['pattern_re'],obj_femto.monitoredStatus)
        # match_ipsecIpAddr = re.search(field_ipsecIpAddr['pattern_re'],obj_femto.ipsecIpAddr)
        match_clusterId = re.search(field_clusterId['pattern_re'],obj_femto.clusterId)
        match_groupId = re.search(field_groupId['pattern_re'],obj_femto.groupId)
        match_fgw = re.search(field_fgw['pattern_re'],obj_femto.fgw)
        match_usid = re.search(field_usid['pattern_re'],obj_femto.usid)
        match_swVersion = re.search(field_swVersion['pattern_re'],obj_femto.swVersion)
        match_adminStatus = re.search(field_adminStatus['pattern_re'],obj_femto.adminStatus)
        match_alarmfield = False
        if bool_onlyalarmed:
            if obj_femto.inalarm:
                match_alarmfield = True
            else:
                match_alarmfield = False
        else:
            match_alarmfield = True
        if bool_onlyoffline:
            if obj_femto.ipsecIpAddr == 'NA':
                match_ipsecfield = True
            else:
                match_ipsecfield = False
        else:
            match_ipsecfield = True
        if (match_groupName and
                match_usecase and
                match_ctsname and
                match_monitoredStatus and 
                match_clusterId and
                match_groupId and
                match_fgw and
                match_usid and
                match_swVersion and
                match_adminStatus
                ):
            match_nonbools = True
        else:
            match_nonbools = False
        if match_alarmfield and match_nonbools and match_ipsecfield:
            return True
        else:
            return False

    if not exitflag:
        eeker.dblock.acquire()
        t_resultlist = []
        for ap in eeker.db_femtos:
            if matches(ap):
                t_resultlist.append(ap)
        coloredList(t_resultlist,
                'metro',
                'NA',
                eeker.db_femtos,
                True)
        try:
            try:
                wantrunonwholegroup = eeker.macrolist.pop()
            except:
                wantrunwholegroup_string = ("Do you want to "
                            "run status check on this entire result list?? (y/n) ")
                wantrunonwholegroup = raw_input(wantrunwholegroup_string)
            if wantrunonwholegroup == 'y':
                # now call the pull_console_dump function on the group
                # send the deepcopied list to pull_ap_console_dump()
                pmLoaders.pull_ap_console_dump(t_resultlist)
        except Exception as e:
            logging.critical(funcname + '\t' + 
                    "Got an exception trying to do bulk operation: " + str(e))
        eeker.dblock.release()
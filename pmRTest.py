import os, datetime,time,sys

def print_help():
    print "This is a regression testing script for testing functionality of the PowerMenu (rendicott@gmail.com)"
    print "Usage: python pmRTest.py FOODFILE FGWPW APOPW APAPW APNOPW APANPW"
    print ""
    print "Example: python pmRTest.py 2014-12-08-09-32-27Powermenu-Food-CTS.csv passw0rd1 passw03d2 p4ssw0rd3 password4 password5"


#process arguments
if len(sys.argv) < 5:
    print_help()
    sys.exit()

try:
    foodfile = sys.argv[1]
except:
    print "Exception processing argument."
    foodfile = '2014-12-08-09-32-27Powermenu-Food-CTS.csv'
try:
    fgwpw = sys.argv[2]
except:
    sys.exit()
try:
    apopw = sys.argv[3]
except:
    sys.exit()
try:
    apapw = sys.argv[4]
except:
    sys.exit()
try:
    apnopw = sys.argv[5]
except:
    sys.exit()
try:
    apnapw = sys.argv[6]
except:
    sys.exit()


pws = (fgwpw,apopw,apapw,apnopw,apnapw)
    
s0 = 'rm *.pkl'
s01 = 'rm *.csv'
s1 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "c,10,9+01,9+02,8+BRHMALM02203,8+13+BRHMALM02203,m,7+111,111,+++" -l pm_s1.log' % pws
s2 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "5+,4+BRHMALM02203,n,3+visa,3+29+151,s,201-19,g,201-19,y,n,b,LSANCLM30328-LSANCLM30338-LSANCLM30327,112,y,c,12,c,10,i,+++" -l pm_s2.log' % pws
s3 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "c,10,n,9+01,9+02,9+03,e+3,rendicott@gmail.com,n,113,+++" -l pm_s3.log' % pws
s4 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "c,12,u,n,n,y,y,y,rendicott@gmail.com,y,y,+++" -l pm_s4.log' % pws
s5 = 'rm *.pkl'
s50 = 'rm *.csv'
s51 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "c,12,5+a,+++" -l pm_s5.log' % pws

#need to make a new tuple to add foodfile
tfoodfile = (foodfile,)
pwsf = pws + tfoodfile
s6 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "c,12,5+a,+++" -l pm_s6.log' % pwsf

s7 = 'python pm.py -d -1 --fgwpw %s --apopw %s --apapw %s --apnopw %s --apnapw %s -m "f,3+dodo,m,9+01" -l pm_s7.log' % pwsf

cmdlist = []
cmdlist.append(s0)
cmdlist.append(s01)
cmdlist.append(s1)
cmdlist.append(s2)
cmdlist.append(s3)
cmdlist.append(s4)
cmdlist.append(s5)
cmdlist.append(s50)
cmdlist.append(s51)
cmdlist.append(s6)
cmdlist.append(s7)

timestart = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
timings = []

for o in cmdlist:
    timings.append(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
    try:
        print ""
        print "Running command: " + o
        os.system(o)
        timings.append(datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
        print ""
    except:
        print "Exception with " + o
        
timeend = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

print "Start time: \t\t" + str(timestart)
print "End time: \t\t" + str(timeend)

print ""
print "Other timings:"
for i in timings:
    print i
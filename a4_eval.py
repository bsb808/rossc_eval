#!/usr/bin/env python 
import os
import logging
import subprocess
import time
import signal

# local
import students
reload(students)
import hwutils
reload(hwutils)

global REPONAME, HW
HW='a4'
REPONAME='rossc_%s'%HW

# Where to put the results
hwdir='/home/bsb/rossc/rossc_assign_eval'
if not os.path.exists(os.path.join(hwdir,HW)):
    os.mkdir(os.path.join(hwdir,HW))

# Where all the student repositories are
devwd='./assign_workingcopies'

#logging.basicConfig(filename='example.log',level=logging.DEBUG)

# Get root logger
logger = logging.getLogger()
#Have to set the root logger level, it defaults to logging.WARNING
logger.setLevel(logging.NOTSET)
fstr="%(levelname)s: %(message)s"
formatter = logging.Formatter(fstr)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# tell the handler to use this format
console.setFormatter(formatter)
logger.addHandler(console)

import collections
summary = collections.OrderedDict()

for s in  students.STUDS:
    # Setup logger
    # Remove all old handlers
    #for hdlr in logger.handlers[:]:  # remove all old handlers
    #    hdlr.stream.close()
    #    logger.removeHandler(hdlr)
    # Setup file handler for logging
    logfile = os.path.join(hwdir,HW,'%s_%s.log'%(HW,s))
    print "Logging to <%s>"%logfile
    fileh = logging.FileHandler(logfile,'w')
    fileh.setFormatter(formatter)
    fileh.setLevel(logging.INFO)
    # Add file handler
    logger.addHandler(fileh)


    repo = os.path.join(devwd,s,REPONAME)
    logging.info("")
    logging.info("-------------START----------------------")
    logging.info("----------------------------------------")
    logging.info("Check for directory <<%s>>"%s)

    test=os.path.exists(repo)
    logging.info("Does repo exists at %s? %s"%(repo,str(test)))

    successes = 0
    failures = 0

    if test:
        successes += 1
        ilist_all = []  # master list of all required images
        logging.info("Contents of repository:")
        ds,fs = hwutils.walk(repo)
        hwutils.callCmd('tree %s'%repo)

        logging.info("")
        logging.info("Assignment: ROS plumbing - connecting nodes via topics")
        logging.info("Exercise: Setup Git repository and make it a ROS package")
        flist = ['package.xml','CMakeLists.txt']
        y,n = hwutils.checkFiles(repo,flist)
        successes += y
        failures += n


        logging.info("Exercise: Plumbing the system")
        flist = ['launch/course_control.launch']
        ilist = ['images/rosgraph.png']
        y,n = hwutils.checkFiles(repo,flist+ilist)
        successes += y
        failures += n

        fname = os.path.join(repo,flist[0])
        tstrs = [ ['remap','odometry/nav','nav_odom'],
                  ['remap','cmd_course','cmd_vel'],
                  ['remap','cmd_drive','cmd_drive']]
        for ts in tstrs:
            if hwutils.testTextStrings(fname,ts):
                successes += 1
            else: 
                failures += 1

        pdffile = os.path.join(hwdir,HW,'%s_%s_images.pdf'%(HW,s))
        hwutils.images2pdf(repo,ilist,pdffile)

            
    else:
        logging.info("Terminating testing - can't test without the repository")
        failures += 1

    logging.info("")
    logging.info("-- SUMMARY --")
    msg = "Number of tests executed: %d"%(successes+failures)
    msg += "\n\t Successes: %d"%successes
    msg += "\n\t Failures: %d"%failures
    if failures == 0:
        logging.info(msg)
    else:
        logging.warn(msg)

    logging.info("****************END*********************")
    logging.info("End of testing for <%s>"%HW)
    #logging.shutdown()

    summary[s] = [successes,failures]

    logger.removeHandler(fileh)

# Write summary log file
sumfile = os.path.join(hwdir,HW,'summary.log')
sumf = open(sumfile,'w')
msg = "User, \tSuccesses, \tFailures\n"
sumf.write(msg)
for k in summary.keys():
    sf = summary[k]
    msg = "%s, \t%d, \t%d\n"%(k,sf[0],sf[1])
    sumf.write(msg)
sumf.close()

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
HW='a1'
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
        logging.info("Contents of repository:")
        ds,fs = hwutils.walk(repo)
        hwutils.callCmd('tree %s'%repo)

        logging.info("")
        logging.info("Assignment: Introduction to Linux and Git")
        flist = ['sandbox','sandbox/dir1','sandbox/dir1/file1.txt',
                 'sandbox/dir2','sandbox/dir2/file2.txt','sandbox/commands.txt']
        y,n = hwutils.checkFiles(repo,flist)
        successes += y
        failures += n
        hwutils.catFiles(repo,['sandbox/commands.txt'])

        logging.info("")
        flist = ['playpen','playpen/folder1','playpen/folder1/file1.txt',
                 'playpen/folder2','playpen/folder2/file2.txt','playpen/play.txt']
        y,n = hwutils.checkFiles(repo,flist)
        successes += y
        failures += n

        logging.info("")
        logging.info("Assignment: Piloting a Turtle")
        flist = ['scripts/turtleletter.sh']
        y,n = hwutils.checkFiles(repo,flist)
        successes += y
        failures += n
        hwutils.catFiles(repo,flist)

        # Get a screen capture of turtle results
        if y > 0:
            logging.info("Attempting to run bash script <%s>"%flist[0])
            outf = os.path.join(hwdir,HW,'turtleletter_%s.png'%s)
            logging.info("Saving resulting image as <%s>"%outf)
            rcore = subprocess.Popen('roscore', shell=True, 
                                     stderr=subprocess.STDOUT,
                                     preexec_fn=os.setsid)
            time.sleep(2.0)
            tsim = subprocess.Popen(['rosrun turtlesim turtlesim_node'],
                                      shell=True, stderr=subprocess.STDOUT,
                                    preexec_fn=os.setsid)
            time.sleep(1.0)
            SDIR = os.path.join(repo,'scripts')
            proc = subprocess.Popen(['bash','turtleletter.sh'],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    preexec_fn=os.setsid,
                                    cwd=SDIR)
            (out,err) = proc.communicate()
            print "out: ",out
            print "err: ",err

            proc = subprocess.Popen(['gnome-screenshot','-w','-f',outf],
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    cwd=SDIR)
            (out,err) = proc.communicate()
            print "out: ",out
            print "err: ",err
            
            try:
                os.killpg(os.getpgid(tsim.pid),signal.SIGTERM)
            except:
                pass
            try:
                tsim.terminate()
            except:
                pass
            try:
                os.killpg(os.getpgid(rcore.pid),signal.SIGTERM)
            except:
                pass
            try: 
                rcore.terminate()
            except:
                pass
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

    logger.removeHandler(fileh)


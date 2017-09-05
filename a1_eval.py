#!/usr/bin/env python 
import os
import logging

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
devwd='/home/bsb/rossc/assignments'

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
    if test:
        logging.info("Contents of repository:")
        ds,fs = hwutils.walk(repo)
        hwutils.callCmd('tree %s'%repo)

        logging.info("")
        logging.info("Exercise 2: Check existence of directories and files")
        flist = ['sandbox','sandbox/dir1','sandbox/dir1/file1.txt',
                 'sandbox/dir2','sandbox/dir2/file2.txt','sandbox/commands.txt']
        hwutils.checkFiles(repo,flist)
        hwutils.catFiles(repo,['sandbox/commands.txt']);
        
        logging.info("")
        logging.info("Exercise 3: Check existence of more directories and files")
        flist = ['playpen','playpen/folder1','playpen/folder1/file1.txt',
                 'playpen/folder2','playpen/folder2/file2.txt','playpen/play.txt']
        hwutils.checkFiles(repo,flist)
        
        logging.info("")
        logging.info("Exercise 4: Check existence of tree.out")
        flist = ['tree.out']
        hwutils.checkFiles(repo,flist)
        hwutils.catFiles(repo,['tree.out']);

    else:
        logging.info("Terminating testing - can't test without the repository")

    logging.info("****************END*********************")
    logging.info("End of testing for <%s>"%HW)
    #logging.shutdown()

    logger.removeHandler(fileh)


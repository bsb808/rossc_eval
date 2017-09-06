#!/usr/bin/env python 
import os
import subprocess

# Include the common list of repos to operate upon
import students
reload(students)



#DEVWD='/home/bsb/rossc/assignments'
DEVWD='./assign_workingcopies'
#for REPO in "${REPOS[@]}"

for s in students.STUDS:
    print "Student: <%s>"%s
    DIR = os.path.join(DEVWD,s)
    if not os.path.exists(DIR):
        print("Missing student directory for <%s> - making it"%s)
        os.makedirs(DIR)
    NN=2
    for N in range(1,NN):
	R="rossc_a%d"%N
	DIRR=os.path.join(DIR,R)
        
        if os.path.exists(DIRR):
	    print "Pulling from remote <%s>"%R
	    p=subprocess.Popen(['git','pull','origin','master'],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=DIRR)
            (out,err) = p.communicate()
            print "out: ",out
            print "err: ",err

	else:
	    REPO=("git@github.com:%s/%s.git"%(s,R))
	    print("Cloning <%s> into <%s>"%(REPO,DIR))
	    p=subprocess.Popen(['git','clone',REPO],
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               cwd=DIR)
            (out,err) = p.communicate()
            print "out: ",out
            print "err: ",err
            

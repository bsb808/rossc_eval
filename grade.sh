#!/bin/bash

# Clone and pull - change the file to change which repos
GRADING='/home/bsb/rossc/rossc_eval'
cd "${GRADING}"
./clone_repos.py

RESULTS='/home/bsb/rossc/rossc_assign_eval'
# a1
cd "${GRADING}"
./a1_eval.py
cd "${RESULTS}"
git add ./a1/*.*


cd "${GRADING}"
./a2_eval.py
cd "${RESULTS}"
git add ./a2/*.*

cd "${GRADING}"
./a3_eval.py
cd "${RESULTS}"
git add ./a3/*.*

cd "${GRADING}"
./a4_eval.py
cd "${RESULTS}"
git add ./a4/*.*


# Commit and push
cd "${RESULTS}"
NOW=`date +%Y.%m.%d-%H:%M:%S`
cmsg="Latest auto commit: ${NOW}"
echo $cmsg
#git status
git commit -a -m "${cmsg}"
git push origin master

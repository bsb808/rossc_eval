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

# Commit and push
cd "${RESULTS}"
NOW=`date +%Y.%m.%d-%H:%M:%S`
echo ${NOW}
git status
git commit -a -m ${NOW}
git push origin master

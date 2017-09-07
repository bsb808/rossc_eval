# Commit and push
RESULTS='/home/bsb/rossc/rossc_assign_eval'

cd "${RESULTS}"
NOW=`date +%Y.%m.%d-%H:%M:%S`
cmsg="Latest auto commit: ${NOW}"
echo $cmsg
#git status
git commit -a -m "${cmsg}"
git push origin master

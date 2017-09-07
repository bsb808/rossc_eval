import hwutils as hw
import logging

teststrs = ['remap','odometry/nav','nav_dom'
fname = '/home/bsb/catkin_ws/src/rossc_a4/launch/course_control.launch'
f = open(fname)
result = False
for line in f:
    tests = []
    for t in teststrs:
        tests.append(t in line)
    if all(tests):
        result = True

print result
    

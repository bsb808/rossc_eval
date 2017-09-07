import numpy as np
fname = '/home/bsb/catkin_ws/src/rossc_a5/timer.out'
f = open(fname)
times = []
for line in f:
    if 'data' in line:
        aa = line.split()
        print aa
        times.append(float(aa[1]))

best = max(np.array(times))
print "Best time = %.3f s"%best


    

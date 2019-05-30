#!/usr/bin/env python

import sys
import rospy
from lab2.srv import *

def jint_control_client(j1,j2,j3,time):
    rospy.wait_for_service('jint_control_srv')
    try:
        jint_control_srv = rospy.ServiceProxy('jint_control_srv', jint)
        resp1 = jint_control_srv(j1,j2,j3,time)
        return resp1.status
    except rospy.ServiceException, e:
	print "Service call failed: %s"%e

def usage():
    return "%s [x y]"%sys.argv[0]

    if len(sys.argv) == 6:
        j1 = float(sys.argv[1])
        j2 = float(sys.argv[2])
        j3 = float(sys.argv[3])
        time = float(sys.argv[4])

    else:
        print usage()
        sys.exit(1)
    print "Requesting params: %s %s %s %s %s"%(j1,j2,j3,time)
    print "%s, %s, %s, %s, %s -> %s"%(j1,j2,j3,time, jint_client(j1,j2,j3,time))

#!/usr/bin/env python

import sys
import rospy
from lab2.srv import *
from math import *
import numpy

def ikin_square():
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_control_srv = rospy.ServiceProxy('oint_control_srv', Oint)
	sqr = ((-1,-1,2), (-1,2,2), (2,2,2),(2,-1,2))
        resp1 = oint_control_srv(sqr[0][0], sqr[0][1], sqr[0][2], sqr[1][0], sqr[1][1], sqr[1][2], 10)
        resp2 = oint_control_srv(sqr[1][0], sqr[1][1], sqr[1][2], sqr[2][0], sqr[2][1], sqr[2][2], 10)
        resp3 = oint_control_srv(sqr[2][0], sqr[2][1], sqr[2][2], sqr[3][0], sqr[3][1], sqr[3][2], 10)
        resp4 = oint_control_srv(sqr[3][0], sqr[3][1], sqr[3][2], sqr[0][0], sqr[0][1], sqr[0][2], 10)
        return "Narysowano kwadrat"
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def ikin_ellipse():
    rospy.wait_for_service('oint_control_srv')
    try:
        oint_control_srv = rospy.ServiceProxy('oint_control_srv', Oint)
        prev_point = (3,0,2)
        for theta in numpy.arange(0, 2*pi, pi/40):
	    point = (3*cos(theta), 2*sin(theta), 2)
	    resp = oint_control_srv(prev_point[0], prev_point[1], prev_point[2], point[0], point[1], point[2], 0.2)
	    prev_point = point
	return "Narysowano elipse"
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


if __name__ == "__main__":
    x = int(sys.argv[1])
    if x==0:
	ikin_square()
    elif x==1:
	ikin_ellipse()
    print(x)

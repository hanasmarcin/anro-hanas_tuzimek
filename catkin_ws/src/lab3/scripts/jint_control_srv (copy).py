#!/usr/bin/env python

import beginner_tutorials.srv
import lab2.srv
import lab2.srv
from lab2.srv import *
import rospy

def handle_jint(req):
    print "Returning [%s + %s + %s]"%(req.a, req.b, req.c)
    return JintResponse(req.a + req.b + req.c)

def jint_server():
    rospy.init_node('jint')
    s = rospy.Service('jint_control_srv', Jint, handle_jint)
    print "Ready to INTERPOLATE."
    rospy.spin()

if __name__ == "__main__":
    jint_server()

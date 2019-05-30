#!/usr/bin/env python

import rospy
from lab2.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from math import *
from geometry_msgs.msg import PoseStamped
from tf.transformations import *
import os
import json

class Node(object):
    def __init__(self):
	self.th2_prev=0
	self.th3_prev=0

	rospy.Subscriber('/oint', PoseStamped, self.transform_callback)
    	self.pub = rospy.Publisher('joint_states',JointState,queue_size=10)


    def transform_callback(self, data):
    	px = data.pose.position.x
  	py = data.pose.position.y
   	pz = data.pose.position.z
 
    	r = quaternion_matrix([data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])
    	a1 = 3
    	a2 = 2
    #th1 = atan2(py, px)
    #th2 = asin(-pz/a)
    #th3 = asin(-r[2][0])-th2
    #th3_2 = acos(r[0][0]*cos(th1) + r[1][0]*sin(th1)) - th2

    	th1 = atan(py/px)
    	k2 = pz
    	k1 = px*cos(th1) + py*sin(th1)

    	th2=-2*atan((2*a1*k2 - sqrt(- a1**4 + 2*a1**2*a2**2 + 2*a1**2*k1**2 + 2*a1**2*k2**2 - a2**4 + 2*a2**2*k1**2 + 2*a2**2*k2**2 - k1**4 - 2*k1**2*k2**2 -k2**4))/(a1**2 + 2*a1*k1 - a2**2 + k1**2 + k2**2))

    	th2_2=-2*atan((2*a1*k2 + sqrt(- a1**4 + 2*a1**2*a2**2 + 2*a1**2*k1**2 + 2*a1**2*k2**2 - a2**4 + 2*a2**2*k1**2 + 2*a2**2*k2**2 - k1**4 - 2*k1**2*k2**2 - k2**4))/(a1**2 + 2*a1*k1 - a2**2 + k1**2 + k2**2))
 

    	th3=-2*atan(sqrt((- a1**2 + 2*a1*a2 - a2**2 + k1**2 + k2**2)*(a1**2 + 2*a1*a2 + a2**2 - k1**2 - k2**2))/(- a1**2 + 2*a1*a2 - a2**2 + k1**2 + k2**2))

    	th3_2=2*atan(sqrt((- a1**2 + 2*a1*a2 - a2**2 + k1**2 + k2**2)*(a1**2 + 2*a1*a2 + a2**2 - k1**2 - k2**2))/(- a1**2 + 2*a1*a2 - a2**2 + k1**2 + k2**2))

	print(str(th2)+" | "+str(th2_2))
    	if abs(self.th2_prev-th2) > abs(self.th2_prev-th2_2) and abs(self.th2_prev-th2)<6.28:
            th2 = th2_2
	    th3 = th3_2
   

    #if abs(th2_2) > abs(th2):
    	self.th2_prev=th2
	self.th3_prev=th3

    #if abs(th3_2) > abs(th3):

    #print(str(th3)+str(th3_2))
    #if req.time <= 0 or not 0 <= req.j1 <= 6 or not -3 <= req.j2 <= 3 or not -1 <= req.j3 <= 1:
    #    return False

    	hello_str = JointState()
    	hello_str.header = Header()
    	hello_str.header.stamp = rospy.Time.now()
    	hello_str.name = ['1_na_boki', '1_przod_tyl', 'czlon_z_2']
    	hello_str.position = [th_0[0]+th1, th_0[1]+th2, th_0[2]+th3]
    	hello_str.velocity = []
    	hello_str.effort = []
    	self.pub.publish(hello_str)


    	return (str(th1)+" "+str(th2)+" "+str(th3))

th_0 = []

if __name__ == "__main__":
    rospy.init_node('ikin_srv')
    
    th2_prev=0
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        params = json.loads(file.read())
        matrices = {}
        for key in params.keys():
            _, _, _, th0 = params[key]
            th_0.append(float(th0))
    my_node = Node()
    rospy.spin()

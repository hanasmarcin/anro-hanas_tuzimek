#!/usr/bin/env python

import rospy
from lab2.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math


freq = 50


def handle_interpolation(req):
    if req.time <= 0 or not 0 <= req.j1 <= 100 or not 0 <= req.j2 <= 100 or not 0 <= req.j3 <= 100:
        return False

	
    start_pos = [0, 0, 0]
    end_pos = [req.j1, req.j2, req.j3]


    for k in range(0, int(freq*req.time)+1):
	current_pos = []
	for i in range(0, 3):
	    current_pos.append(start_pos[i]+(end_pos[i]-start_pos[i])/(freq*req.time)*k)

	print(current_pos) 
	rate = rospy.Rate(50) # 50hz
        hello_str = JointState()
        hello_str.header = Header()
        hello_str.header.stamp = rospy.Time.now()
        hello_str.name = ['1_na_boki', '1_przod_tyl', 'czlon_z_2']
        hello_str.position = [current_pos[0], current_pos[1], current_pos[2]]
        hello_str.velocity = []
        hello_str.effort = []
        pub.publish(hello_str)
        rate.sleep()


    current_time = 0
    return (str(req.j1)+" "+str(req.j2)+" "+str(req.j3))


if __name__ == "__main__":
    rospy.init_node('int_srv')
    pub = rospy.Publisher('joint_states',JointState,queue_size=10)
    s = rospy.Service('jint_control_srv', Jint, handle_interpolation)
    rospy.spin()

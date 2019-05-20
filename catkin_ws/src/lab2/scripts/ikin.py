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

freq = 50

th_0 = []


def transform_callback(data):
    px = data.pose.position.x
    py = data.pose.position.y
    pz = data.pose.position.z
 
    r = quaternion_matrix([data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w])
    a = 0.5

    th1 = atan2(py, px)
    th2 = asin(-pz/a)
    th3 = asin(-r[2][0])-th2
    th3_2 = acos(r[0][0]*cos(th1) + r[1][0]*sin(th1)) - th2
    if abs(th3_2) > abs(th3):
	th3 = th3_2
    print(str(th3)+str(th3_2))
    #if req.time <= 0 or not 0 <= req.j1 <= 6 or not -3 <= req.j2 <= 3 or not -1 <= req.j3 <= 1:
    #    return False

    hello_str = JointState()
    hello_str.header = Header()
    hello_str.header.stamp = rospy.Time.now()
    hello_str.name = ['1_na_boki', '1_przod_tyl', 'czlon_z_2']
    hello_str.position = [th_0[0]+th1, th_0[1]+th2, th_0[2]+th3]
    hello_str.velocity = []
    hello_str.effort = []
    pub.publish(hello_str)


    current_time = 0
    return (str(th1)+" "+str(th2)+" "+str(th3))


if __name__ == "__main__":
    rospy.init_node('ikin_srv')
    rospy.Subscriber('/oint', PoseStamped, transform_callback)
    pub = rospy.Publisher('joint_states',JointState,queue_size=10)
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        params = json.loads(file.read())
        matrices = {}
        for key in params.keys():
            _, _, _, th0 = params[key]
            th_0.append(float(th0))
    rospy.spin()

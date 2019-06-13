#!/usr/bin/env python

import rospy
from lab2.srv import Jint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math
import os
import json
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped


freq = 50

xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
def handle_interpolation(req):
    if req.time <= 0 or not 0 <= req.j1 <= 100 or not 0 <= req.j2 <= 100 or not 0 <= req.j3 <= 100:
        return False

	
    start_pos = [0, 0, 0]
    end_pos = [req.j1, req.j2, req.j3]


    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        params = json.loads(file.read())


    for k in range(0, int(freq*req.time)+1):
	pos_change = []
	for i in range(0, 3):
	    pos_change.append((end_pos[i]-start_pos[i])/(freq*req.time)*k)

	mainMatrix = translation_matrix((0, 0, 0))
    
	matrices = {}
        for key in params.keys():
            a, d, al, th = params[key]
            al, a, d, th = float(al), float(a), float(d), float(th)
            tz = translation_matrix((0, 0, d))
            rz = rotation_matrix(th+pos_change[int(key)-1], zaxis)
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(al, xaxis)
            matrices[key] = concatenate_matrices(tx, rx, tz, rz)
            
        for key in sorted(params.keys()):
	    mainMatrix = concatenate_matrices(mainMatrix,matrices[key])
 

        x , y , z = translation_from_matrix(mainMatrix)
    
        robot_pose = PoseStamped()
        robot_pose.header.frame_id = "base_link"
        robot_pose.header.stamp = rospy.Time.now()
        robot_pose.pose.position.x = x
        robot_pose.pose.position.y = y
        robot_pose.pose.position.z = z
    
        xq, yq, zq, wq = quaternion_from_matrix(mainMatrix)

        robot_pose.pose.orientation.x = xq
        robot_pose.pose.orientation.y = yq
        robot_pose.pose.orientation.z = zq
        robot_pose.pose.orientation.w = wq
	rate = rospy.Rate(50) # 50hz
        pub.publish(robot_pose)
        rate.sleep()

    current_time = 0
    return (str(req.j1)+" "+str(req.j2)+" "+str(req.j3))


if __name__ == "__main__":
    rospy.init_node('int_srv')
    pub = rospy.Publisher('oint',PoseStamped, queue_size=10)
    s = rospy.Service('oint_control_srv', Jint, handle_interpolation)
    rospy.spin()

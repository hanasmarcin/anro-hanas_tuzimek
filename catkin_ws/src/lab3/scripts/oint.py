#!/usr/bin/env python

import rospy
from lab2.srv import Oint
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from math import *
import os
import json
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped
from nav_msgs.msg import Path

class Oint_node(object):
    def __init__(self):
        self.freq = 50
	self.pub = rospy.Publisher('oint', PoseStamped, queue_size=10)
	self.pub_path = rospy.Publisher('oint_path', Path, queue_size=10)
        self.s = rospy.Service('oint_control_srv', Oint, self.handle_interpolation)
	self.path = Path()

        
    def handle_interpolation(self, req):
	print(sqrt(req.xk**2 + req.yk**2 + req.zk**2))
	if not (1<=sqrt(req.x0**2 + req.y0**2 + req.z0**2)<=5 and 1<=sqrt(req.xk**2 + req.yk**2 + req.zk**2)<=5):
	    return "Zle dane punktow"

        start_pos = [req.x0, req.y0, req.z0]
        end_pos = [req.xk, req.yk, req.zk]


        for k in range(0, int(self.freq*req.time)+1):
	    pos_change = []
	    for i in range(0, 3):
	        pos_change.append((end_pos[i]-start_pos[i])/(self.freq*req.time)*k)
           
    
            robot_pose = PoseStamped()
            robot_pose.header.frame_id = "base_link"
            robot_pose.header.stamp = rospy.Time.now()
            robot_pose.pose.position.x = start_pos[0]+pos_change[0]
            robot_pose.pose.position.y = start_pos[1]+pos_change[1]
            robot_pose.pose.position.z = start_pos[2]+pos_change[2]

            robot_pose.pose.orientation.x = 0
            robot_pose.pose.orientation.y = 0
            robot_pose.pose.orientation.z = 0
            robot_pose.pose.orientation.w = 0

	    self.path.poses.append(robot_pose)
            self.path.header.frame_id = "base_link"
            self.path.header.stamp = rospy.Time.now()
	    self.pub_path.publish(self.path)
	    rate = rospy.Rate(50) # 50hz
            self.pub.publish(robot_pose)
            rate.sleep()

        current_time = 0
        return "yay"


if __name__ == "__main__":
    rospy.init_node('int_srv')
    my_node = Oint_node()
    rospy.spin()

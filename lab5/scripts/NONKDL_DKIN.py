#! /usr/bin/python
import rospy
import json
import os
from sensor_msgs.msg import *
from tf.transformations import *
from visualization_msgs.msg import Marker
from geometry_msgs.msg import PoseStamped

xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)
with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
    params = json.loads(file.read())
    print(params)

def callback(data):
    mainMatrix = translation_matrix((0, 0, 0))
    print(data)
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        params = json.loads(file.read())
	matrices = {}
        for key in params.keys():
            a, d, al, th = params[key]
            al, a, d, th = float(al), float(a), float(d), float(th)
            tz = translation_matrix((0, 0, d))
            rz = rotation_matrix(th+data.position[int(key)-1], zaxis)
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

    publisher.publish(robot_pose)


def nonkdl_listener():
    rospy.init_node('NONKDL_DKIN', anonymous = False)
    # publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    rospy.Subscriber("joint_states", JointState , callback)

    rospy.spin()

if __name__ == '__main__':
    json_file = {}
    t_list = {}
    publisher = rospy.Publisher('n_k_axes', PoseStamped, queue_size=10)

    
    
    # laczenie z modelem
    try:
	    nonkdl_listener()        
    except rospy.ROSInterruptException:
	pass

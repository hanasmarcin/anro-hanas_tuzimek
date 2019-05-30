#! /usr/bin/python
import rospy
import json
import os
from sensor_msgs.msg import *
from geometry_msgs.msg import *
from visualization_msgs.msg import Marker
from tf.transformations import *

pub = rospy.Publisher('poseStamped', PoseStamped , queue_size = 100 )

#marker_pub = rospy.Publisher('visualization_marker', Marker , queue_size = 100 )
xaxis, yaxis, zaxis = (1, 0, 0), (0, 1, 0), (0, 0, 1)

#with open('../config/dhparams.json', 'r') as file:
    #dhparams = json.loads(file.read())


def callback(data):
    poseS = PoseStamped()
    mainMatrix = translation_matrix( (0,0,0) )
    with open(os.path.dirname(os.path.realpath(__file__)) + '/../dh.json', 'r') as file:
        
	params = json.loads(file.read())
        for key in params.keys():
            a, d, al, th = params[key]
            al, a, d, th = float(al), float(a), float(d), float(th)

            tz = translation_matrix((0, 0, d))
            rz = rotation_matrix(th, zaxis)
            tx = translation_matrix((a, 0, 0))
            rx = rotation_matrix(al, xaxis)

            matrix = concatenate_matrices(tz, rz, tx, rx)
	    mainMatrix = concatenate_matrices(mainMatrix,matrix)
    

    x , y , z = translation_from_matrix(mainMatrix)
    
    poseS.header.stamp = rospy.Time.now()
    poseS.header.frame_id = "base_link"
    poseS.pose.position.x = x # x
    poseS.pose.position.y = y # y
    poseS.pose.position.z = z+d # z
    	

    
    xq , yq , zq , wq = quaternion_from_matrix(mainMatrix)	    
    poseS.pose.orientation.x = xq
    poseS.pose.orientation.y = yq
    poseS.pose.orientation.z = zq
    poseS.pose.orientation.w = wq

    pub.publish(poseS)
	
	

def listener():


    rospy.init_node('NONKDL', anonymous=True)

    rospy.Subscriber("joint_states", JointState , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()



if __name__ == '__main__':
    try:
	listener()        
    except rospy.ROSInterruptException:
        pass

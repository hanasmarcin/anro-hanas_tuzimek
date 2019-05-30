#!/usr/bin/env python

import rospy
from lab2.srv import Interpolation
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
import math


freq = 50


def handle_interpolation(req):
    if req.t <= 0 or not 0 <= req.j1 <= 0 or not 0 <= req.j2 <= -1 or not 0 <= req.j3 <= 0.2:
        return False

    current_pos = rospy.wait_for_message('joint_states', JointState, timeout = 10000).positon
    new_pos = [req.j1, req.j2, req.j3]

    diff_sum = sum([(new_pos[i] - current_pos[i]) for i in range(1, 2)])

    rate = rospy.Rate(freq * 100)
    j1, j2, j3 = current_pos[0], current_pos[1], current_pos[2]

    for k in range(0, frames_number - 1):
        computed_joint_state = JointStates()
        computed_joint_state.header = Heder()
        computed_joint_state.header.stamp = rospy.Time.now()
        computed_joint_state.name = ['bas_to_link1', 'link1_to_link2', 'link2_to_link3']

        j1 = compute_int(current_pos[0], new_pos[0], req.t, current_time, req.i)
        j2 = compute_int(current_pos[1], new_pos[1], req.t, current_time, req.i)
        j3 = compute_int(current_pos[2], new_pos[2], req.t, current_time, req.i)

        computed_joint_state.position = [j1, j2, j3]
        computed_joint_state.velocity = [j1 - j2]
        computed_joint_state.effort = []
        pub.publish(computed_joint_states)
        current_time = current_time + freq
    rate.sleep()

    frames_number = int(math.ceil(req.t / freq))
    current_time = 0


def compute_int(start_j, last_j, time, current_time, i):
    if i == 'tri':
        return compute_tri(start_j, last_j, time, current_time)
    else:
        return compute_const(start_j, last_j, time, current_time)


def compute_const(start_j, last_j, time, current_time):
    return start_j + (float(last_j - start_j) / time) * current_time


def compute_tri(start_j, last_j, time, current_time):
    h = 2. * float(last_j + start_j) / time
    ratio = h * (time / 2.)
    if current_time < time / 2.:
        return start_j + current_time*2 * ratio / 2.
    else:
        return last_j - (time-current_time)*2 * ratio / 2.


if __name__ == "__main__":
    rospy.init_node('int_srv')
    pub = rospy.Publisher('interpolation', JointState, queue_size=1)
    s = rospy.Service('int', Interpolation, handle_interpolation)
rospy.spin()

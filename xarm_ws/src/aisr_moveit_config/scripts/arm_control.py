#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
from xarm.wrapper import XArmAPI
from sensor_msgs.msg import JointState
import json
from xarm.wrapper import XArmAPI
import numpy as np
import  time
import sys
import copy
import rospy
import geometry_msgs.msg
from math import *


real_zero_values = [-162.4, 68,114,58,194]  #模型中关节为0度时,实体关节的角度
real_init_values = [-168, 68, 114, 58, 194, 54.5, -26] #实体初始角度
# real_zero_values = [-2.8344,1.4573,1.9897,1.0123,3.3859]  #模型中关节为0度时,实体关节的弧度
# real_init_values = [-2.9323,1.1868,1.9897,1.0123,3.3859,0.9512,-0.4538] #实体初始弧度


class Arm(object):
    def __init__(self):
        super(Arm, self).__init__()
        print("================ Setup =================")
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('xarm_move_circle', anonymous=True)

        robot = moveit_commander.RobotCommander()

        scene = moveit_commander.PlanningSceneInterface()

        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

        # We can get the name of the reference frame for this robot:
        planning_frame = move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)


        # We can get the current state of the robot
        print("============ Printing robot state ============")
        print(robot.get_current_state())

        # Set the reference frame of the end effector
        reference_frame = "dummy_link"
        move_group.set_pose_reference_frame(reference_frame)

        # Allow replanning
        move_group.allow_replanning(True)

        # Misc variables
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link



def callback(data):
    joint_position = data.position
    angles = [joint_position[5]*180/3.14159, joint_position[6]*180/3.14159, joint_position[7]*180/3.14159, joint_position[8]*180/3.14159, joint_position[9]*180/3.14159,54.5, -26]
    angles_ = model_values_to_real_values(angles)
    # angles_ = [-168, 68, 114, 58, 179, 54.5, -26]
    print(angles_)
    if arm.connected and arm.state != 4:
        #def set_servo_angle_j(self, angles, speed=None, mvacc=None, mvtime=None, is_radian=None, **kwargs):
       ret = arm.set_servo_angle(angle=angles_, is_radian = False,radius = 60, speed = 10)
       print('moved')  
       time.sleep(0.1)




def real_values_to_model_values(real_values = [-2.8344,1.4573,1.9897,1.0123,3.3859]):
    '''将xarm的实际角度转为模型上的角度, 减去一个初始差值 '''
    model_values = real_values
    model_values[0] -= real_zero_values[0]
    model_values[1] -= real_zero_values[1]
    model_values[1] *=-1  #注意第二个joint与模型转动方向相反
    model_values[2] -= real_zero_values[2]
    model_values[3] -= real_zero_values[3]
    model_values[4] -= real_zero_values[4]
    return model_values

def model_values_to_real_values(model_values = [0,0,0,0,0]):
    ''' 将模型上的角度转为xarm上的角度 加上一个初始差值 '''
    real_values = model_values
    real_values[0] += real_zero_values[0]
    real_values[1] *= -1
    real_values[1] += real_zero_values[1]
    real_values[2] += real_zero_values[2]
    real_values[3] += real_zero_values[3]
    real_values[4] += real_zero_values[4]
    return real_values


if __name__ == '__main__':

    ip = '192.168.1.217'
    arm = XArmAPI(ip)
    arm.motion_enable(enable=True)

    arm.set_mode(0)
    arm.set_state(0)
    time.sleep(0.1)

    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/joint_states', JointState, callback)
    rospy.spin()


    # arm = Arm()
    # print "============ Press `Enter` to execute a movement function ============"
    # raw_input()
    # arm.move_circle()
    # print "============ Motion finished ============"
 
    #arm.disconnect()



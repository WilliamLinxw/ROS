#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
import json
import numpy as np
import  time
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import *
import cv2


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

        group_name = 'xarm7'
        move_group = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

        # We can get the name of the reference frame for this robot:
        planning_frame = move_group.get_planning_frame()
        print("============ Planning frame: %s" % planning_frame)

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print("============ End effector link: %s" % eef_link)

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print("============ Available Planning Groups:", robot.get_group_names())

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
        self.group_names = group_names

    def move_circle_with_cartesian(self):
        xarm7 = self.move_group
        eef_link = self.eef_link
        center = [0.417,-0.241,0.50]
        radius = 0.06
        
        xyz = [center[0] + radius ,center[1],center[2] + 0.03]
        xarm7.set_position_target(xyz, end_effector_link = eef_link)
        print('set position target')
        xarm7.plan()
        xarm7.go(wait=True)
        print('moved')
        rospy.sleep(0.05)

        xarm7.stop()
        xarm7.clear_pose_targets()



        # Create a circle waypoints
        target_pose = xarm7.get_current_pose().pose
        waypoints = []
        theta = np.arange(0, 2*np.pi+0.4, 0.2)
        x = center[0] + radius * np.cos(theta)
        y = center[1] + radius * np.sin(theta)
        for i in range(len(x)):
            target_pose.position.x = x[i]
            target_pose.position.y = y[i]
            target_pose.position.z = center[2]
            waypoints.append(copy.deepcopy(target_pose))
        
        # Compute the Cartesian path
        fraction = 0
        maxtrails = 100
        attempts = 0
        jump_threshold = 0.0
        eef_step = 0.01

        while fraction < 1 and attempts < maxtrails:
            plan, fraction = xarm7.compute_cartesian_path(waypoints, eef_step, jump_threshold)
            attempts += 1

            if attempts % 10 == 0:
                print("Still trying after %d attempts ...", attempts)
        
        # Visualize the plan, where the positions, velocity and accelerations of all joints stored
        print("Plan: ", plan)
        print(type(plan))

        # Execute the plan if it is successfully planned, or print how many trials attempted
        if fraction == 1:
            print("Path computed successfully. Moving the arm.")
            xarm7.execute(plan, wait=True)
        else:
            print("Path planning failed with only %0.6f success after %d attempts.", fraction, maxtrails)
        

        current_pose = xarm7.get_current_pose().pose
        xarm7.set_position_target([current_pose.position.x,current_pose.position.y,current_pose.position.z+0.03], end_effector_link = eef_link)
        print('set position target')
        xarm7.plan()
        xarm7.go(wait=True)
        print('moved')
        rospy.sleep(1)
        xarm7.stop()


    def move_circle(self):
        xarm7 = self.move_group
        eef_link = self.eef_link
        center = [0.417,-0.241,0.50]
        radius = 0.06

        # Go to a desired position where the center of the circle is

        xarm7.set_position_target([center[0] + radius ,center[1],center[2] + 0.03], end_effector_link = eef_link)
        print('set position target')
        xarm7.plan()
        xarm7.go(wait=True)
        print('moved')
        rospy.sleep(0.01)

        xarm7.stop()
        xarm7.clear_pose_targets()

        # Create a circle waypoints
        waypoints = []
        theta = 0
        while theta <= 2 * pi + 0.4:
            X = center[0] + radius * cos(theta)
            Y = center[1] + radius * sin(theta)
            Z = center[2]
            target_position = [X, Y, Z]
            print(target_position)
            theta += 0.2
            xarm7.set_position_target(target_position)
            xarm7.plan()
            xarm7.go(wait=True)
            rospy.sleep(0.01)

        current_pose = xarm7.get_current_pose().pose
        xarm7.set_position_target([current_pose.position.x,current_pose.position.y,current_pose.position.z+0.03], end_effector_link = eef_link)
        print('set position target')
        xarm7.plan()
        xarm7.go(wait=True)
        print('moved')
        rospy.sleep(1)
        xarm7.stop()




    def get_word_strokes(self):
        word_strokes = []
        with open('./fu.json') as f:
            res = f.read()
            res = json.loads(res)
            medians = np.array(res['medians'])
            for s in medians:
                word_strokes.append(np.array(s))
        return word_strokes


    def get_arm_strokes(self,words_strokes,center_point):
        center_x,center_y,center_z = center_point[0],center_point[1],center_point[2]
            

        w = 0.05
        dst = np.float32([[center_x-w, center_y+w], 
                        [center_x+w, center_y+w],
                        [center_x+w, center_y-w]
                        ])
        src = np.float32([[0, 0], [0,1024], [1024, 1024]])
        T_img2arm = cv2.getAffineTransform(src, dst)

        arm_strokes = []
        for word_id in range(0, len(words_strokes)):
            word = words_strokes[word_id]
            new_word = []
            for stroke in word:
                stroke_ = stroke.reshape([-1, 2])
                ones_ = np.ones([len(stroke_), 1])
                stroke_ = np.hstack([stroke_, ones_]).T
                arm_stroke_ = np.matmul(
                    T_img2arm, stroke_).T.reshape([-1, 2])
                x_y = np.array(arm_stroke_).reshape(-1,2)
                z = np.ones((len(x_y),1)) * center_point[2]
                x_y_z = np.hstack([x_y,z])
                new_word.append(x_y_z)
            arm_strokes.append(new_word)
        return arm_strokes
    
    def write_fu(self):
        xarm7 = self.move_group
        eef_link = self.eef_link

        word_strokes = self.get_word_strokes()
        start_pos = [0.417,-0.241,0.50]

        arm_strokes = self.get_arm_strokes([word_strokes],start_pos)
        # print("++++++arm_strokes",arm_strokes)
        arm_stroke = arm_strokes[0]

        xarm7.set_position_target([arm_stroke[0][0][0],arm_stroke[0][0][1],arm_stroke[0][0][2]+0.03])
        xarm7.plan()
        xarm7.go(wait=True)
        for stroke in arm_stroke:
            for point in stroke:
                print(point)
                xarm7.set_position_target(point)
                xarm7.plan()
                xarm7.go(wait=True)
                print("set_position_target:",point)
            
            current_pose = xarm7.get_current_pose().pose
            xarm7.set_position_target([current_pose.position.x,current_pose.position.y,current_pose.position.z+0.03])
            xarm7.plan()
            xarm7.go(wait=True)
            rospy.sleep(0.1)

        current_pose = xarm7.get_current_pose().pose
        xarm7.set_position_target([current_pose.position.x,current_pose.position.y,current_pose.position.z+0.03])
        xarm7.plan()
        xarm7.go(wait=True)
        rospy.sleep(0.1)
        xarm7.stop()  
        rospy.sleep(1)


    def write_fu_with_cartesian(self):
        xarm7 = self.move_group
        eef_link = self.eef_link

        word_strokes = self.get_word_strokes()
        start_pos = [0.417,-0.241,0.50]

        arm_strokes = self.get_arm_strokes([word_strokes],start_pos)
        # print("++++++arm_strokes",arm_strokes)
        arm_stroke = arm_strokes[0]

        current_pose = xarm7.get_current_pose().pose
        xarm7.set_position_target([arm_stroke[0][0][0],arm_stroke[0][0][1],arm_stroke[0][0][2]+0.03])
        xarm7.plan()
        xarm7.go(wait=True)
        # xarm7.stop()
        # xarm7.clear_pose_targets()
        waypoints = []
        target_pose = xarm7.get_current_pose().pose
        for stroke in arm_stroke:
            for point in stroke:
                target_pose.position.x = point[0]
                target_pose.position.y = point[1]
                target_pose.position.z = point[2]
                waypoints.append(copy.deepcopy(target_pose))
            target_pose.position.z += 0.03
            waypoints.append(copy.deepcopy(target_pose))
        fraction = 0
        maxtrails = 100
        attempts = 0
        jump_threshold = 0.0
        eef_step = 0.01

        while fraction < 1 and attempts < maxtrails:
            plan, fraction = xarm7.compute_cartesian_path(waypoints, eef_step, jump_threshold)
            attempts += 1

            if attempts % 10 == 0:
                print("Still trying after %d attempts ...", attempts)
        
        # Visualize the plan, where the positions, velocity and accelerations of all joints stored
        print("Plan: ", plan)
        print(type(plan))

        # Execute the plan if it is successfully planned, or print how many trials attempted
        if fraction == 1:
            print("Path computed successfully. Moving the arm.")
            xarm7.execute(plan, wait=True)
        else:
            print("Path planning failed with only %0.6f success after %d attempts.", fraction, maxtrails)
        
        current_pose = xarm7.get_current_pose().pose
        xarm7.set_position_target([current_pose.position.x,current_pose.position.y,current_pose.position.z+0.03])
        xarm7.plan()
        xarm7.go(wait=True)
        rospy.sleep(1)


# def draw_cirlce(r,center_vector,limit_size): #需要注意是单位是米
#     center_vector=np.array(center_vector)
#     x=np.zeros((limit_size,1))
#     y=np.zeros((limit_size,1))
#     da = 360 / limit_size
#     for i in range(limit_size):
#         x[i,0]=center_vector[0]+r*(np.cos(i*da/180*np.pi))
#         y[i,0]=center_vector[1]+r*(np.sin(i*da/180*np.pi))

#     z = np.ones((limit_size,1)) * center_vector[2]
#     all=np.hstack((x,y,z))
#     return all  #输出是一个矩阵
# start_pos = [0.3,-0.4,0.49]
# circle_xyz=draw_cirlce(0.05,start_pos,72)





if __name__ == '__main__':

    arm = Arm()
    # arm.move_circle()
    arm.move_circle_with_cartesian()
    # arm.write_fu()
    # arm.write_fu_with_cartesian()



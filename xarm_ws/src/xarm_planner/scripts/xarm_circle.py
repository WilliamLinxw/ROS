#!/usr/bin/env python

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import *
from std_msgs.msg import String
import numpy as np

class MoveCircle(object):
    def __init__(self):
        super(MoveCircle, self).__init__()

        print "================ Setup ================="
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('xarm_move_circle', anonymous=True)

        robot = moveit_commander.RobotCommander()

        scene = moveit_commander.PlanningSceneInterface()

        group_name = 'xarm7'
        move_group = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

        # We can get the name of the reference frame for this robot:
        planning_frame = move_group.get_planning_frame()
        print "============ Planning frame: %s" % planning_frame

        # We can also print the name of the end-effector link for this group:
        eef_link = move_group.get_end_effector_link()
        print "============ End effector link: %s" % eef_link

        # We can get a list of all the groups in the robot:
        group_names = robot.get_group_names()
        print "============ Available Planning Groups:", robot.get_group_names()

        print "============ Printing robot state"
        print robot.get_current_state()
        print "============"

        # Misc variables
        self.box_name = ''
        self.robot = robot
        self.scene = scene
        self.move_group = move_group
        self.display_trajectory_publisher = display_trajectory_publisher
        self.planning_frame = planning_frame
        self.eef_link = eef_link
        self.group_names = group_names

    def move_circle(self):
        xarm7 = self.move_group

        # Go back to the home position
        xarm7.set_named_target('home_pose')
        xarm7.go(wait=True)
        rospy.sleep(1)

        # Go to a desired position with the center of the circle is
        pose_goal = geometry_msgs.msg.Pose()
        pose_goal.orientation.x = 1
        pose_goal.orientation.y = 0
        pose_goal.orientation.z = 0
        pose_goal.orientation.w = 0

        pose_goal.position.x = 0.5
        pose_goal.position.y = 0
        pose_goal.position.z = -0.012

        xarm7.set_pose_target(pose_goal)
        
        xarm7.go(wait=True)
        xarm7.stop()
        xarm7.clear_pose_targets()

        # Get the center of the circle
        current_pose = xarm7.get_current_pose().pose
        centerX = current_pose.position.x
        centerY = current_pose.position.y
        radius = 0.05

        # Create a circle waypoints
        waypoints = []
        # theta = 0
        # while theta <= 2 * pi:
        #     target_pose = xarm7.get_current_pose().pose
        #     target_pose.position.x = centerX + radius * cos(theta)
        #     target_pose.position.y = centerY + radius * sin(theta)
        #     waypoints.append(copy.deepcopy(target_pose))
        #     theta += 0.01
        #     print(theta)
        target_pose = xarm7.get_current_pose().pose
        theta = np.arange(0, 2*np.pi, 0.01)
        x = centerX + radius * np.cos(theta)
        y = centerY + radius * np.sin(theta)
        for i in range(len(x)):
            target_pose.position.x = x[i]
            target_pose.position.y = y[i]
            waypoints.append(copy.deepcopy(target_pose))
        print("Waypoints: ", waypoints)

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

        # Execute the plan if it is successfully planned
        if fraction == 1:
            print("Path computed successfully. Moving the arm.")
            xarm7.execute(plan, wait=True)
        else:
            print("Path planning failed with only %0.6f success after %d attempts.", fraction, maxtrails)
        
        rospy.sleep(1)

        print "============ Motion finished ============"

def main():
    arm = MoveCircle()

    print "============ Press `Enter` to execute a movement function ..."
    raw_input()
    arm.move_circle()

if __name__ == '__main__':
    while not rospy.is_shutdown():
        try:
            main()
            break
        except rospy.ROSInterruptException:
            break
        except KeyboardInterrupt:
            break

    

        


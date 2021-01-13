import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from moveit_python import *
from math import pi
from std_msgs import String

class MoveCircle(object):
    def __init__(self):
        super(MoveCircle, self).__init__()

        print "================ Setup ================="
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('xarm_move_circle', anonymous=True)

        robot = moveit_commander.RobotCommander()

        scene = moveit_commander.PlanningSceneInterface()

        group_name = 'xarm7'
        group = moveit_commander.MoveGroupCommander(group_name)

        display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path', moveit_msgs.msg.DisplayTrajectory, queue_size=20)

        print "================ Waiting for Rviz =================="
        rospy.sleep(10)
        print "================ Start moving! ================="

        print "============ Reference frame: %s" % group.get_planning_frame()

        print "============ End effector link: %s" % group.get_end_effector_link()

        print "============ Robot Groups:"
        print robot.get_group_names()

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
        xarm7.go('home_pose', wait=True)
        xarm7.stop()

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
        current_pose = xarm.get_current_pose().pose
        centerX = current_pose.position.x
        centerY = current_pose.position.y
        radius = 0.05

        # Create a circle waypoints
        waypoints = []
        theta = 0
        while theta <= 4 * pi:
            target_pose = xarm7.get_current_pose().pose
            target_pose.position.x = centerX + radius * cos(theta)
            target_pose.position.y = centerY + radius * sin(theta)
            waypoints.append(copy.deepcopy(target_pose))
            theta += 0.01

        # Compute the Cartesian path
        fraction = 0
        maxtrails = 100
        attepts = 0

        while fraction < 1 and attepts < maxtrails:
        


/*********************************************************************
 * Software License Agreement (BSD License)
 *
 *  Copyright (c) 2012, Willow Garage, Inc.
 *  All rights reserved.
 *
 *  Redistribution and use in source and binary forms, with or without
 *  modification, are permitted provided that the following conditions
 *  are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above
 *     copyright notice, this list of conditions and the following
 *     disclaimer in the documentation and/or other materials provided
 *     with the distribution.
 *   * Neither the name of Willow Garage nor the names of its
 *     contributors may be used to endorse or promote products derived
 *     from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 *  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 *  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 *  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
 *  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 *  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 *  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 *  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 *  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 *  POSSIBILITY OF SUCH DAMAGE.
 *********************************************************************/

/* Author: Sachin Chitta, Michael Lautman*/

#include <ros/ros.h>
#include <moveit_msgs/DisplayRobotState.h>
#include <moveit_msgs/DisplayTrajectory.h>
// MoveIt
#include <moveit/robot_model_loader/robot_model_loader.h>
#include <moveit/robot_model/robot_model.h>
#include <moveit/robot_state/robot_state.h>

#include <fstream>
#include <iostream>
#include <string>


#define write_points_num 897


int main(int argc, char** argv)
{
  ros::init(argc, argv, "robot_model_and_robot_state_tutorial");
  ros::AsyncSpinner spinner(1);
  spinner.start();

  // BEGIN_TUTORIAL
  // Start
  // ^^^^^
  // Setting up to start using the RobotModel class is very easy. In
  // general, you will find that most higher-level components will
  // return a shared pointer to the RobotModel. You should always use
  // that when possible. In this example, we will start with such a
  // shared pointer and discuss only the basic API. You can have a
  // look at the actual code API for these classes to get more
  // information about how to use more features provided by these
  // classes.
  //
  // We will start by instantiating a
  // `RobotModelLoader`_
  // object, which will look up
  // the robot description on the ROS parameter server and construct a
  // :moveit_core:`RobotModel` for us to use.
  //
  // .. _RobotModelLoader:
  //     http://docs.ros.org/melodic/api/moveit_ros_planning/html/classrobot__model__loader_1_1RobotModelLoader.html
  robot_model_loader::RobotModelLoader robot_model_loader("robot_description");
  robot_model::RobotModelPtr kinematic_model = robot_model_loader.getModel();
  ROS_INFO("Model frame: %s", kinematic_model->getModelFrame().c_str());

  // Using the :moveit_core:`RobotModel`, we can construct a
  // :moveit_core:`RobotState` that maintains the configuration
  // of the robot. We will set all joints in the state to their
  // default values. We can then get a
  // :moveit_core:`JointModelGroup`, which represents the robot
  // model for a particular group, e.g. the "white_arm" of the Panda
  // robot.
  robot_state::RobotStatePtr kinematic_state(new robot_state::RobotState(kinematic_model));
  kinematic_state->setToDefaultValues();
  const robot_state::JointModelGroup* joint_model_group = kinematic_model->getJointModelGroup("white_arm");

  const std::vector<std::string>& joint_names = joint_model_group->getVariableNames();
  std::vector<double> joint_values;

  // Print joint state and joint limits
  kinematic_state->printStatePositionsWithJointLimits(joint_model_group);
  int count = 0;

  //Write joint values to joint_position.txt
  std::string out_file_name = "/home/lair-test/ros1_ws/xarm_ws/src/aisr4_moveit_config/src/work_space.txt";
  std::ofstream out_file;
  out_file.open(out_file_name.c_str(),std::ios::app);

  kinematic_state->setToDefaultValues();
  kinematic_state->copyJointGroupPositions(joint_model_group, joint_values);

  // Start time
  ros::WallTime start_time = ros::WallTime::now();
  // Iterate from joint1 to joint4
  for(float joint1 = -1.57; joint1 < 2.3; joint1 += 0.08725)
  {
    for(float joint2 = -2.0; joint2 < 0.15; joint2 += 0.08725)
    {
      for(float joint3 = -1.57; joint3 < 1.57; joint3 += 0.08725)
      {
        for(float joint4 = -2.0; joint4 < 0; joint4 += 0.08725)
        {
          joint_values[0] = joint1;
          joint_values[1] = joint2;
          joint_values[2] = joint3;
          joint_values[3] = joint4;
          joint_values[4] = 0;
          ROS_INFO("Ieteration count: %d", count);
          kinematic_state->setJointGroupPositions(joint_model_group, joint_values);
          const Eigen::Isometry3d& end_effector_state = kinematic_state->getGlobalLinkTransform("white_link8");
          ROS_INFO_STREAM("Translation: \n" << end_effector_state.translation()[0] <<"," << end_effector_state.translation()[1] <<"," << end_effector_state.translation()[2] << "\n");
          out_file << end_effector_state.translation()[0] <<"," << end_effector_state.translation()[1] <<"," <<  end_effector_state.translation()[2] <<std::endl;
          count += 1;
        }
      }
    }
  }
  ROS_INFO("Ieteration count: %d", count);
  ROS_INFO("IK Time :%f",(ros::WallTime::now() - start_time).toSec());


  ros::shutdown();
  return 0;
}

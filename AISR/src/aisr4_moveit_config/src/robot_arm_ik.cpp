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

  // Read txt
  struct vec3 {
    float  x;
    float  y;
    float  z;
    };
  vec3 write_points[write_points_num];
  std::string in_file_name = "/home/lair-test/ros1_ws/aisr/src/aisr4_moveit_config/src/write_point.txt";
  ROS_INFO("File path: %s", in_file_name);
  std::ifstream in_file;
  in_file.open(in_file_name.c_str());
  if (in_file.is_open())
  {
    std::string line;
    int i = 0;
    while(getline(in_file,line))
    {
      const char* split = ",";
      char* p = strtok((char*)line.c_str(), split);
      float val;
      for(int k = 0; p != NULL; k++)
      {
        sscanf(p, "%f", &val);
        p = strtok(NULL, split);
        if (k==0)
        {
          write_points[i].x = val;
        }
        else if (k==1)
        {
          write_points[i].y = val;
        }
        else
        {
          write_points[i].z = val;
        }
      }
      i++;
    }
    in_file.close();
  }
  else
	{
    ROS_INFO("Can't find input file: %s", in_file_name);
	}
  ROS_INFO("write_points: %f,%f", write_points[0].x, write_points[write_points_num-1].x);

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
  kinematic_state->printStatePositionsWithJointLimits(joint_model_group);
  // Get Joint Values
  // ^^^^^^^^^^^^^^^^
  // We can retreive the current set of joint values stored in the state for the Panda arm.
  std::vector<double> joint_values;
  kinematic_state->copyJointGroupPositions(joint_model_group, joint_values);
  ROS_INFO("Joint Value: %f,%f,%f,%f,%f", joint_values[0],joint_values[1],joint_values[2],joint_values[3],joint_values[4]);

  // Set to write_position
  kinematic_state->setToDefaultValues(joint_model_group,"write_position");
  kinematic_state->copyJointGroupPositions(joint_model_group, joint_values);
  ROS_INFO("Joint Value: %f,%f,%f,%f,%f", joint_values[0],joint_values[1],joint_values[2],joint_values[3],joint_values[4]);


  // Inverse Kinematics
  // ^^^^^^^^^^^^^^^^^^
  // We can now solve inverse kinematics (IK) for the Panda robot.
  // To solve IK, we will need the following:
  //
  //  * The desired pose of the end-effector (by default, this is the last link in the "white_arm" chain):
  //    end_effector_state that we computed in the step above.
  //  * The timeout: 0.1 s
  geometry_msgs::Pose target_pose1;
  target_pose1.orientation.w = 1.0;
  double timeout = 0.1;

  //Write joint values to joint_position.txt
  std::string out_file_name = "/home/lair-test/ros1_ws/xarm_ws/src/aisr4_moveit_config/src/joint_position.txt";
  std::ofstream out_file;
  out_file.open(out_file_name.c_str(),std::ios::app);

  ros::WallTime start_time = ros::WallTime::now();

  for(int i = 0; i < write_points_num; i++)
  {
    target_pose1.position.x = write_points[i].x;
    target_pose1.position.y = write_points[i].y;
    target_pose1.position.z = write_points[i].z;
    ROS_INFO("Target position: %f,%f,%f", target_pose1.position.x, target_pose1.position.y, target_pose1.position.z);
    bool found_ik = kinematic_state->setFromIK(joint_model_group, target_pose1, timeout);
    // Now, we can print out the IK solution (if found):
    if (found_ik)
    {
      kinematic_state->copyJointGroupPositions(joint_model_group, joint_values);
      out_file << joint_values[0] <<"," << joint_values[1] <<"," <<  joint_values[2] <<","  << joint_values[3] <<","  << joint_values[4] <<std::endl;
      ROS_INFO("Joint Value: %f,%f,%f,%f,%f", joint_values[0],joint_values[1],joint_values[2],joint_values[3],joint_values[4]);
    }
    else
    {
      ROS_INFO("Did not find IK solution");
    }
  }
  ROS_INFO("IK Time :%f",(ros::WallTime::now() - start_time).toSec());



  ros::shutdown();
  return 0;
}

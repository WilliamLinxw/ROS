cmake_minimum_required(VERSION 3.1.3)
project(aisr4_moveit_config)


find_package(catkin REQUIRED
  COMPONENTS
    interactive_markers
    moveit_core
    moveit_visual_tools
    moveit_ros_planning
    moveit_ros_planning_interface
    moveit_ros_perception
    pluginlib
    geometric_shapes
    pcl_ros
    pcl_conversions
    rosbag
    tf2_ros
    tf2_eigen
    tf2_geometry_msgs
)

find_package(Eigen3 REQUIRED)
find_package(Boost REQUIRED system filesystem date_time thread)

find_package(Boost REQUIRED COMPONENTS system)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)


catkin_package(
  LIBRARIES
  INCLUDE_DIRS
  CATKIN_DEPENDS
    moveit_core
    moveit_visual_tools
    moveit_ros_planning_interface
    interactive_markers
    tf2_geometry_msgs
  DEPENDS
    EIGEN3
)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

add_executable(robot_model_and_robot_state_tutorial src/robot_model_and_robot_state_tutorial.cpp)
add_executable(robot_arm_ik src/robot_arm_ik.cpp)
target_link_libraries(robot_model_and_robot_state_tutorial ${catkin_LIBRARIES} ${Boost_LIBRARIES})
target_link_libraries(robot_arm_ik ${catkin_LIBRARIES} ${Boost_LIBRARIES})

install(TARGETS robot_model_and_robot_state_tutorial robot_arm_ik DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})
install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})

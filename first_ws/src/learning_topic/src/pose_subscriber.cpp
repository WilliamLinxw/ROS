#include <ros/ros.h>
#include "turtlesim/Pose.h"

// Enter the callback function after receiving the message
void poseCallback(const turtlesim::Pose::ConstPtr& msg){
    // Print the message
    ROS_INFO("Turtle pose x: %0.6f, y: %0.6f", msg -> x, msg -> y);
}

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "pose_subscriber");

    // Create node handle
    ros::NodeHandle n;

    // Create a subscriber, subscribing /turtle1/pose, register the callback function poseCallback
    ros::Subscriber pose_sub = n.subscribe("/turtle1/pose", 10, poseCallback);

    // Wait for the callback
    ros::spin();

    return 0;
}
#include <ros/ros.h>
#include <learning_topic/person.h>

// Enter the callback function after receiving the message
void personalInfoCallback(const learning_topic::person::ConstPtr& msg){
    // Print the message
    ROS_INFO("Personal Info: name: %s  age: %d  gender: %d", msg->name.c_str(), msg->age, msg->gender);
}

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "person_subscriber");

    // Create node handle
    ros::NodeHandle n;

    // Create a subscriber, subscribing /turtle1/pose, register the callback function poseCallback
    ros::Subscriber personal_info_sub = n.subscribe("/person_info", 10, personalInfoCallback);

    // Wait for the callback
    ros::spin();

    return 0;
}
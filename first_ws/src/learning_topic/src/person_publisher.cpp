#include <ros/ros.h>
#include <learning_topic/person.h>

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "person_publisher");

    // Create Node Handle
    ros::NodeHandle n;

    // Create a publisher, publishing to the topic /turtle1/cmd_vel, with message type of geometry_msgs::Twist, queue length of 10
    ros::Publisher person_info_pub = n.advertise<learning_topic::person>("/person_info", 10);

    // Set the loop rate
    ros::Rate loop_rate(1);

    while(ros::ok()){
        // Initialize the message
        learning_topic::person person_msg;
        person_msg.name = "Caesar";
        person_msg.age = 22;
        person_msg.gender = learning_topic::person::male;

        // Publish the message
        person_info_pub.publish(person_msg);
        ROS_INFO("Publish Personal Info: name: %s  age: %d  gender: %d", person_msg.name.c_str(), person_msg.age, person_msg.gender);

        // Delay with the loop rate
        loop_rate.sleep();
    }
    return 0;
}
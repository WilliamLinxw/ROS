#include <ros/ros.h>
#include <geometry_msgs/Twist.h>

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "velocty_publisher");

    // Create Node Handle
    ros::NodeHandle n;

    // Create a publisher, publishing to the topic /turtle1/cmd_vel, with message type of geometry_msgs::Twist, queue length of 10
    ros::Publisher turtle_vel_pub = n.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 10);

    // Set the loop rate
    ros::Rate loop_rate(10);

    while(ros::ok()){
        // Initialize the message
        geometry_msgs::Twist vel_msg;
        vel_msg.linear.x = 0.5;
        vel_msg.angular.z = 0.2;

        // Publish the message
        turtle_vel_pub.publish(vel_msg);
        ROS_INFO("Publish the turtle's velocity command[%0.2f m/s, %0.2f rad/s]", vel_msg.linear.x, vel_msg.angular.z);

        // Delay with the loop rate
        loop_rate.sleep();
    }
    return 0;
}
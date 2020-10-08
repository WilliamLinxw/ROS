#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <std_srvs/Trigger.h>

ros::Publisher turtle_vel_pub;
bool pubCommand = false;

// Callback function of service, req as input, res as output
bool commanCallback(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res){
    pubCommand = !pubCommand;

    // Display the request data
    ROS_INFO("Publish turtle velocity command [%s]", pubCommand==true?"Yes":"No");

    // Set the response data
    res.success == true;
    res.message = "Change turtle command state!";

    return true;
}

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "turtle_command_server");

    // Create the handle
    ros::NodeHandle n;

    // Create a server named /turtle_command, with the callback function of commandCallback
    ros::ServiceServer command_service = n.advertiseService("/turtle_command", commanCallback);

    // Create a publisher, publishing to /turtle1/cmd_vel with message type geometry_msgs::Twist and queue of 10
    turtle_vel_pub = n.advertise<geometry_msgs::Twist>("/turtle1/cmd_vel", 10);

    // Wait for the call back
    ROS_INFO("Ready to receive turtle.");

    // Set the loop rate
    ros::Rate loop_rate(10);

    while(ros::ok()){
        // Check the callback queue
        ros::spinOnce();

        // If the flag is true, publish the velocity command
        if(pubCommand){
            geometry_msgs::Twist vel_msg;
            vel_msg.linear.x = 0.5;
            vel_msg.angular.z = 0.2;
            turtle_vel_pub.publish(vel_msg);
        }

        // Loop
        loop_rate.sleep();
    }
}
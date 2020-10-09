#include <string>
#include <ros/ros.h>
#include <std_srvs/Empty.h>

int main(int argc, char **argv){
    int red, green, blue;

    // Initialize the node
    ros::init(argc, argv, "parameter_config");

    // Create the node handle
    ros::NodeHandle node;

    // Read the current parameters
    ros::param::get("/turtlesim/background_r", red);
    ros::param::get("/turtlesim/background_g", green);
    ros::param::get("/turtlesim/background_b", blue);

    ROS_INFO("Get background color: %d, %d, %d.", red, green, blue);

    // Set the parameters
    ros::param::set("/turtlesim/background_r", 255);
    ros::param::set("/turtlesim/background_g", 255);
    ros::param::set("/turtlesim/background_b", 255);

    ROS_INFO("Set background color:255, 255, 255.");

    // Read the current parameters
    ros::param::get("/turtlesim/background_r", red);
    ros::param::get("/turtlesim/background_g", green);
    ros::param::get("/turtlesim/background_b", blue);

    ROS_INFO("Re-get background color: %d, %d, %d.", red, green, blue);

    // Call the service the refresh the background color
    ros::service::waitForService("/clear");
    ros::ServiceClient clear_background = node.serviceClient<std_srvs::Empty>("/clear");
    std_srvs::Empty srv;
    clear_background.call(srv);

    sleep(1);
}
#include <ros/ros.h>
#include <turtlesim/Spawn.h>

int main(int argc, char** argv){
    // Initialize the node
    ros::init(argc, argv, "turtle_spawn");

    // Create the node handle
    ros::NodeHandle node;

    // Create a client for the /spawn service to link them
    ros::service::waitForService("/spawn");
    ros::ServiceClient add_turtle = node.serviceClient<turtlesim::Spawn>("/spawn");

    // Initialize the requesting data of turtlesim::Spawn
    turtlesim::Spawn srv;
    srv.request.x = 2.0;
    srv.request.y = 2.0;
    srv.request.name = "turtle2";

    // Request the call of service
    ROS_INFO("Call service to spawn turtle at [x: %0.6f, y; %0.6f] with [name: %s]", srv.request.x, srv.request.y, srv.request.name.c_str());
    add_turtle.call(srv);

    // Display the result of calling
    ROS_INFO("Spawn turtle successfully [name: %s]", srv.response.name.c_str());

    return 0;
}
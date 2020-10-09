#include <ros/ros.h>
#include <learning_service/Person.h>

// Callback of the service, with req as input and res as output
bool personCallback(learning_service::Person::Request &req, learning_service::Person::Response &res){
    // Display the request information
    ROS_INFO("Person: name: %s, age: %d, gender: %d", req.name.c_str(), req.age, req.gender);

    // Set the response
    res.result = "OK";

    return true;
}

int main(int argc, char **argv){
    // Initialize the node
    ros::init(argc, argv, "person_server");

    // Create the node handle
    ros::NodeHandle n;

    // Create a service named /show_person, register the callback function personCallback
    ros::ServiceServer person_service = n.advertiseService("/show_person", personCallback);

    // Wait for the callback
    ROS_INFO("Ready to show personal information");
    ros::spin();

    return 0;
}
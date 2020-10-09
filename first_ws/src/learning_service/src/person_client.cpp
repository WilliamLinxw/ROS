#include <ros/ros.h>
#include <learning_service/Person.h>

int main(int argc, char** argv){
    // Initialize the node
    ros::init(argc, argv, "person_client");

    // Create the node handle
    ros::NodeHandle node;

    // Create a client after finding the /show_person service and connect them
    ros::service::waitForService("/show_person");
    ros::ServiceClient person_client = node.serviceClient<learning_service::Person>("/show_person");

    // Initialize the request data for learning_service::Person
    learning_service::Person srv;
    srv.request.name = "Tom";
    srv.request.age = 20;
    srv.request.gender = learning_service::Person::Request::male;

    // Require for the service
    ROS_INFO("Call service to show person[name: %s, age: %d, gender: %d]", srv.request.name.c_str(), srv.request.age, srv.request.gender);

    person_client.call(srv);

    // Display the calling result
    ROS_INFO("Show person result: %s", srv.response.result.c_str());

    return 0;
}
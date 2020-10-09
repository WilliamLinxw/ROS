#include <ros/ros.h>
#include <tf/transform_broadcaster.h>
#include <turtlesim/Pose.h>

std::string turtle_name;

void poseCallback(const turtlesim::PoseConstPtr& msg){
    // Create a tf broadcaster
    static tf::TransformBroadcaster br;

    // Initialize the tf params
    tf::Transform transform;
    transform.setOrigin(tf::Vector3(msg->x, msg->y, 0.0));
    tf::Quaternion q;
    q.setRPY(0, 0, msg->theta);
    transform.setRotation(q);

    // Broadcast the tf data between the world and turtles
    br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "world", turtle_name));
}

int main(int argc, char** argv){
    // Initialize the node
    ros::init(argc, argv, "my_tf_broadcaster");

    // Use the input to select turtle
    if(argc != 2){
        ROS_ERROR("Need a turtle name as an argument");
        return -1;
    }

    turtle_name = argv[1];

    // Subscribe the pose topic
    ros::NodeHandle node;
    ros::Subscriber sub = node.subscribe(turtle_name+"/pose", 10, &poseCallback);

    // Wait for the callback
    ros::spin();

    return 0;
}
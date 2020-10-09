#include <ros/ros.h>
#include <tf/transform_listener.h>
#include <geometry_msgs/Twist.h>
#include <turtlesim/Spawn.h>

int main(int argc, char** argv){
    // Initialize the node
    ros::init(argc, argv, "my_if_listener");

    // Create the node handle
    ros::NodeHandle node;

    // Spawn turtle2
    ros::service::waitForService("/spawn");
    ros::ServiceClient add_turtle = node.serviceClient<turtlesim::Spawn>("/spawn");
    turtlesim::Spawn srv;
    add_turtle.call(srv);

    // Create the publisher to send velocity command
    ros::Publisher turtle_vel = node.advertise<geometry_msgs::Twist>("/turtle2/cmd_vel", 10);

    // Create a tf listener
    tf::TransformListener listener;

    ros::Rate rate(10.0);

    while(node.ok()){
        // Get tf data between turtle1 and turtle2
        tf::StampedTransform transform;
        try{
            listener.waitForTransform("/turtle2", "turtle1", ros::Time(0), ros::Duration(3.0));
            listener.lookupTransform("/turtle2", "turtle1", ros::Time(0), transform);
        }
        catch(tf::TransformException &ex){
            ROS_ERROR("%s", ex.what());
            ros::Duration(1.0).sleep();
            continue;
        }

        // Publish the velocity command for turtle1 according to their positions
        geometry_msgs::Twist vel_msg;
        vel_msg.angular.z = 4.0 * atan2(transform.getOrigin().y(), transform.getOrigin().x());
        vel_msg.linear.x = 0.5 * sqrt(pow(transform.getOrigin().x(), 2) + pow(transform.getOrigin().y(),2));
        turtle_vel.publish(vel_msg);

        rate.sleep();
    }
    return 0;
}
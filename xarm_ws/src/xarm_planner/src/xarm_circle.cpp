#include <math.h>
#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/robot_trajectory/robot_trajectory.h>

using namespace std;

int main(int argc, char **argv)
{
    ros::init(argc, argv, "draw_a_circle");
    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::MoveGroupInterface xarm7("xarm7");

    string eef_link = xarm7.getEndEffector();
    std::string reference_frame = "world";
    xarm7.setPoseReferenceFrame(reference_frame);

    xarm7.allowReplanning(true);

    xarm7.setGoalPositionTolerance(0.001);
    xarm7.setGoalOrientationTolerance(0.01);
    xarm7.setMaxAccelerationScalingFactor(0.8);
    xarm7.setMaxVelocityScalingFactor(0.8);

    // Back to home position
    xarm7.setNamedTarget("home_pose");
    xarm7.move();
    sleep(1);

    geometry_msgs::Pose target_pose;
    target_pose.orientation.x = 1;
    target_pose.orientation.y = 0;
    target_pose.orientation.z = 0;
    target_pose.orientation.w = 0;

    target_pose.position.x = 0.50;
    target_pose.position.y = 0;
    target_pose.position.z = -0.012;

    xarm7.setPoseTarget(target_pose);
    xarm7.move();

    vector<geometry_msgs::Pose> waypoints;
    waypoints.push_back(target_pose);

    // Create a circle on a surface with the same z coordinate
    double centerA = target_pose.position.x;
    double centerB = target_pose.position.y;
    double radius = 0.06;

    for(double theta = 0.0; theta <= M_PI*4; theta += 0.01)
    {
        target_pose.position.x = centerA + radius * cos(theta);
        target_pose.position.y = centerB + radius * sin(theta);
        waypoints.push_back(target_pose);
    }

    // Compute Cartesian Path
    moveit_msgs::RobotTrajectory trajectory;
    const double jump_threshold = 0.0;
    const double eef_step = 0.01;
    double fraction = 0.0;
    int maxtries = 100;   // Max trials
    int attempts = 0;     // Trials taken

    while(fraction < 1.0 && attempts < maxtries)
    {
        fraction = xarm7.computeCartesianPath(waypoints, eef_step, jump_threshold, trajectory);
        attempts++;

        if(attempts % 10 == 0)
            ROS_INFO("Still trying after %d attempts...", attempts);
    }

    if(fraction == 1)
    {
        ROS_INFO("Path computed successfully. Moving the arm.");

        // Generate the data of motion planning
        moveit::planning_interface::MoveGroupInterface::Plan plan;
        plan.trajectory_ = trajectory;

        // Execute the plan
        xarm7.execute(plan);
        sleep(1);
    }
    else
    {
        ROS_INFO("Path planning failed with only %0.6f success after %d attempts.", fraction, maxtries);
    }

    // // Back to the home position
    // xarm7.setNamedTarget("home_pose");
    // xarm7.move();
    // sleep(1);

    ros::shutdown();
    return 0;
}
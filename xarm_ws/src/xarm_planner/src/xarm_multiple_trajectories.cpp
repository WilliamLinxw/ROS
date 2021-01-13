#include <ros/ros.h>
#include <moveit/move_group_interface/move_group_interface.h>
#include <moveit/robot_trajectory/robot_trajectory.h>
#include <moveit/trajectory_processing/iterative_time_parameterization.h>
#include <moveit_msgs/OrientationConstraint.h>

int main(int argc, char **argv)
{
    ros::init(argc, argv, "xarm_multiple_trajectories");
    ros::NodeHandle node_handle;
    ros::AsyncSpinner spinner(1);
    spinner.start();

    moveit::planning_interface::MoveGroupInterface xarm7("xarm7");

    double accScale = 0.8;
    double velScale = 0.8;
    xarm7.setMaxAccelerationScalingFactor(accScale);
    xarm7.setMaxVelocityScalingFactor(velScale);
    xarm7.setGoalPositionTolerance(0.001);
    xarm7.setGoalOrientationTolerance(0.01);

    // 控制机械臂先回到初始化位置
    xarm7.setNamedTarget("home_pose");
    xarm7.move();
    sleep(1);

    std::string end_effector_link = xarm7.getEndEffectorLink();

    //设置目标位置所使用的参考坐标系
    std::string reference_frame = "world";
    xarm7.setPoseReferenceFrame(reference_frame);

    //当运动规划失败后，允许重新规划
    xarm7.allowReplanning(true);

    geometry_msgs::Pose target_pose;
    target_pose.position.x = 0.3397;
    target_pose.position.y = 0;
    target_pose.position.z = 0.263206;
    target_pose.orientation.x = 0.7071;
    target_pose.orientation.y = 0;
    target_pose.orientation.z = 0;
    target_pose.orientation.w = 0.7071;

    xarm7.setPoseTarget(target_pose);

    moveit::planning_interface::MoveGroupInterface::Plan plan1;
    moveit::planning_interface::MoveItErrorCode success1 = xarm7.plan(plan1);

    ROS_INFO("Plan1 (pose goal) %s", success1 ? "SUCCESS":"FAILED");

    if(success1)
      xarm7.execute(plan1);
    sleep(1);

    target_pose.position.x = 0.091682;
    target_pose.position.y = -0.384206;
    target_pose.position.z = 0.445935;
    xarm7.setPoseTarget(target_pose);

    moveit::planning_interface::MoveGroupInterface::Plan plan2;
    moveit::planning_interface::MoveItErrorCode success2 = xarm7.plan(plan2);

    ROS_INFO("Plan2 (pose goal) %s", success2 ? "SUCCESS":"FAILED");

    if(success2)
      xarm7.execute(plan2);
    sleep(1);

    // 控制机械臂回到初始化位置
    xarm7.setNamedTarget("home_pose");
    xarm7.move();
    sleep(1);

    //连接两条轨迹
    moveit_msgs::RobotTrajectory trajectory;
    trajectory.joint_trajectory.joint_names = plan1.trajectory_.joint_trajectory.joint_names;
    trajectory.joint_trajectory.points = plan1.trajectory_.joint_trajectory.points;
    for(unsigned i = 0; i < plan2.trajectory_.joint_trajectory.points.size(); i++)
    {
        trajectory.joint_trajectory.points.push_back(plan2.trajectory_.joint_trajectory.points[i]);
    }

    //采用时间最优算法对轨迹重规划
    moveit::planning_interface::MoveGroupInterface::Plan joinedPlan;
    robot_trajectory::RobotTrajectory rt(xarm7.getCurrentState()->getRobotModel(), "xarm7");
    rt.setRobotTrajectoryMsg(*xarm7.getCurrentState(), trajectory);
    trajectory_processing::IterativeParabolicTimeParameterization iptp;
    iptp.computeTimeStamps(rt, velScale, accScale);

    rt.getRobotTrajectoryMsg(joinedPlan.trajectory_);

    if (!xarm7.execute(joinedPlan))
    {
        ROS_ERROR("Failed to execute plan");
        return false;
    }

    sleep(1);

    ROS_INFO("Finished");

    ros::shutdown(); 

    return 0;
}
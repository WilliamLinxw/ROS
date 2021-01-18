# 结合XArm Moveit功能包画圆

- 在模拟环境中画圆

  1. 启动MoveIt

     ``` 
     $ roslaunch xarm7_moveit_config demo.launch
     ```

  2. 运行画圆脚本

     ```
     运行C++节点（文件位于xarm_planner/src/xarm_circle.cpp）
     $ rosrun xarm_planner xarm_circle
     或
     运行Python节点（脚本位于xarm_planner/scripts/xarm_circle.cpp，脚本中可打印利用MoveIt生成的规划等信息，也可自行添加日志命令查看程序中运行的记录）
     $ rosrun xarm_planner xarm_circle.py
     ```

- 在实际环境中画圆（需要连接XArm）

  1. 启动MoveIt并连接XArm（28楼机械臂IP：192.168.1.209）

     ```
     $ roslaunch xarm_planner xarm_planner_realHW.launch robot_ip:=<your controller box LAN IP address>
     ```

  2. 运行画圆脚本

     ```
     运行C++节点（文件位于xarm_planner/src/xarm_circle.cpp）
     $ rosrun xarm_planner xarm_circle
     或
     运行Python节点（脚本位于xarm_planner/scripts/xarm_circle.cpp，脚本中可打印利用MoveIt生成的规划等信息，也可自行添加日志命令查看程序中运行的记录）
     $ rosrun xarm_planner xarm_circle.py
     ```

     
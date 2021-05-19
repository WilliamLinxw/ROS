#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  time
import numpy as np
from xarm.wrapper import XArmAPI
from xarm.wrapper import XArmAPI

real_zero_values = [-162.4, 70,114,58,194]  #模型中关节为0度时,实体关节的角度
def model_values_to_real_values(model_values = [0,0,0,0,0]):
    ''' 将模型上的角度转为xarm上的角度 加上一个初始差值 '''
    real_values = model_values
    real_values[0] += real_zero_values[0]
    real_values[1] += real_zero_values[1]
    real_values[2] += real_zero_values[2]
    real_values[3] *= -1
    real_values[3] += real_zero_values[3]
    real_values[4] *= -1
    real_values[4] += real_zero_values[4]
    return real_values


if __name__ == '__main__': 
    # Init 
    ip = '192.168.1.217'
    arm = XArmAPI(ip)
    arm.motion_enable(enable=True)
    arm.set_mode(0)
    arm.set_state(0)
    count = 0
    
    # Read joint_position.txt
    in_file = "./joint_position.txt"
    joint_positions = np.zeros((897,5))
    i = 0
    with open(in_file, 'r+', encoding='utf-8') as f:
        for line in f.readlines():
            joints = line[:-1].split(',')
            joint_positions[i][0] = float(joints[0])
            joint_positions[i][1] = float(joints[1])
            joint_positions[i][2] = float(joints[2])
            joint_positions[i][3] = float(joints[3])
            joint_positions[i][4] = float(joints[4])
            i = i + 1
    
    print("joint_position:",len(joint_positions))
    print(joint_positions)

    input("-------- Press Enter to publish --------")

    for joint_position in joint_positions:
        # print("joint_value:",joint_position[:])
        angles = [joint_position[0]*180/3.14159, joint_position[1]*180/3.14159, joint_position[2]*180/3.14159, joint_position[3]*180/3.14159, joint_position[4]*180/3.14159,54.5, -26]
        angles_ = model_values_to_real_values(angles)
        print(angles_)
        if arm.connected and arm.state != 4:
            ret = arm.set_servo_angle(angle=angles_, is_radian = False,radius = 40, speed = 60, wait=True)
            print('moved')
    # Move up
    angles_[3] = angles_[3] + 10
    arm.set_servo_angle(angle=angles_, is_radian = False,radius = 40, speed = 40, wait=True)
          
    arm.disconnect()



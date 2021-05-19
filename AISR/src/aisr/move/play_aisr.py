#!/usr/bin/env python
#coding=utf-8

import rospy
import sys
import numpy as np
import math
from std_msgs.msg import Float64
import pickle as pk
import pdb
import time
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class run_sim(object):
    def __init__(self):
        self.joint_publishers = {}
        self.name_list = ['waist1', 'waist2', 'waist3', 'neck1', 'neck2', 'white1', 'white2', 'white3', 
        'white4', 'white5', 'black1', 'black2', 'black3', 'black4', 'black5', 'black6', 'black7']
        """
        self.name_list = ["waist_pan", "waist_roll", "head_tilt", "head_pan",
                 "r_shoulder_lift", "r_upper_arm_roll", "r_elbow_flex", "r_shoulder_out", "r_wrist_roll",
                 "l_shoulder_lift", "l_upper_arm_roll", "l_elbow_flex", "l_shoulder_out", "l_wrist_roll",  
                 "r_thumb1", "r_thumb", "r_thumb3", "r_index1", "r_index", "r_index3", 
                 "r_middle1", "r_middle", "r_middle3", "r_ring1", "r_ring", "r_ring3", "r_ring4",
                 "r_pinky1", "r_pinky", "r_pinky3", "r_pinky4",                   
                 "l_thumb1", "l_thumb", "l_thumb3", "l_index1", "l_index", "l_index3", 
                 "l_middle1", "l_middle", "l_middle3", "l_ring1", "l_ring", "l_ring3", "l_ring4",
                 "l_pinky1", "l_pinky", "l_pinky3", "l_pinky4"]        
        self.name_list = ["waist_pan", "waist_roll", "head_tilt", "head_pan",
                 "r_shoulder_lift", "r_upper_arm_roll", "r_elbow_flex", "r_shoulder_out", "r_wrist_roll",
                 "l_shoulder_lift", "l_upper_arm_roll", "l_elbow_flex", "l_shoulder_out", "l_wrist_roll",  
                 "l_thumb1", "l_thumb", "l_thumb3", "l_index1", "l_index", "l_index3", 
                 "l_middle1", "l_middle", "l_middle3", "l_ring1", "l_ring", "l_ring3", "l_ring4",
                 "l_pinky1", "l_pinky", "l_pinky3", "l_pinky4",
                 "r_thumb1", "r_thumb", "r_thumb3", "r_index1", "r_index", "r_index3", 
                 "r_middle1", "r_middle", "r_middle3", "r_ring1", "r_ring", "r_ring3", "r_ring4",
                 "r_pinky1", "r_pinky", "r_pinky3", "r_pinky4"]
        """
        self.set_publishers()

    def set_publishers(self):
        for name in self.name_list:
            self.joint_publishers[name + '_pub'] = rospy.Publisher('/aisr/%s_controller/command'%name, Float64, queue_size=10)        

    def step_sim(self, data):
        for i in range(len(self.name_list)):
            self.joint_publishers[self.name_list[i] + '_pub'].publish(data[i])

def integrate(action1, action2, scale):
    action1 = np.array(action1)
    action2 = np.array(action2)
    delta = (action2 - action1) / scale
    int_actions = []
    for i in range(scale):
        int_actions.append(action1 + i * delta)
    return int_actions

def integrate_all(action_list, scale):
    int_action_list = []
    for i in range(len(action_list) - 1):
        # interpolation between two actions
        int_actions = integrate(action_list[i], action_list[i + 1], scale)
        int_action_list.append(int_actions)
    return int_action_list

def plot_line(ax, A, B, c=None):
    if c:
        ax.plot3D([A[0], B[0]], [A[1], B[1]], [A[2], B[2]], c=c)
    else:
        ax.plot3D([A[0], B[0]], [A[1], B[1]], [A[2], B[2]])

def print_degress(data):
    print("waist_pan: ", np.degrees(data[0]), data[0])
    print("head_pan: ", np.degrees(data[3]), data[3])
    print("r_shoulder_lift: ", np.degrees(data[4]), data[4])
    print("r_upper_arm_roll: ", np.degrees(data[5]), data[5])
    print("r_elbow_flex: ", np.degrees(data[6]), data[6])
    print("r_shoulder_out: ", np.degrees(data[7]), data[7])
    print("r_wrist_roll: ", np.degrees(data[8]), data[8])

    print("l_shoulder_lift: ", np.degrees(data[9]), data[9])
    print("l_upper_arm_roll: ", np.degrees(data[10]), data[10])
    print("l_elbow_flex: ", np.degrees(data[11]), data[11])
    print("l_shoulder_out: ", np.degrees(data[12]), data[12])
    print("l_wrist_roll: ", np.degrees(data[13]), data[13])

    print("r_thumb: ", np.degrees(data[14: 17]))
    print("r_index: ", np.degrees(data[17: 20]))
    print("r_middle: ", np.degrees(data[20: 23]))
    print("r_ring: ", np.degrees(data[23: 27]))
    print("r_pinky: ", np.degrees(data[27: 31]))
    print("l_thumb: ", np.degrees(data[31: 34]))
    print("l_index: ", np.degrees(data[34: 37]))
    print("l_middle: ", np.degrees(data[37: 40]))
    print("l_ring: ", np.degrees(data[40: 44]))
    print("l_pinky: ", np.degrees(data[44: 48]))

def axisEqual3D(ax):
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)

"""
pose_joint = {
    "spine_base" : 0,
    "r_hip" : 1,
    "r_knee" : 2,
    "r_ankle" : 3,
    "l_hip" : 4,
    "l_knee" : 5,
    "l_ankle" : 6,
    "spine_mid" : 7,
    "neck" : 8,
    "nose" : 9,
    "head" : 10,
    "l_shoulder" : 11,
    "l_elbow" : 12,
    "l_wrist" : 13,
    "r_shoulder" : 14,
    "r_elbow" : 15,
    "r_wrist" : 16
}
"""
pose_joint_name_list = ['spine_base', 'spine_mid', 'neck', 'head', 
                     'l_shoulder', 'l_elbow', 'l_wrist', 'l_hand', 
                     'r_shoulder', 'r_elbow', 'r_wrist', 'r_hand',
                     'l_hip', 'l_knee', 'l_ankle', 'l_foot', 
                     'r_hip', 'r_knee', 'r_ankle', 'r_foot',
                     'spine_shoulder', 'l_handtip', 'l_thumb', 
                     'r_handtip', 'r_thumb']
pose_joint = {}
for i in range(len(pose_joint_name_list)):
    pose_joint[pose_joint_name_list[i]] = i

robot_joint = {
    "waist_pan" : 0,
    "waist_roll" : 1,
    "head_tilt" : 2,
    "head_pan" : 3,
    "r_shoulder_lift" : 4,
    "r_upper_arm_roll" : 5,
    "r_elbow_flex" : 6,
    "r_shoulder_out" : 7,
    "r_wrist_roll" : 8,
    "l_shoulder_lift" : 9,
    "l_upper_arm_roll" : 10,
    "l_elbow_flex" : 11,
    "l_shoulder_out" : 12,
    "l_wrist_roll" : 13
}

def main(angles, skeleton=None, idx=0, rate=25, debug=False):
    rospy.init_node('TaiChi', anonymous=True)
    sim = run_sim()
    rate = rospy.Rate(rate)
    time_ = time.time()
    sim.step_sim(angles)
    rate.sleep()

    # debug, print skeleton and angles
    """
    print("skeleton:")
    print(skeleton)
    print("angles:")
    print_degress(angles)
    print("")
    """

    # print("angles:")
    # print_degress(angles)
    # print("")

    if debug:
        # print_degress(angles)
    
        plot_list = [pose_joint["spine_base"], pose_joint["spine_mid"], pose_joint["spine_shoulder"], \
                     pose_joint["l_shoulder"], pose_joint["l_elbow"], pose_joint["l_wrist"], \
                    pose_joint["r_shoulder"], pose_joint["r_elbow"], pose_joint["r_wrist"]]
                    # pose_joint["r_hand"], pose_joint["r_thumb"], pose_joint["l_hand"], pose_joint["l_thumb"]]
        
        # errors = pk.load(open("/home/diqichen/workspace/action-imitation/action/yan1_traverse_v7_s04_f1_w4_h_errors.pkl", "rb"))
        # print("errors: ", errors[i])
        
        '''
        # draw skeleton and hands
        plt.ioff()
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        # skeleton
        ax.scatter3D(skeleton[0][plot_list, 0], skeleton[0][plot_list, 1], skeleton[0][plot_list, 2]);
        plot_line(ax, skeleton[0][pose_joint["spine_base"]], skeleton[0][pose_joint["spine_mid"]])
        plot_line(ax, skeleton[0][pose_joint["spine_mid"]], skeleton[0][pose_joint["spine_shoulder"]])
        plot_line(ax, skeleton[0][pose_joint["spine_shoulder"]], skeleton[0][pose_joint["l_shoulder"]])
        plot_line(ax, skeleton[0][pose_joint["spine_shoulder"]], skeleton[0][pose_joint["r_shoulder"]])
        plot_line(ax, skeleton[0][pose_joint["l_shoulder"]], skeleton[0][pose_joint["l_elbow"]], c='b')
        plot_line(ax, skeleton[0][pose_joint["l_elbow"]], skeleton[0][pose_joint["l_wrist"]], c='b')
        plot_line(ax, skeleton[0][pose_joint["r_shoulder"]], skeleton[0][pose_joint["r_elbow"]], c='r')
        plot_line(ax, skeleton[0][pose_joint["r_elbow"]], skeleton[0][pose_joint["r_wrist"]], c='r')
        # hands
        ax.scatter3D(skeleton[1][:, 0], skeleton[1][:, 1], skeleton[1][:, 2], c='r'); # right
        ax.scatter3D(skeleton[2][:, 0], skeleton[2][:, 1], skeleton[2][:, 2], c='b'); # left
        
        print(skeleton[1])
        print(skeleton[2])
        axisEqual3D(ax)        
        plt.show()
        '''

        """
        # draw skeleton
        plt.ioff()
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.scatter3D(skeleton[plot_list, 0], skeleton[plot_list, 1], skeleton[plot_list, 2]);
        plot_line(ax, skeleton[pose_joint["spine_base"]], skeleton[pose_joint["spine_mid"]])
        plot_line(ax, skeleton[pose_joint["spine_mid"]], skeleton[pose_joint["spine_shoulder"]])
        plot_line(ax, skeleton[pose_joint["spine_shoulder"]], skeleton[pose_joint["l_shoulder"]])
        plot_line(ax, skeleton[pose_joint["spine_shoulder"]], skeleton[pose_joint["r_shoulder"]])
        plot_line(ax, skeleton[pose_joint["l_shoulder"]], skeleton[pose_joint["l_elbow"]], c='b')
        plot_line(ax, skeleton[pose_joint["l_elbow"]], skeleton[pose_joint["l_wrist"]], c='b')
        plot_line(ax, skeleton[pose_joint["l_wrist"]], skeleton[pose_joint["l_hand"]], c='b')
        plot_line(ax, skeleton[pose_joint["l_wrist"]], skeleton[pose_joint["l_thumb"]], c='g')
        plot_line(ax, skeleton[pose_joint["r_shoulder"]], skeleton[pose_joint["r_elbow"]], c='r')
        plot_line(ax, skeleton[pose_joint["r_elbow"]], skeleton[pose_joint["r_wrist"]], c='r')
        plot_line(ax, skeleton[pose_joint["r_wrist"]], skeleton[pose_joint["r_hand"]], c='r')
        plot_line(ax, skeleton[pose_joint["r_wrist"]], skeleton[pose_joint["r_thumb"]], c='g')
        axisEqual3D(ax)
        plt.show()
        """

        # debug, sshow image
        # img_dir = "/raid/home/chendiqi/Dataset/TaiChi/outputVideos/TaiChi2/"
        # img_dir = "/media/Data/Diqi/data/outputVideos/TaiChi2/"
        # img_dir = "/media/Data/Diqi/data/videos/data_hello/color_image/"
          
        img_dir = "/media/Data/data/data_yan3/color_image/"
        img_name = img_dir + "%05d.png"%(0 + 3 * (idx))
        img = mpimg.imread(img_name)
        plt.imshow(img)
        plt.show()
        
    return time_

if __name__ == '__main__':    
    if len(sys.argv) > 1:
        action_list, skeleton_list = pk.load(open("./action/%s.pkl"%sys.argv[1], "rb"))
    else:
        action_list, skeleton_list = pk.load(open("/home/diqichen/workspace/action-imitation/action/yan1_traverse_v7_s04_f1_w4.pkl", "rb"))
    # action_list = []
    # for i in range(100):
        # action_list.append((np.random.rand(17) - 0.5) * 2)
        # action_list.append(np.zeros(17))

    # core parameters
    
    discrete = True    
    if discrete:
        debug = False
        fps = 2
        scale = 5
        rate = fps
        smooth = False
        n_smooth = 0
        interpolation = False
    else:
        debug = False
        fps = 25
        scale = 2
        rate = fps
        smooth = True
        n_smooth = 10
        interpolation = True
    
    rate_control = False
    bound = 10
    cnt = 0
    try:
        if debug == False:
            # try postprocessing
            if smooth:
                for i in range(n_smooth):
                    smooth_action_list = []
                    for i in range(len(action_list)):
                        if i == 0 or i == len(action_list) - 1:
                            smooth_action_list.append(action_list[i])
                        else:
                            # no smooth for hand joint angles
                            tmp_action_list = (action_list[i - 1] + action_list[i] + action_list[i + 1]) / 3
                            tmp_action_list[14:] = action_list[i][14:]
                            smooth_action_list.append(tmp_action_list)
                    action_list = smooth_action_list

            if interpolation:
                # action_list = action_list[0:20]
                # with interpolation
                int_action_list = integrate_all(action_list, scale)
                start_time = time.time()
                # waist_pan = action_list[0][0]
                step_time = []                
                for a_list in int_action_list:
                    for action in a_list:
                        cnt += 1
                        if rate_control:                            
                            if cnt > fps:
                                end_time = time.time()
                                real_fps = cnt / (end_time - start_time)
                                if real_fps < fps and rate <= fps + bound:
                                    rate += 1
                                elif real_fps > fps and rate >= fps - bound:
                                    rate -= 1
                        print(cnt)
                        print(action)
                        # if cnt % 25 == 0:
                            # pdb.set_trace()
                        time_ = main(action, rate=rate)
                        step_time.append(time_)
                end_time = time.time()
                print("time: %fs"%(end_time - start_time))
            else:
                # without interpolation
                start_time = time.time()
                # waist_pan = action_list[0][0]
                step_time = []
                for action in action_list:
                    # print(action)
                    # action[0] = waist_pan
                    time_ = main(action, rate=rate)
                    step_time.append(time_)
                    print(cnt)
                    mask = [5, 6, 7, 8, 9]
                    print(action[mask])
                    cnt += 1
                    time.sleep(1.0)
                    if cnt > fps:
                        end_time = time.time()
                        real_fps = cnt / (end_time - start_time)
                        if real_fps < fps and rate <= fps + bound:
                            rate += 1
                        elif real_fps > fps and rate >= fps - bound:
                            rate -= 1
                        # if cnt % fps == 0:
                            # print(real_fps, rate)
            
            step_time = np.array(step_time)
            step_time = step_time[1:] - step_time[:-1]
            print("mean: ", step_time.mean())
            print("std: ", step_time.std())
            print("min: ", step_time.min())
            print("max: ", step_time.max())
        else:
            # debug, observe actions frame by frame
            for i in range(len(action_list)):
                if i < 0:
                    continue
                print(skeleton_list[i])
                main(action_list[i], skeleton_list[i], i, debug=debug)
        
    except rospy.ROSInterruptException:
        sys.exit()
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from scipy.spatial import ConvexHull
import math

def distance(point1,point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)

if __name__ == '__main__': 
    # Init 
    
    # Read joint_position.txt
    in_file = "./workspace.txt"
    x_positions = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    y_positions = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    z_positions = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    x_min = 0.0
    x_max = 0.0
    y_min = 0.0
    y_max = 0.0
    z_min = 0.0
    z_max = 0.0
    inner_ellipse_a = [1000.0]*25
    inner_ellipse_b = [1000.0]*25
    z_scape = np.linspace(0.51,1.78,25)
    print("z_scape:",z_scape)
    with open(in_file, 'r+', encoding='utf-8') as f:
        for i,line in enumerate(f.readlines()):
            position = line[:-1].split(',')
            x = float(position[0])
            y = float(position[1])
            z = float(position[2])
            if i == 0:
                x_min = x_max = x
                y_min = y_max = y
                z_min = z_max = z
            if i%1 ==0:
                if x_min > x:
                    x_min = x
                if x_max < x:
                    x_max = x
                if y_min > y:
                    y_min = y
                if y_max < y:
                    y_max = y
                if z_min > z:
                    z_min = z
                if z_max < z:
                    z_max = z
                for k,z_value in enumerate(z_scape):
                    if z >= z_value and z <= z_value+0.01:
                        x_positions[k].append(x)
                        y_positions[k].append(y)
                        z_positions[k].append(z)
                        if x >=-0.05 and x<= 0.05:
                            dis_x = distance([x,y],[0,-0.27])
                            if dis_x < inner_ellipse_a[k]:
                                inner_ellipse_a[k] = dis_x
                        if y >= -0.32 and y <= -0.22:
                            dis_y = distance([x,y],[0,-0.27])
                            if dis_y < inner_ellipse_b[k]:
                                inner_ellipse_b[k] = dis_y
    print("total points:",i)
    print("inner_ellipse_a:",inner_ellipse_a)
    print("inner_ellipse_b:",inner_ellipse_b)
    # print(x_positions)
    print("x_position:",[len(i) for i in x_positions])
    # print(y_positions)
    print("y_position:",[len(i) for i in y_positions])
    # print(z_positions)
    print("z_position:",[len(i) for i in z_positions])
    # # print(x_min,x_max)
    print("x_min:",x_min,"     x_max:",x_max)
    # # print(y_min,y_max)
    print("y_min:",y_min,"     y_max:",y_max)
    # # print(z_min,z_max)
    print("z_min:",z_min,"     z_max:",z_max)

    input("-------- Press Enter to Plot --------")
    # Creating scatter plots
    # fig = plt.figure()
    # ax = Axes3D(fig)
    # ax.scatter(x_positions, y_positions, z_positions, marker='o', s=40, label='')

    # Plot white arm
    # x_arm = [0,0.00442,0]
    # y_arm = [-0.209,-0.313228,-0.40411]
    # z_arm = [1.171,0.947534,0.535497]
    # ax.plot(x_arm,y_arm,z_arm,'ro-',linewidth=3,label='arm')

    # Set labels
    # ax.set_xlabel("X")
    # ax.set_ylabel("Y")
    # ax.set_zlabel("Z")

    # # Map to 2D 
    # plt.plot(x_positions, y_positions,'yo')
    # plt.xlabel("x")
    # plt.ylabel("y")

    # Plot 2D outer convex inner ellipse
    # x_vector = np.asarray(x_positions)
    # y_vector = np.asarray(y_positions)
    # points = np.vstack((x_vector,y_vector)).T
    # hull = ConvexHull(points)
    # hull = hull.vertices.tolist()
    # hull.append(hull[0])
    # plt.plot(points[hull,0],points[hull,1],'k:',lw=3)
    # t = np.linspace(0,2*math.pi,100)
    # plt.plot(inner_ellipse_b*np.cos(t),-0.27+inner_ellipse_a*np.sin(t),'r-',lw=2)

    #Plot 3D outer convex
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    inner_area = [0]*25
    out_area = [0]*25
    area = [0]*25
    for k in range(25):
        if inner_ellipse_a[k] == 1000.0:
            inner_ellipse_a[k] = 0
        if inner_ellipse_b[k] == 1000.0:
            inner_ellipse_b[k] = 0
        x_vector = np.asarray(x_positions[k])
        y_vector = np.asarray(y_positions[k])
        points = np.vstack((x_vector,y_vector)).T
        hull = ConvexHull(points)
        out_area[k] = (hull.volume)
        hull = hull.vertices.tolist()
        hull.append(hull[0])
        ax.plot(points[hull,0],points[hull,1], z_scape[k]+0.005, 'k:',lw=2)
        t = np.linspace(0,2*math.pi,100)
        inner_area[k] = math.pi * inner_ellipse_a[k] * inner_ellipse_b[k]
        area[k] = out_area[k] - inner_area[k]
        ax.plot(inner_ellipse_b[k] * np.cos(t),-0.27+inner_ellipse_a[k] * np.sin(t), z_scape[k]+0.005,'r-',lw=2)

    print("out_area:",out_area) 
    print("inner_area:",inner_area)
    print("area:",area)
    x_arm = [0,0.00442,0]
    y_arm = [-0.209,-0.313228,-0.40411]
    z_arm = [1.171,0.947534,0.535497]
    ax.plot(x_arm,y_arm,z_arm,'go-',linewidth=3,label='arm')

    # Plot sub_workspace cube
    x_cube = 0.25
    y_cube = -0.78
    z_cube = 0.79
    dx_cube = 0.15
    dy_cube = 0.82
    dz_cube = 0.34
    xx = [x_cube, x_cube, x_cube+dx_cube, x_cube+dx_cube, x_cube]
    yy = [y_cube, y_cube+dy_cube, y_cube+dy_cube, y_cube, y_cube]
    kwargs = {'alpha': 1, 'color': 'yellow'}
    ax.plot3D(xx, yy, [z_cube]*5, **kwargs)
    ax.plot3D(xx, yy, [z_cube+dz_cube]*5, **kwargs)
    ax.plot3D([x_cube, x_cube], [y_cube, y_cube], [z_cube, z_cube+dz_cube], **kwargs)
    ax.plot3D([x_cube, x_cube], [y_cube+dy_cube, y_cube+dy_cube], [z_cube, z_cube+dz_cube], **kwargs)
    ax.plot3D([x_cube+dx_cube, x_cube+dx_cube], [y_cube+dy_cube, y_cube+dy_cube], [z_cube, z_cube+dz_cube], **kwargs)
    ax.plot3D([x_cube+dx_cube, x_cube+dx_cube], [y_cube, y_cube], [z_cube, z_cube+dz_cube], **kwargs)
    plt.show()

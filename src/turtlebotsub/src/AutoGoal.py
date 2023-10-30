#!/usr/bin/env python
import rospy
import numpy as np
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from time import sleep
PI = 3.1415926535897
flag = False
rotation = False
def posedata(data, autogoal):
    global flag, rotation
    if flag == True:
        exit()
    location = Pose()
    location = data
    
    
    distance_to_goal = np.sqrt((x_to_Goal - location.x)**2 + (y_to_Goal - location.y)**2)
    
    
    angle_to_goal = np.arctan2(y_to_Goal - location.y, x_to_Goal - location.x)
    required_rotation = angle_to_goal - location.theta
    #'''
    Command = Twist()
    
    if  rotation == False:
        if required_rotation < 0.001 and required_rotation > -0.001:
            Command.angular.z = 0
            autogoal.publish(Command)
            rotation = True
        if required_rotation > PI:
            required_rotation -= 2*PI
        elif required_rotation < -PI:
            required_rotation += 2*PI
        Command.angular.z = required_rotation
        autogoal.publish(Command)
    else:
        Command.angular.z = 0
        autogoal.publish(Command)
    
    if rotation == True and flag == False:
            if distance_to_goal < 0.01:
                Command.linear.x = 0
                autogoal.publish(Command)
                print("Goal Reached")
                sleep(2)
                flag = True
                exit()
            else:
                Command.linear.x = distance_to_goal
                autogoal.publish(Command)
             #'''
def autogo():
    global x_to_Goal, y_to_Goal 
    print("Starting Autogoal")
    x_to_Goal = input("Enter X coordinate: ")
    x_to_Goal = float(x_to_Goal)
    while x_to_Goal > 10.5 or x_to_Goal < 0.5:
        if x_to_Goal > 10.5:
            print("x coordinate too large")
            x_to_Goal = input("Enter X coordinate: ")
            x_to_Goal = float(x_to_Goal)
        elif x_to_Goal < 0.5:
            print("x coordinate too small")
            x_to_Goal = input("Enter X coordinate: ")
            x_to_Goal = float(x_to_Goal)
    y_to_Goal = input("Enter Y coordinate: ")
    y_to_Goal = float(y_to_Goal)
    while y_to_Goal > 10.5 or y_to_Goal < 0.5:
        if y_to_Goal > 10.5:
            print("y coordinate too large")
            y_to_Goal = input("Enter Y coordinate: ")
            y_to_Goal = float(y_to_Goal)
        elif y_to_Goal < 0.5:
            print("y coordinate too small")
            y_to_Goal = input("Enter Y coordinate: ")
            y_to_Goal = float(y_to_Goal)
    rospy.init_node('autogoal', anonymous=True)

    autogoal = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)

    rospy.Subscriber('/turtle1/pose', Pose, posedata, autogoal)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        autogo()
    except rospy.ROSInterruptException:
        pass

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
    if flag == True: # checks if the goal is reached
        exit()
    location = Pose()
    location = data
    
    
    distance_to_goal = np.sqrt((x_to_Goal - location.x)**2 + (y_to_Goal - location.y)**2) # calculates the distance to the goal
    
    
    angle_to_goal = np.arctan2(y_to_Goal - location.y, x_to_Goal - location.x) # calculates the angle to the goal
    required_rotation = angle_to_goal - location.theta # calculates the required rotation to the goal
    #'''
    Command = Twist()
    
    if  rotation == False: # checks if the robot is not facing the goal
        if required_rotation < 0.001 and required_rotation > -0.001: # checks if the robot is facing the goal
            Command.angular.z = 0
            autogoal.publish(Command)
            rotation = True
        if required_rotation > PI: # checks if the required rotation is greater than PI
            required_rotation -= 2*PI 
        elif required_rotation < -PI: # checks if the required rotation is less than -PI 
            required_rotation += 2*PI
        Command.angular.z = required_rotation
        autogoal.publish(Command) # publishes the angular velocity to the robot
    else:
        Command.angular.z = 0 # sets the angular velocity to 0
        autogoal.publish(Command) # publishes the angular velocity to the robot
    
    if rotation == True and flag == False: # checks if the robot is facing the goal and the goal is not reached
            if distance_to_goal < 0.01: # checks if the robot arrived at the goal
                Command.linear.x = 0 # sets the linear velocity to 0
                autogoal.publish(Command) # publishes the linear velocity to the robot
                print("Goal Reached") # prints "Goal Reached"
                sleep(2)
                flag = True # sets the flag to True to exit the program
                exit()
            else:
                Command.linear.x = distance_to_goal 
                autogoal.publish(Command)
             #'''
def autogo():
    global x_to_Goal, y_to_Goal  
    print("Starting Autogoal")  
    x_to_Goal = input("Enter X coordinate: ") # gets the x coordinate of the goal from the user
    x_to_Goal = float(x_to_Goal) # converts the x coordinate to float
    while x_to_Goal > 10.5 or x_to_Goal < 0.5: # checks if the x coordinate is within the range
        if x_to_Goal > 10.5: # checks if the x coordinate is greater than 10.5
            print("x coordinate too large")  # prints "x coordinate too large"
            x_to_Goal = input("Enter X coordinate: ") # gets the x coordinate of the goal from the user
            x_to_Goal = float(x_to_Goal) # converts the x coordinate to float
        elif x_to_Goal < 0.5: # checks if the x coordinate is less than 0.5
            print("x coordinate too small") # prints "x coordinate too small"
            x_to_Goal = input("Enter X coordinate: ") # gets the x coordinate of the goal from the user
            x_to_Goal = float(x_to_Goal) # converts the x coordinate to float
    y_to_Goal = input("Enter Y coordinate: ") # gets the y coordinate of the goal from the user
    y_to_Goal = float(y_to_Goal) # converts the y coordinate to float
    while y_to_Goal > 10.5 or y_to_Goal < 0.5: # checks if the y coordinate is within the range
        if y_to_Goal > 10.5: # checks if the y coordinate is greater than 10.5
            print("y coordinate too large") # prints "y coordinate too large"
            y_to_Goal = input("Enter Y coordinate: ") # gets the y coordinate of the goal from the user
            y_to_Goal = float(y_to_Goal) # converts the y coordinate to float
        elif y_to_Goal < 0.5: # checks if the y coordinate is less than 0.5
            print("y coordinate too small")
            y_to_Goal = input("Enter Y coordinate: ")
            y_to_Goal = float(y_to_Goal) # converts the y coordinate to float
    rospy.init_node('autogoal', anonymous=True) # initializes the node

    autogoal = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) # creates the publisher variable for cmd_vel

    rospy.Subscriber('/turtle1/pose', Pose, posedata, autogoal) # creates the subscriber for the pose node

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        autogo()
    except rospy.ROSInterruptException:
        pass

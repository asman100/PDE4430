#!/usr/bin/env python
import rospy
import numpy as np
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from time import sleep
import os
flag = False
def posedata(data, collisionavoid): # callback function for pose subscriber
    Command = Twist()
    location = Pose()
    location = data
    if location.x <= 0.5 or location.x >= 10.5 or location.y <= 0.5 or location.y >= 10.5: # checks if turtle is within the boundaries
        Command.linear.x = 0 # stops turtle
        Command.angular.z = 0 # stops turtle
        collisionavoid.publish(Command)
        print("Collision Detected") # prints collision detected
        exit()

def autogo():
    
    rospy.init_node('collisionavoid', anonymous=True) # initializes node

    collisionavoid = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) # publisher for turtle1/cmd_vel

    rospy.Subscriber('/turtle1/pose', Pose, posedata, collisionavoid) # subscriber for turtle1/pose

    rate = rospy.Rate(1000)  
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        autogo()
    except rospy.ROSInterruptException:
        pass

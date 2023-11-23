#!/usr/bin/env python
# for the rest of roomba helper 2,3,4,5 the code is the same except for the sequences therefore assume the same comments apply to all of them
import rospy
import numpy as np
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from time import sleep
import sys
flag = True
start = True
seq1 = [(0.5, 0.5),(10.5,0.5),(10.5,1.5),(0.5,1.5),(0.5,0.5)] # 1st sequence
seq2 = [(0.5, 3),(0.5,2.5),(10.5,2.5),(10.5,3.5),(0.5,3.5),(0.5,4.5),(10.5,4.5)] # 2nd sequence
seq3 = [(0.5, 5.5),(10.5,5.5),(5.5,5.5)] # 3rd sequence
seq4 = [(0.5, 8),(0.5,8.5),(10.5,8.5),(10.5,7.5),(0.5,7.5),(0.5,6.5),(10.5,6.5)] # 4th sequence
seq5 = [(0.5, 10.5),(10.5,10.5),(10.5,9.5),(0.5,9.5),(0.5,10.5)] # 5th sequence
Mother_seq = (seq1,seq2,seq3,seq4,seq5) # all sequences
myseq = []
actseq = []
target = None
PI = 3.1415926535897
AllSequences = [seq1,seq2,seq3,seq4,seq5] # copy of all sequences
rotation = False

def Target_Position(index, Vacuum):
    global actseq
    actseq = Mother_seq[index.data] # gets the sequence from the index
    
 
def posedata(data, Vacuum):
    global flag , actseq, start, myseq, target, rotation
    
    if len(actseq) == 0: # checks if the sequence is empty
        exit()
    
    if start == True: # checks if the program is running for the first time
        myseq = actseq
        start = False
    
    
    location = Pose()
    location = data
    if flag == True: # checks if the robot arrived at location
        if myseq:  # checks if myseq is not empty
            target = myseq.pop(0)
            print(target)
            flag = False
            rotation = False
        else:
            print("myseq is empty, cannot pop element")
        
    
    if target:
        
        distance_to_goal = np.sqrt((target[0] - location.x)**2 + (target[1] - location.y)**2) # calculates the distance to the goal
    
    
        angle_to_goal = np.arctan2(target[1] - location.y, target[0] - location.x) # calculates the angle to the goal
        required_rotation = angle_to_goal - location.theta # calculates the required rotation to the goal
   
        Command = Twist()
    
        if  rotation == False:
            if required_rotation < 0.001 and required_rotation > -0.001: # checks if the robot is facing the goal
                Command.angular.z = 0
                Vacuum.publish(Command)
                rotation = True
            if required_rotation > PI: # checks if the angle to goal is more that 180 degrees and corrects it to be less than 180 degrees
                required_rotation -= 2*PI
            elif required_rotation < -PI: # checks if the angle to goal is less that -180 degrees and corrects it to be positive
                required_rotation += 2*PI
            Command.angular.z = required_rotation # rotates the robot to face the goal
            Vacuum.publish(Command)
        else:
            Command.angular.z = 0
            Vacuum.publish(Command)
        
        if rotation == True and flag == False: # checks if the robot is facing the goal and if it arrived at the location
                if distance_to_goal < 0.01: # checks if the robot arrived at the location
                    Command.linear.x = 0
                    Vacuum.publish(Command)
                    sleep(2)
                    flag = True
                    if(len(myseq) == 0):
                        sys.exit() # exits the program if the sequence is empty
                else:
                    Command.linear.x = distance_to_goal  # moves the robot to the goal
                    Vacuum.publish(Command)
def autonav():
    global x_to_Goal, y_to_Goal 
    rospy.init_node('RoombaHelper1', anonymous=True) # initializes the node
    Vacuum = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) # creates the publisher variable for the vacuum
    rospy.Subscriber('/Roomba_Helper_1', Int32, Target_Position, Vacuum ) # creates the subscriber for the helper node
    rospy.Subscriber('/turtle1/pose', Pose, posedata, Vacuum) # creates the subscriber for the pose node

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        autonav()
    except rospy.ROSInterruptException:
        pass

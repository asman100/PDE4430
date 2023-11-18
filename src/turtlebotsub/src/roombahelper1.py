#!/usr/bin/env python
import rospy
import numpy as np
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from time import sleep
import sys
flag = True
start = True
seq1 = [(0.5, 0.5),(10.5,0.5),(10.5,1.5),(0.5,1.5),(0.5,0.5)]
seq2 = [(0.5, 3),(0.5,2.5),(10.5,2.5),(10.5,3.5),(0.5,3.5),(0.5,4.5),(10.5,4.5)]
seq3 = [(0.5, 5.5),(10.5,5.5),(5.5,5.5)]
seq4 = [(0.5, 8),(0.5,8.5),(10.5,8.5),(10.5,7.5),(0.5,7.5),(0.5,6.5),(10.5,6.5)]
seq5 = [(0.5, 10.5),(10.5,10.5),(10.5,9.5),(0.5,9.5),(0.5,10.5)]
Mother_seq = (seq1,seq2,seq3,seq4,seq5)
myseq = []
actseq = []
target = None
PI = 3.1415926535897
AllSequences = [seq1,seq2,seq3,seq4,seq5]
rotation = False

def Target_Position(index, Vacuum):
    global actseq
    actseq = Mother_seq[index.data]
    
 
def posedata(data, Vacuum):
    global flag , actseq, start, myseq, target, rotation
    
    if len(actseq) == 0:
        exit()
    
    if start == True:
        myseq = actseq
        start = False
    
    
    location = Pose()
    location = data
    if flag == True:
        if myseq:  # checks if myseq is not empty
            target = myseq.pop(0)
            print(target)
            flag = False
            rotation = False
        else:
            print("myseq is empty, cannot pop element")
        
    
    if target:
        
        distance_to_goal = np.sqrt((target[0] - location.x)**2 + (target[1] - location.y)**2)
    
    
        angle_to_goal = np.arctan2(target[1] - location.y, target[0] - location.x)
        required_rotation = angle_to_goal - location.theta
   
        Command = Twist()
    
        if  rotation == False:
            if required_rotation < 0.001 and required_rotation > -0.001:
                Command.angular.z = 0
                Vacuum.publish(Command)
                rotation = True
            if required_rotation > PI:
                required_rotation -= 2*PI
            elif required_rotation < -PI:
                required_rotation += 2*PI
            Command.angular.z = required_rotation
            Vacuum.publish(Command)
        else:
            Command.angular.z = 0
            Vacuum.publish(Command)
        
        if rotation == True and flag == False:
                if distance_to_goal < 0.01:
                    Command.linear.x = 0
                    Vacuum.publish(Command)
                    sleep(2)
                    flag = True
                    if(len(myseq) == 0):
                        sys.exit()
                else:
                    Command.linear.x = distance_to_goal
                    Vacuum.publish(Command)
def autonav():
    global x_to_Goal, y_to_Goal 
    rospy.init_node('RoombaHelper1', anonymous=True)
    Vacuum = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.Subscriber('/Roomba_Helper_1', Int32, Target_Position, Vacuum )
    rospy.Subscriber('/turtle1/pose', Pose, posedata, Vacuum)

    rate = rospy.Rate(10)  # 10 Hz
    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        autonav()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python
import curses
import rospy
from geometry_msgs.msg import Twist
import time
PI = 3.1415926535897
screen = curses.initscr() 
curses.noecho()
curses.cbreak()
screen.keypad(True)
stdscr = curses.initscr() 

def teleoperation(): #function to control the turtlebot by teleoperation
    rospy.init_node('telecontrol', anonymous=True) #initializes the node
    teleop = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) #publishes to the topic /turtle1/cmd_vel
    ctrl = Twist()
    rate = rospy.Rate(10) 
    
    speed = 0

    stdscr.addstr(0, 0, "Use the arrow keys to move the turtle. Press + to increase speed and - to decrease speed. Press q to quit.") #displays instructions on the terminal
    stdscr.refresh() #refreshes the terminal

     
    ctrl.linear.y = 0  
    ctrl.linear.z = 0
    ctrl.angular.x = 0
    ctrl.angular.y = 0
    while not rospy.is_shutdown(): #while the node is running
        key = screen.getch() #gets the key pressed
        if key == ord('+'): #if the key pressed is +, the speed increases by .5
            ctrl.angular.z = 0
            ctrl.linear.x = 0
            speed += .5
            print("\nSpeed is now: "+str(speed)+"\n")
        elif key == ord('-'): #if the key pressed is -, the speed decreases by .5
            ctrl.angular.z = 0
            ctrl.linear.x = 0
            if speed == 0:
                speed = 0
            else:
                speed -= .5
            print("\nSpeed is now: "+str(speed)+"\n")
        elif key == curses.KEY_UP: #if the key pressed is the up arrow, the turtle moves forward
            ctrl.angular.z = 0
            ctrl.linear.x = abs(speed)
        elif key == curses.KEY_DOWN: #if the key pressed is the down arrow, the turtle moves backward
            ctrl.angular.z = 0
            ctrl.linear.x = -abs(speed)
        elif key == curses.KEY_LEFT: #if the key pressed is the left arrow, the turtle turns left
            ctrl.linear.x = 0
            ctrl.angular.z = PI/3
        elif key == curses.KEY_RIGHT: #if the key pressed is the right arrow, the turtle turns right
            ctrl.linear.x = 0
            ctrl.angular.z = -PI/3
        elif key == ord('q'): #if the key pressed is q, the program exits
            break
        
        teleop.publish(ctrl) #publishes the message to the topic cmd_vel
        if key == -1:   #if no key is pressed, the turtle stops
            speed = 0
            ctrl.linear.x = 0
            ctrl.angular.z = 0
        #rospy.loginfo(ctrl)
        teleop.publish(ctrl)
        rate.sleep()
        

if __name__ == '__main__':
    try:
        teleoperation()
        
    except rospy.ROSInterruptException:
        pass

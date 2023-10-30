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

def teleoperation():
    rospy.init_node('telecontrol', anonymous=True)
    teleop = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    ctrl = Twist()
    rate = rospy.Rate(10) # 10hz
    
    
    speed = 0

    stdscr.addstr(0, 0, "Use the arrow keys to move the turtle. Press + to increase speed and - to decrease speed. Press q to quit.")
    stdscr.refresh()

    tcurr = rospy.Time.now().to_sec()
    currtheta = 0 
    currdist = 0      
    ctrl.linear.y = 0 
    ctrl.linear.z = 0
    ctrl.angular.x = 0
    ctrl.angular.y = 0
    while not rospy.is_shutdown():
        key = screen.getch()
        if key == ord('+'):
            ctrl.angular.z = 0
            ctrl.linear.x = 0
            speed += .5
            print("\nSpeed is now: "+str(speed)+"\n")
        elif key == ord('-'):
            ctrl.angular.z = 0
            ctrl.linear.x = 0
            if speed == 0:
                speed = 0
            else:
                speed -= .5
            print("\nSpeed is now: "+str(speed)+"\n")
        elif key == curses.KEY_UP:
            ctrl.angular.z = 0
            ctrl.linear.x = abs(speed)
        elif key == curses.KEY_DOWN:
            ctrl.angular.z = 0
            ctrl.linear.x = -abs(speed)
        elif key == curses.KEY_LEFT:
            ctrl.linear.x = 0
            ctrl.angular.z = PI/3
        elif key == curses.KEY_RIGHT:
            ctrl.linear.x = 0
            ctrl.angular.z = -PI/3
        elif key == ord('q'):
            break
        
        teleop.publish(ctrl)
        if key == -1:  
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

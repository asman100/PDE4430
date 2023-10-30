#!/usr/bin/env python
import rospy
from turtlesim.srv import Spawn
import random

def spawn_turtle(name,x,y,theta):
    
    rospy.wait_for_service('/spawn')
    try:
        
        spawn = rospy.ServiceProxy('/spawn', Spawn)
        spawn(x, y, theta, name)
    except rospy.ServiceException as e:
        rospy.logerr(f"Service call failed: {e}")
        




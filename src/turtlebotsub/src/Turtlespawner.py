#!/usr/bin/env python
import rospy
from turtlesim.srv import Spawn

# this is a script for spawning turtles which is used by spawner helper
def spawn_turtle(name,x,y,theta): # spawn_turtle(name,x,y,theta)
    
    rospy.wait_for_service('/spawn') # wait for the service to be available
    try:
        
        spawn = rospy.ServiceProxy('/spawn', Spawn) # create a proxy for the service
        spawn(x, y, theta, name) # call the service specifiying the location and name of the turtle
    except rospy.ServiceException as e: # if the service call fails, print the error
        rospy.logerr(f"Service call failed: {e}")
        




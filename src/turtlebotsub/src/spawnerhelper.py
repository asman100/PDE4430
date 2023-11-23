#!/usr/bin/env python
import rospy
from Turtlespawner import spawn_turtle  

def main():
    rospy.init_node('Spawn_Helper') # Initialize the node to call the service spawn turtle to spawn the turtle bots at the specified locations using the turtle spawner script

    
    spawn_turtle("turtle2",0.5,0.5,0.0) # spawn_turtle(name,x,y,theta)
    spawn_turtle("turtle3",0.5,8,0.0)
    spawn_turtle("turtle4",0.5,3.0,0.0)
    spawn_turtle("turtle5",0.5,10.5,0.0)
    

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
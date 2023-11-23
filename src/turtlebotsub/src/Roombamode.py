#!/usr/bin/env python
import rospy
import numpy as np
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from turtlesim.msg import Pose
import rospy
import numpy as np

locations = [(0.5, 0.5, False), (0.5, 3, False), (0.5, 5.5, False), (0.5, 8, False), (0.5, 10.5, False)] # sets the starting locations for the roombas
unused_locations = [] # array of the unused starting locations for the roombas
start_locations = [] #  the starting locations for the roombas
Roomba1_loc = Pose()
Roomba2_loc = Pose()
Roomba3_loc = Pose()
Roomba4_loc = Pose()
Roomba5_loc = Pose()



def find_start(bot_location): # finds the ideal starting location for the roombas
    start_locations = locations.copy()  # copies the starting locations for the roombas
    unused_locations = [target for target in start_locations if not target[2]] # finds the unused starting locations for the roombas
    
    if not unused_locations: # if there are no unused starting locations for the roombas
        return None

    distances = [np.sqrt((bot_location[0] - target[0]) ** 2 + (bot_location[1] - target[1]) ** 2) for target in unused_locations] # finds the distance between the roomba and the starting locations
    min_distance_index = np.argmin(distances) # finds the index of the minimum distance
    start_point = unused_locations[min_distance_index]  # sets the starting location to the minimum distance
    start_locations[start_locations.index(start_point)] = (start_point[0], start_point[1], True) # sets the starting location to used

    return start_point


def locationname(target_location): # finds the index of the starting location
    for index, location in enumerate([(0.5, 0.5), (0.5, 3), (0.5, 5.5), (0.5, 8), (0.5, 10.5)]):
        if location == target_location:
            return index
    return -1 

def Roomba1_data(data1, Roomba1):   # finds the starting location of the roomba
    Roomba1_loc = data1 
    Roomba1_start = find_start((Roomba1_loc.x, Roomba1_loc.y))  
    Roomba1_start = (Roomba1_start[0], Roomba1_start[1]) 
    index1 = Int32()
    index1 = locationname(Roomba1_start)
    Roomba1.publish(index1)
def Roomba2_data(data2, Roomba2):  # finds the starting location of the roomba
    Roomba2_loc = data2
    Roomba2_start = find_start((Roomba2_loc.x, Roomba2_loc.y))
    Roomba2_start = (Roomba2_start[0], Roomba2_start[1])
    index2 = Int32()
    index2 = locationname(Roomba2_start)
    Roomba2.publish(index2)
def Roomba3_data(data3, Roomba3):  # finds the starting location of the roomba
    Roomba3_loc = data3
    Roomba3_start = find_start((Roomba3_loc.x, Roomba3_loc.y))
    Roomba3_start = (Roomba3_start[0], Roomba3_start[1])
    index3 = Int32()
    index3 = locationname(Roomba3_start)
    Roomba3.publish(index3)
def Roomba4_data(data4, Roomba4):  # finds the starting location of the roomba
    Roomba4_loc = data4
    Roomba4_start = find_start((Roomba4_loc.x, Roomba4_loc.y))
    Roomba4_start = (Roomba4_start[0], Roomba4_start[1])
    index4 = Int32()
    index4 = locationname(Roomba4_start)
    Roomba4.publish(index4)
def Roomba5_data(data5, Roomba5):  # finds the starting location of the roomba
    Roomba5_loc = data5
    Roomba5_start = find_start((Roomba5_loc.x, Roomba5_loc.y))
    Roomba5_start = (Roomba5_start[0], Roomba5_start[1])
    index5 = Int32()
    index5 = locationname(Roomba5_start)
    Roomba5.publish(index5)

def roombamode():
    
    rospy.init_node('Roombamode', anonymous=True) # initializes the node

    Roomba1 = rospy.Publisher('/Roomba_Helper_1', Int32, queue_size=10) # publishes the starting location of the roomba
    rospy.Subscriber('/turtle1/pose', Pose, Roomba1_data, Roomba1) # subscribes to the roomba's pose
    Roomba2 = rospy.Publisher('/Roomba_Helper_2', Int32, queue_size=10)
    rospy.Subscriber('/turtle2/pose', Pose, Roomba2_data, Roomba2)
    Roomba3 = rospy.Publisher('/Roomba_Helper_3', Int32, queue_size=10)
    rospy.Subscriber('/turtle3/pose', Pose, Roomba3_data, Roomba3)
    Roomba4 = rospy.Publisher('/Roomba_Helper_4', Int32, queue_size=10)
    rospy.Subscriber('/turtle4/pose', Pose, Roomba4_data, Roomba4)
    Roomba5 = rospy.Publisher('/Roomba_Helper_5', Int32, queue_size=10)
    rospy.Subscriber('/turtle5/pose', Pose, Roomba5_data, Roomba5)
    rospy.spin()
   

if __name__ == '__main__':
    try:
        roombamode()
    except rospy.ROSInterruptException:
        pass



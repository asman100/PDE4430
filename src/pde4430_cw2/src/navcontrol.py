#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
import math

x_array = (-0.75, 0.5, 1.7, 2, 1, -1, -2)
y_array = (2, 2, 1.2, 0, -0.5, -0.5, 0)
z_array = (0, 0, -0.45, -0.7, 1, -1, 0.7)
w_array = (1, 1, 0.9, 0.7, 0, 0, 0.7)
previous_goal = Pose()
client = None  # Declare the client globally
counter = 0


def movebase_client(msg):
    global previous_goal, client, counter, x_array, y_array, z_array, w_array
    if counter >= len(x_array):
        counter = 0
    if client is None or client.get_state() not in [
        actionlib.GoalStatus.ACTIVE,
        actionlib.GoalStatus.PENDING,
    ]:
        client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        client.wait_for_server()

        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        previous_goal = goal.target_pose.pose
        x = msg.position.x
        y = msg.position.y
        goal.target_pose.pose.position.x = x_array[counter]
        goal.target_pose.pose.position.y = y_array[counter]

        goal.target_pose.pose.orientation.w = w_array[counter]
        goal.target_pose.pose.orientation.z = z_array[counter]
        client.send_goal(goal)
        counter += 1
    else:
        rospy.loginfo("Goal is still active; waiting for it to complete.")


def main():
    global client
    rospy.init_node("movebase_client_py")
    rospy.Subscriber("patrol", Pose, movebase_client)
    rospy.spin()


if __name__ == "__main__":
    main()

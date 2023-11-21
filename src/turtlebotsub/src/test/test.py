
import rospy
from std_msgs.msg import String

def publisher_node():
    # Initialize the ROS node
    rospy.init_node('pde4432', anonymous=True)

    # Create a publisher object
    pub = rospy.Publisher('hello', String, queue_size=10)

    # Set the publishing rate (in Hz)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # Create a message object
        msg = String()
        msg.data = "Hello, world!"

        # Publish the message
        pub.publish(msg)

        # Sleep to maintain the publishing rate
        rate.sleep()

if __name__ == '__main__':
    try:
        publisher_node()
    except rospy.ROSInterruptException:
        pass

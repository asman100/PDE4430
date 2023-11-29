import rospy
from std_msgs.msg import Float32, Int16

def rpm(motor1):
    # Process data from topic1
    print(motor1.data)
    pass

def rpm0(motor2):
    # Process data from topic2
    print(motor2.data)
    pass

def ultrasonic(dist):
    # Process data from topic3
    print(dist.data)
    pass

def publisher():
    rospy.init_node('publisher_node', anonymous=True)
    rospy.Subscriber('rpm1', Float32, rpm)
    rospy.Subscriber('rpm2', Float32, rpm0)
    rospy.Subscriber('distance', Float32, ultrasonic)
    pub = rospy.Publisher('output_topic', Int16, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # Publish data to output_topic
        

        rate.sleep()

if __name__ == '__main__':
    try:
        
        publisher()
    except rospy.ROSInterruptException:
        pass

def kalman_filter(state_estimate, estimate_error, measurement, measurement_error):
    # Kalman Gain
    kalman_gain = estimate_error / (estimate_error + measurement_error)

    # Updated State Estimate
    updated_state_estimate = state_estimate + kalman_gain * (measurement - state_estimate)

    # Updated Estimate Error
    updated_estimate_error = (1 - kalman_gain) * estimate_error

    return updated_state_estimate, updated_estimate_error
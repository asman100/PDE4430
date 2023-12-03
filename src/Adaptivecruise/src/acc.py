import rospy
from std_msgs.msg import Float32, Int16
import numpy as np

lasttime = 0
lastdist = 0
speed = 0


class KalmanFilter:
    def __init__(
        self,
        initial_state,
        initial_estimate_error,
        process_variance,
        measurement_variance,
    ):
        self.state = initial_state
        self.estimate_error = initial_estimate_error
        self.process_variance = process_variance
        self.measurement_variance = measurement_variance

    def update(self, measurement):
        predicted_state = self.state
        predicted_estimate_error = self.estimate_error + self.process_variance

        kalman_gain = predicted_estimate_error / (
            predicted_estimate_error + self.measurement_variance
        )
        self.state = predicted_state + kalman_gain * (measurement - predicted_state)
        self.estimate_error = (1 - kalman_gain) * predicted_estimate_error

        return self.state


initial_state = 0
initial_estimate_error = 1
process_variance = 0.1
measurement_variance = 1
kf = KalmanFilter(
    initial_state, initial_estimate_error, process_variance, measurement_variance
)


def rpm(motor1):
    print(motor1.data)
    pass


def rpm0(motor2):
    print(motor2.data)
    pass


def ultrasonic(dist):
    global lasttime, lastdist, speed
    currdist = kf.update(dist.data)
    now = rospy.get_rostime()
    speed = (currdist - lastdist) / (now.secs - lasttime)
    lasttime = now.secs
    lastdist = dist.data

    pass


def publisher():
    rospy.init_node("publisher_node", anonymous=True)
    rospy.Subscriber("rpm1", Float32, rpm)
    rospy.Subscriber("rpm2", Float32, rpm0)
    rospy.Subscriber("distance", Float32, ultrasonic)
    pub = rospy.Publisher("output_topic", Int16, queue_size=10)
    rate = rospy.Rate(60)  # 10 Hz

    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == "__main__":
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass

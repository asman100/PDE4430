import rospy
from std_msgs.msg import Float32, Int16, Float32MultiArray
import numpy as np

lasttime = 0
lastdist = 0
speed = 0
PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286
radius = 2.59
motor1speed = 0
motor2speed = 0
pwm = 0
goal_speed = 0
kp = 0.5  # Proportional constant
ki = 0.2  # Integral constant
kd = 0.1  # Derivative constant
last_error = 0
integral = 0
# Motor control limits
min_speed = 0  # Minimum motor speed
max_speed = 255  # Maximum motor speed


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


def calculate_pid(error):
    global integral, last_error

    # Proportional term
    p = kp * error

    # Integral term
    integral += error
    i = ki * integral

    # Derivative term
    derivative = error - last_error
    d = kd * derivative

    # Calculate the PID output
    output = p + i + d

    # Update the error and return the PID output
    last_error = error
    return output


def control_motor(pid_output):
    # Apply motor control limits
    speed = int(pid_output)
    if goal_speed == 0:
        speed = 0
    elif goal_speed > speed:
        speed = min_speed
    elif goal_speed < speed:
        speed = max_speed
    return speed


initial_state = 0
initial_estimate_error = 1
process_variance = 0.1
measurement_variance = 1
kf = KalmanFilter(
    initial_state, initial_estimate_error, process_variance, measurement_variance
)


def rpm(motor1):
    global motor1speed
    global motor2speed
    motor1speed = motor1.data[0] * 2 * radius * PI / 60
    motor2speed = motor1.data[1] * 2 * radius * PI / 60
    motor(pub)
    pass


def ultrasonic(dist):
    global lasttime, lastdist, speed
    currdist = kf.update(dist.data)
    now = rospy.get_rostime()

    speed = (currdist - lastdist) / ((now.secs - lasttime) / 1e9)
    speed = int(-speed)

    lasttime = now.nsecs
    lastdist = dist.data

    pass


def motor(pub):
    global motor1speed, motor2speed, speed, pwm, goal_speed
    carspeed = (motor1speed + motor2speed) / 2
    goal_speed = speed + carspeed
    pid_output = calculate_pid(speed)
    pwm = control_motor(pid_output)

    print(pwm)

    pub.publish(pwm)


def publisher():
    rospy.init_node("publisher_node", anonymous=True)
    rospy.Subscriber("rpm1", Float32MultiArray, rpm)

    rospy.Subscriber("distance", Float32, ultrasonic)
    global pub
    pub = rospy.Publisher("output_topic", Int16, queue_size=10)
    rate = rospy.Rate(10)  # 10 Hz
    motor(pub)
    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == "__main__":
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass

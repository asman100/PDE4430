#!/usr/bin/env python
import rospy
from std_msgs.msg import Float32, Int16, Float32MultiArray
import numpy as np
import time

lasttime = 0
lastdist = 0
currdist = 0
speed = 0
PI = 3.141592653589793238462643383279502884197169399375105820974944592307816406286
radius = 2.59
motor1speed = 0
motor2speed = 0
pwm = 0
goal_speed = 0

last_error = 0
flag = 0

min_speed = 0
max_speed = 255
global pub


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


class Car:
    def __init__(self, speed=0):
        self.speed = speed

    def update_speed(self, object_speed, proportional_gain=0.1):
        error = object_speed - self.speed
        if error <= 0 or int(currdist) < 10:
            pwm_signal = 255
        else:
            control_signal = proportional_gain * error

            self.speed += control_signal

            pwm_signal = max(50, min(int(120 - (self.speed * 2.55)), 120))

        return pwm_signal


my_car = Car(0)
initial_state = 10
initial_estimate_error = 1.0
process_variance = 10
measurement_variance = 10
kf = KalmanFilter(
    initial_state, initial_estimate_error, process_variance, measurement_variance
)


def rpm(motor1):
    global pub
    global motor1speed
    global motor2speed
    motor1speed = motor1.data[0] * 2 * radius * PI / 60
    motor2speed = motor1.data[1] * 2 * radius * PI / 60
    my_car.speed = (motor1speed + motor2speed) / 2
    motor(pub)
    pass


def ultrasonic(dist):
    global lasttime, lastdist, speed, flag, initial_state, pwm, motor1speed, currdist
    if flag == 0:
        lastdist = kf.update(dist.data)
        lasttime = time.time()
        flag = 1
    else:
        currdist = kf.update(dist.data)

        current_time = time.time()
        currdist = currdist // 1
        speed = (currdist - lastdist) / ((current_time - lasttime))
        speed = int(speed)
        print("speed: " + str(speed) + "cm/s")
        print("\n dist: " + str(currdist) + "cm")
        print("\n pwm: " + str(pwm))
        print("\n motor1speed: " + str(motor1speed))
        lasttime = current_time

        lastdist = dist.data // 1


def motor(pub):
    global motor1speed, motor2speed, speed, pwm, goal_speed
    carspeed = (motor1speed + motor2speed) / 2
    goal_speed = speed + carspeed
    pwm = my_car.update_speed(goal_speed)
    # print(pwm)
    pub.publish(pwm)


def publisher():
    rospy.init_node("publisher_node", anonymous=True)
    rospy.Subscriber("rpm1", Float32MultiArray, rpm)

    rospy.Subscriber("distance", Float32, ultrasonic)
    global pub
    pub = rospy.Publisher("motor", Int16, queue_size=10)

    rate = rospy.Rate(40)
    motor(pub)
    while not rospy.is_shutdown():
        rate.sleep()


if __name__ == "__main__":
    try:
        publisher()
    except rospy.ROSInterruptException:
        pass

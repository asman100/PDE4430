#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64
import sys, select, termios, tty

msg = """
Control Your Robot!
---------------------------
Moving around:
   -    w   -
   a    s    d

i/k : increase/decrease linear velocity
j/l : increase/decrease angular velocity
space key, k : force stop

CTRL-C to quit
"""

moveBindings = {
    "w": (1, 0),
    "a": (0, 1),
    "d": (0, -1),
    "s": (-1, 0),
}


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def vels(speed, turn):
    return "currently:\tspeed %s\tturn %s " % (speed, turn)


if __name__ == "__main__":
    settings = termios.tcgetattr(sys.stdin)

    rospy.init_node("teleop_twist_keyboard")

    speed = rospy.get_param("~speed", 0.5)
    turn = rospy.get_param("~turn", 3.0)
    x = 0
    th = 0
    status = 0

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    increase_pub = rospy.Publisher(
        "/joint1_position_controller/command", Float64, queue_size=1
    )
    decrease_pub = rospy.Publisher(
        "/joint2_position_controller/command", Float64, queue_size=1
    )
    try:
        print(msg)
        while 1:
            key = getKey()
            if key in moveBindings.keys():
                x = moveBindings[key][0]
                th = moveBindings[key][1]
            elif key == "+":
                increase_pub.publish(0.8)
                decrease_pub.publish(-0.8)
            elif key == "-":
                increase_pub.publish(0)
                decrease_pub.publish(0)
            elif key == " " or key == "s":
                x = 0
                th = 0
            else:
                if key == "\x03":
                    break

            twist = Twist()
            twist.linear.x = x * speed
            twist.angular.z = th * turn
            pub.publish(twist)

    except Exception as e:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0
        twist.angular.z = 0
        pub.publish(twist)
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

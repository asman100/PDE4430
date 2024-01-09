#!/usr/bin/env python
import rospy
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped, Point
from std_msgs.msg import Header
import tf2_msgs.msg


def transform_point(point_3d, from_frame, to_frame, tf_buffer):
    """
    Transform a point from one frame to another frame.
    :param point_3d: The point in the 'from_frame'.
    :param from_frame: The frame in which 'point_3d' is currently.
    :param to_frame: The frame to which you want to transform 'point_3d'.
    :param tf_buffer: The tf2 buffer object used for looking up transformations.
    :return: Transformed point in the 'to_frame'.
    """
    try:
        now = rospy.Time.now()
        tf_buffer.can_transform(to_frame, from_frame, now, rospy.Duration(1.0))
        transform = tf_buffer.lookup_transform(to_frame, from_frame, now)
    except (
        tf2_ros.LookupException,
        tf2_ros.ConnectivityException,
        tf2_ros.ExtrapolationException,
    ) as e:
        rospy.logerr("Transform error: %s", e)
        return None

    # Transform the point
    transformed_point = tf2_geometry_msgs.do_transform_point(
        PointStamped(
            header=Header(frame_id=from_frame),
            point=Point(*point_3d),
        ),
        transform,
    ).point

    return transformed_point.x, transformed_point.y, transformed_point.z


def main():
    rospy.init_node("transform_node")

    # Initialize the tf2 buffer
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    rospy.sleep(1)  # Wait for 2 seconds to ensure all transforms are available

    # Example values for the ball's position in camera frame
    x_camera, y_camera, z_camera = 1.0, 2.0, 3.0  # Replace with actual values

    # Transform the ball's coordinates to the world frame
    ball_world_pose = transform_point(
        (x_camera, y_camera, z_camera), "kinnect_link", "map", tf_buffer
    )

    if ball_world_pose:
        print(
            "Ball's position in the world frame: x={}, y={}, z={}".format(
                *ball_world_pose
            )
        )
    else:
        print("Failed to transform point")


if __name__ == "__main__":
    main()

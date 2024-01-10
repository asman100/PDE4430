#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image, PointCloud2
from cv_bridge import CvBridge, CvBridgeError
import message_filters
import sensor_msgs.point_cloud2 as pc2
import rospy
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import PointStamped, Point, Pose
from std_msgs.msg import Header
import tf2_msgs.msg


def pat(patpub):
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        pose = Pose()
        pose.position.x = 0.0
        pose.position.y = 1000.0

        patpub.publish(pose)
        rate.sleep()


def transform_point(point_3d, from_frame, to_frame, tf_buffer):
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


def detect_circles(cv_image, depth_image):
    # Convert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2, 2)

    # Apply Hough transform on the blurred image
    detected_circles = cv2.HoughCircles(
        gray_blurred,
        cv2.HOUGH_GRADIENT,
        1,
        20,
        param1=50,
        param2=30,
        minRadius=1,
        maxRadius=100,
    )

    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Extract the depth value at the center of the circle
            depth = depth_image[b, a]

            # Print or store the 2D and depth coordinates of the center of the circle

            # Draw the circle on the image
            cv2.circle(cv_image, (a, b), r, (0, 255, 0), 2)
            cv2.circle(cv_image, (a, b), 1, (0, 0, 255), 3)
            return cv_image, (a, b), r  # Return the first detected circle

    return cv_image, None, None


def detect_circle_and_get_3d_coord(rgb_image, depth_image, point_cloud):
    processed_image, circle_center, radius = detect_circles(rgb_image, depth_image)

    if circle_center is not None:
        x, y = circle_center
        # Use depth image to get depth at the center of the circle
        depth = depth_image[y, x]

        # Convert 2D depth image coordinates to 3D point cloud coordinates
        gen = pc2.read_points(
            point_cloud, field_names=("x", "y", "z"), skip_nans=True, uvs=[[x, y]]
        )
        point_3d = next(gen)
        x = point_3d[0]

        return processed_image, point_3d  # This is a tuple (x, y, z)

    return processed_image, None


def callback(rgb_msg, depth_msg, point_cloud_msg):
    bridge = CvBridge()
    try:
        # Convert the ROS Image messages to OpenCV format
        cv_image = bridge.imgmsg_to_cv2(rgb_msg, "bgr8")
        depth_image = bridge.imgmsg_to_cv2(depth_msg, "32FC1")
    except CvBridgeError as e:
        rospy.logerr(e)
        return

    # Process to get 3D coordinates
    processed_image, point_3d = detect_circle_and_get_3d_coord(
        cv_image, depth_image, point_cloud_msg
    )
    if point_3d is not None:
        tf_buffer = tf2_ros.Buffer()
        listener = tf2_ros.TransformListener(tf_buffer)
        rospy.sleep(2)

        x_camera, y_camera, z_camera = point_3d  # Replace with actual values
        ball_world_pose = transform_point(
            (z_camera, x_camera, y_camera), "kinnect_link", "map", tf_buffer
        )
        if ball_world_pose:
            print(
                "Ball's position in the world frame: x={}, y={}, z={}".format(
                    *ball_world_pose
                )
            )
        # Display the processed image with the detected circle
        cv2.imshow("Detected Circle", processed_image)
        cv2.waitKey(1)


def main():
    rospy.init_node("circle_detection_3d_node", anonymous=True)

    rgb_sub = message_filters.Subscriber("/kinnect/color/image_raw", Image)
    depth_sub = message_filters.Subscriber("/kinnect/depth/image_raw", Image)
    pc_sub = message_filters.Subscriber("/kinnect/depth/points", PointCloud2)
    patrol_publisher = rospy.Publisher("patrol", Pose, queue_size=10)
    pat(patrol_publisher)
    ts = message_filters.ApproximateTimeSynchronizer(
        [rgb_sub, depth_sub, pc_sub], 10, 0.1
    )
    ts.registerCallback(callback)

    # Initialize the tf2 buffer
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    rospy.sleep(1)  # Wait for 2 seconds to ensure all transforms are available

    # Example values for the ball's position in camera frame

    # Transform the ball's coordinates to the world frame

    rospy.spin()


if __name__ == "__main__":
    main()

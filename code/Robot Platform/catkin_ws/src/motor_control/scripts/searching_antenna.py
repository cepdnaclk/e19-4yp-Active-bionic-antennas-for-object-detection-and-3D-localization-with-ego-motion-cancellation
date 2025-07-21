#!/usr/bin/env python3

import time
import math
import rospy
from geometry_msgs.msg import Vector3Stamped
from adafruit_servokit import ServoKit

PAN_CHANNEL_RIGHT = 0
TILT_CHANNEL_RIGHT = 1
CENTER_PAN = 90
CENTER_TILT = 90
PAN_AMPLITUDE = 60
TILT_AMPLITUDE = 30
BASE_FREQUENCY = 0.4

# Set update interval for 500 Hz
UPDATE_RATE = 1.0 / 500  # 0.002 seconds

def main():
    rospy.init_node("searching_antenna")
    kit = ServoKit(channels=16)
    angle_pub = rospy.Publisher('/servo_pos/antenna', Vector3Stamped, queue_size=10)

    rospy.loginfo("Start searching mode (ANTENNA) using figure-8 pattern at 500 Hz...")

    rate = rospy.Rate(1.0 / UPDATE_RATE)
    start_time = time.time()

    try:
        while not rospy.is_shutdown():
            t = time.time() - start_time

            pan_angle = CENTER_PAN + PAN_AMPLITUDE * math.cos(2 * math.pi * BASE_FREQUENCY * t)
            tilt_angle = CENTER_TILT + TILT_AMPLITUDE * math.sin(2 * math.pi * 2 * BASE_FREQUENCY * t)

            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            kit.servo[PAN_CHANNEL_RIGHT].angle = pan_angle
            kit.servo[TILT_CHANNEL_RIGHT].angle = tilt_angle

            msg = Vector3Stamped()
            msg.header.stamp = rospy.Time.now()
            msg.vector.x = pan_angle
            msg.vector.y = tilt_angle
            msg.vector.z = 0.0
            angle_pub.publish(msg)

            rate.sleep()

    except rospy.ROSInterruptException:
        rospy.loginfo("ROS Interrupt received, resetting servos and exiting...")
    except KeyboardInterrupt:
        rospy.loginfo("Keyboard Interrupt, resetting servos and exiting...")

    kit.servo[PAN_CHANNEL_RIGHT].angle = CENTER_PAN
    kit.servo[TILT_CHANNEL_RIGHT].angle = CENTER_TILT
    rospy.loginfo("Servos reset to center position.")

if __name__ == "__main__":
    main()

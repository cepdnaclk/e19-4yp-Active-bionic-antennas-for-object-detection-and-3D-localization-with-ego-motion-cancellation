#!/usr/bin/env python3

import time
import math
import rospy
from geometry_msgs.msg import Vector3Stamped
from adafruit_servokit import ServoKit

PAN_CHANNEL = 0
TILT_CHANNEL = 1
CENTER_PAN = 90
CENTER_TILT = 90
SAMPLING_RADIUS_PAN = 15
SAMPLING_RADIUS_TILT = 15
FREQUENCY = 0.8

UPDATE_RATE = 1.0 / 500  # 500Hz

def main():
    rospy.init_node("sampling_antenna")
    kit = ServoKit(channels=16)
    angle_pub = rospy.Publisher('/servo_pos/antenna', Vector3Stamped, queue_size=10)

    rospy.loginfo("Sampling mode activated")

    rate = rospy.Rate(1.0 / UPDATE_RATE)
    start_time = time.time()

    try:
        while not rospy.is_shutdown():
            t = time.time() - start_time

            pan_angle = CENTER_PAN + SAMPLING_RADIUS_PAN * math.cos(2 * math.pi * FREQUENCY * t)
            tilt_angle = CENTER_TILT + SAMPLING_RADIUS_TILT * math.sin(2 * math.pi * FREQUENCY * t)

            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            kit.servo[PAN_CHANNEL].angle = pan_angle
            kit.servo[TILT_CHANNEL].angle = tilt_angle

            msg = Vector3Stamped()
            msg.header.stamp = rospy.Time.now()
            msg.vector.x = pan_angle
            msg.vector.y = tilt_angle
            msg.vector.z = 0.0
            angle_pub.publish(msg)

            rate.sleep()

    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        pass

    kit.servo[PAN_CHANNEL].angle = CENTER_PAN
    kit.servo[TILT_CHANNEL].angle = CENTER_TILT
    rospy.loginfo("Sampling mode exited")

if __name__ == '__main__':
    main()

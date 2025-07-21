#!/usr/bin/env python3

import time
import math
import rospy
from geometry_msgs.msg import Vector3Stamped
from adafruit_servokit import ServoKit

# Servo channels
PAN_CHANNEL_RIGHT = 0
TILT_CHANNEL_RIGHT = 1

# Center positions
CENTER_PAN = 90
CENTER_TILT = 90

# Amplitudes for figure-8 motion
PAN_AMPLITUDE = 60   # Horizontal swing
TILT_AMPLITUDE = 40  # Vertical swing

# Frequency (in Hz) for base loop
BASE_FREQUENCY = 0.6

# ROS loop rate
UPDATE_RATE = 0.02  # seconds (50 Hz)

def main():
    rospy.init_node("searching antenna")
    kit = ServoKit(channels=16)

    angle_pub = rospy.Publisher('/servo_pos/antenna', Vector3Stamped, queue_size=10)

    print("Start searching mode (ANTENNA) using figure-8 pattern...")
    rate = rospy.Rate(1.0 / UPDATE_RATE)
    start_time = time.time()

    try:
        while not rospy.is_shutdown():
            t = time.time() - start_time  # time in seconds

            # Figure-8 movement pattern
            pan_angle = CENTER_PAN + PAN_AMPLITUDE * math.cos(2 * math.pi * BASE_FREQUENCY * t)
            tilt_angle = CENTER_TILT + TILT_AMPLITUDE * math.sin(2 * math.pi * 2 * BASE_FREQUENCY * t)

            # Clamp angles to [0, 180]
            pan_angle = max(0, min(180, pan_angle))
            tilt_angle = max(0, min(180, tilt_angle))

            # Send angles to servos
            kit.servo[PAN_CHANNEL_RIGHT].angle = pan_angle
            kit.servo[TILT_CHANNEL_RIGHT].angle = tilt_angle

            # Publish current angles to ROS topic
            msg = Vector3Stamped()
            msg.header.stamp = rospy.Time.now()
            msg.vector.x = pan_angle
            msg.vector.y = tilt_angle
            msg.vector.z = 0.0
            angle_pub.publish(msg)

            rate.sleep()

    except KeyboardInterrupt:
        print("\nInterrupted. Resetting servos to center...")
        kit.servo[PAN_CHANNEL_RIGHT].angle = CENTER_PAN
        kit.servo[TILT_CHANNEL_RIGHT].angle = CENTER_TILT
        print("Servos reset. Exiting.")

if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass

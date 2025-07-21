#!/usr/bin/env python
# -- coding: utf-8 --

import rospy
import subprocess
import signal
from sensor_msgs.msg import Imu
import numpy as np
import time

class ContactDetector:
    def __init__(self):
        rospy.init_node('contact_search_controller', anonymous=True)
        rospy.loginfo("Contact Search Controller Node Started")

        # Start searching_antenna.py as subprocess
        self.searching_process = subprocess.Popen(["python3", "/home/spincoders/catkin_ws/src/motor_control/scripts/searching_antenna.py"])
        rospy.loginfo("Searching antenna subprocess started")

        self.acc_x_list = []
        self.acc_y_list = []
        self.acc_z_list = []

        self.contact_detected = False
        self.min_samples = 100  # minimum samples before detection
        self.multiplier = 5.5     # threshold multiplier

        self.start_time = time.time()
        self.start_ignore_duration = 12.0  # 2 seconds ignore time from start

        rospy.Subscriber('/imu/antenna', Imu, self.imu_callback)

    def imu_callback(self, msg):
        current_time = time.time()
        elapsed_time = current_time - self.start_time

        # Skip detection for first 2 seconds
        if elapsed_time < self.start_ignore_duration:
            return

        if self.contact_detected:
            return

        acc_x = msg.linear_acceleration.x
        acc_y = msg.linear_acceleration.y
        acc_z = msg.linear_acceleration.z

        self.acc_x_list.append(abs(acc_x))
        self.acc_y_list.append(abs(acc_y))
        self.acc_z_list.append(abs(acc_z))

        count = len(self.acc_x_list)

        if count < self.min_samples:
            return

        avg_x = np.mean(self.acc_x_list)
        avg_y = np.mean(self.acc_y_list)
        avg_z = np.mean(self.acc_z_list)

        threshold_x = self.multiplier * avg_x
        threshold_y = self.multiplier * avg_y
        threshold_z = self.multiplier * avg_z

        if abs(acc_x) > threshold_x or abs(acc_y) > threshold_y or abs(acc_z) > threshold_z:
            rospy.loginfo("Contact Detected after {0:.2f}s! X:{1:.2f} Y:{2:.2f} Z:{3:.2f}".format(
                elapsed_time, acc_x, acc_y, acc_z))
            self.contact_detected = True
            self.stop_searching()

    def stop_searching(self):
        rospy.loginfo("Stopping searching antenna...")
        if self.searching_process.poll() is None:
            self.searching_process.send_signal(signal.SIGINT)
            self.searching_process.wait()
            rospy.loginfo("Servo scanning stopped after contact detection.")
        rospy.signal_shutdown("Contact detected, shutting down node.")

    def run(self):
        rospy.loginfo("Contact detection active, ignoring first {0}s of movement.".format(self.start_ignore_duration))
        rospy.spin()


if __name__ == '__main__':
    detector = ContactDetector()
    detector.run()

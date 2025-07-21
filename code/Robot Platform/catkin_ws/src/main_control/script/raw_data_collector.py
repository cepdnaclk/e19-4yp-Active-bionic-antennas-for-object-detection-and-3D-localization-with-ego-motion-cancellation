#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
import csv
import os
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped
import threading

class DataCollector:
    def __init__(self):
        rospy.init_node('data_collector', anonymous=True)

        # Data placeholders
        self.lock = threading.Lock()
        self.latest_data = {
            'imu_bottom': None,
            'imu_antenna': None,
            'servo_antenna': None,
        }

        # CSV setup
        self.filename = os.path.join(
            os.path.expanduser('~'),
            'catkin_ws', 'data', 'Case6_Move_Dataset7.csv')
        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.csv_file = open(self.filename, 'w')
        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow([
            'timestamp',
            'acc_bottom_x', 'acc_bottom_y', 'acc_bottom_z',
            'gyro_bottom_x', 'gyro_bottom_y', 'gyro_bottom_z',
            'acc_antenna_x', 'acc_antenna_y', 'acc_antenna_z',
            'gyro_antenna_x', 'gyro_antenna_y', 'gyro_antenna_z',
            'servo_antenna_pan', 'servo_antenna_tilt'
        ])

        # Subscribers
        rospy.Subscriber('/imu/bottom', Imu, self.imu_bottom_cb)
        rospy.Subscriber('/imu/antenna', Imu, self.imu_antenna_cb)
        rospy.Subscriber('/servo_pos/antenna', Vector3Stamped, self.servo_antenna_cb)

        rospy.loginfo("Data collection started. Saving to: %s", self.filename)

    def imu_bottom_cb(self, msg):
        self.update_data('imu_bottom', msg)

    def imu_antenna_cb(self, msg):
        self.update_data('imu_antenna', msg)

    def servo_antenna_cb(self, msg):
        self.update_data('servo_antenna', msg)

    def update_data(self, key, msg):
        with self.lock:
            self.latest_data[key] = msg

            # Only write row if all data types are available
            if all(self.latest_data.values()):
                self.write_row()

    def write_row(self):
        imu_bottom = self.latest_data['imu_bottom']
        imu_antenna = self.latest_data['imu_antenna']
        servo_antenna = self.latest_data['servo_antenna']

        # Use the most recent message time (from servo)
        timestamp = servo_antenna.header.stamp.to_sec()

        row = [timestamp,
               imu_bottom.linear_acceleration.x, imu_bottom.linear_acceleration.y, imu_bottom.linear_acceleration.z,
               imu_bottom.angular_velocity.x, imu_bottom.angular_velocity.y, imu_bottom.angular_velocity.z,
               imu_antenna.linear_acceleration.x, imu_antenna.linear_acceleration.y, imu_antenna.linear_acceleration.z,
               imu_antenna.angular_velocity.x, imu_antenna.angular_velocity.y, imu_antenna.angular_velocity.z,
               servo_antenna.vector.x, servo_antenna.vector.y]

        self.csv_writer.writerow(row)
        self.csv_file.flush()

        # Reset latest_data to force new complete data before writing next row
        for k in self.latest_data:
            self.latest_data[k] = None

        rospy.loginfo("Data saved at time: %.3f", timestamp)

    def run(self):
        try:
            rospy.spin()
        finally:
            self.csv_file.close()
            rospy.loginfo("CSV file closed.")

if __name__ == '__main__':
    try:
        node = DataCollector()
        node.run()
    except rospy.ROSInterruptException:
        pass

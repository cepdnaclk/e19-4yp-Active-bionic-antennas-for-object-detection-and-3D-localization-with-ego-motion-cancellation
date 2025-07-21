#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
import csv
import os
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3Stamped
from message_filters import ApproximateTimeSynchronizer, Subscriber

class DataCollector:
    def __init__(self):
        rospy.init_node('data_collector', anonymous=True)

        # Subscribers
        self.acc_right_sub = Subscriber('/imu/right', Imu)
        self.acc_left_sub = Subscriber('/imu/left', Imu)
        self.acc_base_sub = Subscriber('/imu/bottom', Imu)
        self.servo_right_sub = Subscriber('/servo_pos/right', Vector3Stamped)
        self.servo_left_sub = Subscriber('/servo_pos/left', Vector3Stamped)

        # Synchronizer
        self.ts = ApproximateTimeSynchronizer([
            self.acc_right_sub,
            self.acc_left_sub,
            self.acc_base_sub,
            self.servo_right_sub,
            self.servo_left_sub
        ], queue_size=30, slop=0.05)

        # CSV setup
        self.filename = os.path.join(
            os.path.expanduser('~'),
            'catkin_ws', 'data', 'data_no_contact_with_robot_movement.csv')
        dirname = os.path.dirname(self.filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.csv_file = open(self.filename, 'w')
        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow([
            'timestamp',
            'acc_right_x', 'acc_right_y', 'acc_right_z',
            'gyro_right_x', 'gyro_right_y', 'gyro_right_z',
            'acc_left_x', 'acc_left_y', 'acc_left_z',
            'gyro_left_x', 'gyro_left_y', 'gyro_left_z',
            'acc_base_x', 'acc_base_y', 'acc_base_z',
            'gyro_base_x', 'gyro_base_y', 'gyro_base_z',
            'servo_right_pan', 'servo_right_tilt',
            'servo_left_pan', 'servo_left_tilt'
        ])

        rospy.loginfo("Data collection started. Saving to: %s", self.filename)

    def callback(self, imu_right, imu_left, imu_base, servo_right, servo_left):
        # Use the timestamp from the right servo message (or average multiple if needed)
        timestamp = servo_right.header.stamp.to_sec()

        row = [timestamp,
               imu_right.linear_acceleration.x, imu_right.linear_acceleration.y, imu_right.linear_acceleration.z,
               imu_right.angular_velocity.x, imu_right.angular_velocity.y, imu_right.angular_velocity.z,
               imu_left.linear_acceleration.x, imu_left.linear_acceleration.y, imu_left.linear_acceleration.z,
               imu_left.angular_velocity.x, imu_left.angular_velocity.y, imu_left.angular_velocity.z,
               imu_base.linear_acceleration.x, imu_base.linear_acceleration.y, imu_base.linear_acceleration.z,
               imu_base.angular_velocity.x, imu_base.angular_velocity.y, imu_base.angular_velocity.z,
               servo_right.vector.x, servo_right.vector.y,
               servo_left.vector.x, servo_left.vector.y]

        self.csv_writer.writerow(row)
        self.csv_file.flush()

        # Debug logs
        rospy.loginfo("Data collected at timestamp: %.3f", timestamp)
        rospy.loginfo("Right IMU accel: x=%.3f, y=%.3f, z=%.3f", 
                      imu_right.linear_acceleration.x,
                      imu_right.linear_acceleration.y,
                      imu_right.linear_acceleration.z)
        rospy.loginfo("Left IMU accel: x=%.3f, y=%.3f, z=%.3f", 
                      imu_left.linear_acceleration.x,
                      imu_left.linear_acceleration.y,
                      imu_left.linear_acceleration.z)
        rospy.loginfo("Bottom IMU accel: x=%.3f, y=%.3f, z=%.3f", 
                      imu_base.linear_acceleration.x,
                      imu_base.linear_acceleration.y,
                      imu_base.linear_acceleration.z)

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

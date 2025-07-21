#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from sensor_msgs.msg import Imu
from mpu6050 import mpu6050
import smbus
import time

PCA9548A_ADDR = 0x70
MPU6050_ADDR = 0x68
I2C_BUS = 0
CHANNEL = 1  # ANTENNA IMU

def select_channel(bus, channel):
    if 0 <= channel <= 7:
        bus.write_byte(PCA9548A_ADDR, 1 << channel)
        time.sleep(0.005)
    else:
        raise ValueError("Invalid channel")

def main():
    rospy.init_node('imu_antenna_publisher', anonymous=True)
    bus = smbus.SMBus(I2C_BUS)
    select_channel(bus, CHANNEL)
    sensor = mpu6050(MPU6050_ADDR, bus=I2C_BUS)
    pub = rospy.Publisher('/imu/antenna', Imu, queue_size=10)
    rate = rospy.Rate(150)
    print("Start Accelerometer (ANTENNA)...")

    while not rospy.is_shutdown():
        try:
            select_channel(bus, CHANNEL)
            accel = sensor.get_accel_data()
            gyro = sensor.get_gyro_data()

            msg = Imu()
            msg.header.stamp = rospy.Time.now()
            msg.header.frame_id = "imu_channel_1"
            msg.linear_acceleration.x = accel['x']
            msg.linear_acceleration.y = accel['y']
            msg.linear_acceleration.z = accel['z']
            msg.angular_velocity.x = gyro['x']
            msg.angular_velocity.y = gyro['y']
            msg.angular_velocity.z = gyro['z']
            msg.orientation_covariance[0] = -1

            pub.publish(msg)
            rate.sleep()

        except Exception as e:
            rospy.logwarn("ANTENNA IMU error: %s", str(e))

if __name__ == '__main__':
    main()

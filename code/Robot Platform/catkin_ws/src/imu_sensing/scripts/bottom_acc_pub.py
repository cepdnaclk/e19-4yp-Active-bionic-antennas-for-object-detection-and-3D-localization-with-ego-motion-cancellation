#!/usr/bin/env python
# -- coding: utf-8 --

import rospy
from sensor_msgs.msg import Imu
from mpu6050 import mpu6050
import smbus
import time

PCA9548A_ADDR = 0x70
MPU6050_ADDR = 0x68
I2C_BUS = 0
CHANNEL = 2  # Bottom IMU

def select_channel(bus, channel):
    if 0 <= channel <= 7:
        bus.write_byte(PCA9548A_ADDR, 1 << channel)
        #time.sleep(0.005)
    else:
        raise ValueError("Invalid channel")

def configure_sampling(sensor):
    """Configure MPU6050 for 500 Hz sampling rate."""
    # DLPF_CFG = 0 (260 Hz bandwidth, gyro rate 8kHz)
    sensor.bus.write_byte_data(MPU6050_ADDR, 0x1A, 0x00)
    # SMPLRT_DIV = 15 → 8000 / (1 + 15) = 500 Hz sample rate
    sensor.bus.write_byte_data(MPU6050_ADDR, 0x19, 0x0F)
    rospy.loginfo("MPU6050 configured for 500 Hz sampling")

def main():
    rospy.init_node('imu_bottom_publisher', anonymous=True)
    bus = smbus.SMBus(I2C_BUS)
    select_channel(bus, CHANNEL)
    sensor = mpu6050(MPU6050_ADDR, bus=I2C_BUS)

    configure_sampling(sensor)  # Set sensor to 500Hz

    pub = rospy.Publisher('/imu/bottom', Imu, queue_size=10)
    rate = rospy.Rate(500)  # 500 Hz loop rate
    rospy.loginfo("Start Accelerometer (BOTTOM) publishing at 500 Hz...")

    while not rospy.is_shutdown():
        try:
            select_channel(bus, CHANNEL)
            accel = sensor.get_accel_data()
            gyro = sensor.get_gyro_data()

            msg = Imu()
            msg.header.stamp = rospy.Time.now()
            msg.header.frame_id = "imu_channel_2"
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
            rospy.logwarn("Bottom IMU error: %s", str(e))

if __name__ == '__main__':
    main()

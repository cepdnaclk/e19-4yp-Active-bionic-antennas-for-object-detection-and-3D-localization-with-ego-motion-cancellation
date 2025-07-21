#!/usr/bin/env python

import rospy
import serial
import time
from std_msgs.msg import String

class BaseCommunication:
    def __init__(self):
        self.serial_port = rospy.get_param("~port", "/dev/ttyACM0")
        self.baud_rate = rospy.get_param("~baud", 115200)
        self.last_command_time = time.time()
        self.command_received = False

        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            time.sleep(2)
            rospy.loginfo("Connected to Arduino on %s", self.serial_port)
        except serial.SerialException as e:
            rospy.logerr("Serial connection failed: %s", e)
            raise SystemExit

        self.sub = rospy.Subscriber("/nav/base_cmd", String, self.command_callback)
        rospy.loginfo("Subscribed to /nav/base_cmd")

        self.run()

    def command_callback(self, msg):
        cmd = msg.data.strip()
        if cmd:
            self.send_command(cmd)
            self.command_received = True
            self.last_command_time = time.time()

    def send_command(self, cmd):
        try:
            full_cmd = cmd + "\n"
            self.ser.write(full_cmd.encode())
            rospy.loginfo("Sent to Arduino: '%s'", full_cmd.strip())
        except serial.SerialException as e:
            rospy.logerr("Failed to send command: %s", e)

    def run(self):
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            time_since_last_cmd = time.time() - self.last_command_time

            if time_since_last_cmd > 5:
                self.send_command("S")

            rate.sleep()

if __name__ == "__main__":
    rospy.init_node("base_communication")
    BaseCommunication()

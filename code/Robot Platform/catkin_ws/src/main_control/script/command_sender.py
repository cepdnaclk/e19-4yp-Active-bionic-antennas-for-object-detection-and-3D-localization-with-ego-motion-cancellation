#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import time

class CommandSender:
    def __init__(self):
        rospy.init_node('command_sender', anonymous=True)
        self.pub = rospy.Publisher('/nav/base_cmd', String, queue_size=10)
        rospy.sleep(1)

    def send_command(self, cmd):
        self.pub.publish(String(cmd))
        rospy.loginfo("Published command: %s", cmd)

    def sequence_1(self):
        rospy.loginfo("Starting Sequence 1: Send 'S' until shutdown")
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.send_command("S")
            rate.sleep()

    def sequence_2(self):
        rospy.loginfo("Starting Sequence 2: Send 'S' until shutdown")
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.send_command("S")
            rate.sleep()

    def sequence_3(self):
        rospy.loginfo("Starting Sequence 3: F 200 for 16s, then S indefinitely, loop")
        rate = rospy.Rate(16)  # 16 Hz loop

        while not rospy.is_shutdown():
            # Send "F 200" for 16 seconds
            rospy.loginfo("Sending F 200 for 16 seconds")
            start_time = rospy.Time.now().to_sec()
            while (rospy.Time.now().to_sec() - start_time) < 16 and not rospy.is_shutdown():
                self.send_command("F 200")
                rate.sleep()

            # Now send "S" indefinitely (until next loop iteration)
            rospy.loginfo("Sending S indefinitely until next cycle or shutdown")
            while not rospy.is_shutdown():
                self.send_command("S")
                rate.sleep()

    def sequence_4(self):
        rospy.loginfo("Starting Sequence 4: F 50 for 1s, then S for 2s, loop")
        rate = rospy.Rate(1)
        while not rospy.is_shutdown():
            self.send_command("F 250")
            rate.sleep()
            #self.send_command("S")
            #time.sleep(1)

if __name__ == '__main__':
    try:
        sender = CommandSender()
        seq = rospy.get_param('~sequence', 3)

        if seq == 1:
            sender.sequence_1()
        elif seq == 2:
            sender.sequence_2()
        elif seq == 3:
            sender.sequence_3()
        elif seq == 4:
            sender.sequence_4()
        else:
            rospy.logerr("Invalid sequence number. Use 1, 2, 3, or 4.")
    except rospy.ROSInterruptException:
        pass

import time
import math
import rospy
from geometry_msgs.msg import Vector3Stamped
from adafruit_servokit import ServoKit

PAN_CHANNEL = 0
TILT_CHANNEL = 1
CENTER_PAN = 90
CENTER_TILT = 90
SAMPLING_RADIUS_TILT = 30  # Range will be from CENTER - R to CENTER + R
FREQUENCY = 0.5  # Bounce cycles per second

UPDATE_RATE = 0.002  # 500 Hz

def triangle_wave(t, freq):
    cycle = t * freq
    return abs(2 * (cycle - math.floor(cycle + 0.5)))

def main():
    rospy.init_node("sampling_antenna")
    kit = ServoKit(channels=16)
    angle_pub = rospy.Publisher('/servo_pos/antenna', Vector3Stamped, queue_size=10)

    rospy.loginfo("Sampling mode activated - Bouncing Line Pattern")

    rate = rospy.Rate(1.0 / UPDATE_RATE)
    start_time = time.time()

    try:
        while not rospy.is_shutdown():
            t = time.time() - start_time

            # Pan stays centered
            pan_angle = CENTER_PAN

            # Tilt moves in a triangle wave (bouncing line)
            tilt_offset = triangle_wave(t, FREQUENCY) * 2 * SAMPLING_RADIUS_TILT - SAMPLING_RADIUS_TILT
            tilt_angle = CENTER_TILT + tilt_offset

            # Clamp to valid servo angles (0-180)
            tilt_angle = max(0, min(180, tilt_angle))

            # Move servos
            kit.servo[PAN_CHANNEL].angle = pan_angle
            kit.servo[TILT_CHANNEL].angle = tilt_angle

            # Publish angle
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

    # Ensure servos are turned off on exit
    kit.servo[PAN_CHANNEL].angle = None
    kit.servo[TILT_CHANNEL].angle = None

if __name__ == "__main__":
    main()

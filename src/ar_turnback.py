#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Header, ColorRGBA
from geometry_msgs.msg import PoseArray, Pose
from visualization_msgs.msg import Marker, MarkerArray
from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion
from xycar_msgs.msg import xycar_motor
from std_msgs.msg import Int32MultiArray


motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size =1 )
xycar_msg = xycar_motor()


def drive(Angle, Speed):
    global motor_pub, xycar_msg
    xycar_msg.angle = Angle
    xycar_msg.speed = Speed
    motor_pub.publish(xycar_msg)
    

def main():
    t_end = time.time()
    
    for i in range(5):
        t_end = time.time() + 1.8
        while time.time() < t_end:
            drive(-40, -40)
        t_end = time.time() + 0.3
        while time.time() < t_end:
            drive(0, 20)
        time.sleep(2)


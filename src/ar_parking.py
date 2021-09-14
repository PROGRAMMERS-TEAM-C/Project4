#! /usr/bin/env python

import rospy, math, time
import cv2, time, rospy
import numpy as np

from ar_track_alvar_msgs.msg import AlvarMarkers
from tf.transformations import euler_from_quaternion
from std_msgs.msg import Int32MultiArray
from xycar_msgs.msg import xycar_motor

arData = {"DX":0.0, "DY":0.0, "DZ":0.0, "AX":0.0, "AY":0.0, "AZ":0.0, "AW":0.0}

roll, pitch, yaw = 0, 0, 0
angle = 0
speed = 0
end = False

def callback(msg):
    global arData, end
    if end:
        return 1

    for i in msg.markers:
        arData["DX"] = i.pose.pose.position.x
        arData["DY"] = i.pose.pose.position.y
        arData["DZ"] = i.pose.pose.position.z

        arData["AX"] = i.pose.pose.orientation.x
        arData["AY"] = i.pose.pose.orientation.y
        arData["AZ"] = i.pose.pose.orientation.z
        arData["AW"] = i.pose.pose.orientation.w
    control()
    

motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size =1 )

xycar_msg = xycar_motor()


def control():
    global arData, angle, speed, end
    (roll,yaw, pitch)=euler_from_quaternion((arData["AX"],arData["AY"],arData["AZ"], arData["AW"]))
	
    roll = math.degrees(roll)
    pitch = math.degrees(pitch)
    yaw = math.degrees(yaw)
  
    distance = math.sqrt(pow(arData["DX"],2) + pow(arData["DZ"],2))

    dx_dy_yaw = "DX:"+str(int(arData["DX"]))+" DY:"+str(int(arData["DY"]))+" Yaw:"+ str(round(yaw,1))
    angle = 10
    speed = 20

            
    if arData["DZ"] == 0:
        angle = 0
    else:
        angle = math.degrees(np.arctan(arData["DX"] / arData["DZ"])) * 2.0
            
    if distance < 0.45:
        angle = 0
        speed = 0




    xycar_msg.angle = angle
    xycar_msg.speed = speed
    motor_pub.publish(xycar_msg)




#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import rospy, math
import time
import numpy as np
from sensor_msgs.msg import LaserScan
from xycar_msgs.msg import xycar_motor
from std_msgs.msg import Int32MultiArray
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker, MarkerArray

time_start = time.time()
time_stop = time.time()
motor_pub = rospy.Publisher("xycar_motor", xycar_motor, queue_size=1)
xycar_msg = xycar_motor()

global end
end = False

def drive(Angle, Speed):
    global motor_pub, xycar_msg
    xycar_msg.angle = Angle
    xycar_msg.speed = Speed
    motor_pub.publish(xycar_msg)

def callback(data):
    global end

    lidar_data = data.ranges
    #print(lidar_data)

    if end:
        return 1

    # [int(0 * increment)]
    lidar_list = lidar_data[-25:]+lidar_data[:25]
    lidar_list = list(lidar_list)
    lidar_list[:] = [value for value in lidar_list if value != 0]

    print('lidar_list_means: ', np.mean(lidar_list))
    if np.mean(lidar_list) < 0.7:
        t_end = time.time() + 3.7
        while time.time() <= t_end:
            drive(-50, 25)
        
        end = True
    else:
        drive(1, 25)
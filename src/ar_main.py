#!/usr/bin/env python

import rospy, time
from std_msgs.msg import Header, ColorRGBA
from geometry_msgs.msg import PoseArray, Pose
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker, MarkerArray
from sensor_msgs.msg import LaserScan
from darknet_ros_msgs.msg import BoundingBoxes
from xycar_msgs.msg import xycar_motor
import lidar_driving
import ar_approach
import ar_turnback
import dqn_drive_end
import yolo_drive
import ar_parking
import math

yolodata = None
yoloobject = None
boxdata = None

rospy.init_node('ar_main')
laserdata = None
mode = -1
runLidar = True
runReverse = True
runApproach1 = True
runTurnback = True
runStartDQN = True
runEndDQN = True
runYolo = True
runApproach2 = True
runPark = True
yoloSpare1 = False
yoloSpare2 = False
arData = {"DX":0.0, "DY":0.0, "DZ":0.0, "AX":0.0, "AY":0.0, "AZ":0.0, "AW":0.0}

#msg2= yolo_msg()
time.sleep(15)

def lasercallback(data):
    global laserdata
    laserdata = data
    
def boxcallback(data):
    global boxdata
    global yoloobject
    boxdata = data

def callback(data):
    global mode, runLidar, runApproach1, runTurnback, runApproach2, runStartDQN, runEndDQN, runYolo, runPark, laserdata
    global yoloSpare1, yoloSpare2
    global yoloobject, boxdata
    print('mode: ', mode)
    
    for i in data.markers:
        arData["DX"] = i.pose.pose.position.x
        arData["DY"] = i.pose.pose.position.y
        arData["DZ"] = i.pose.pose.position.z

        arData["AX"] = i.pose.pose.orientation.x
        arData["AY"] = i.pose.pose.orientation.y
        arData["AZ"] = i.pose.pose.orientation.z
        arData["AW"] = i.pose.pose.orientation.w
        
        distance = math.sqrt(pow(arData["DX"],2) + pow(arData["DZ"],2))
        if i.id == 96:
            break

        if i.id == 5:
            yoloobject = 'bicycle'
        if i.id == 6:
            yoloobject = 'pottedplant'
        if mode == 0:
            break
        if mode == 3 and i.id == 0:
            break
        if mode == 4 and i.id == 1:
            if runEndDQN:
                break
        if mode == 4 and i.id == 5:
            if runEndDQN:
                yoloSpare1 = True
                break
        if mode == 4 and i.id == 6:
            if runEndDQN:
                yoloSpare2 = True
                break
        if i.id == 9:
            if distance <= 1.52:
                mode = 9
            break
        if mode == 9 and not runApproach2 and i.id == 0:
            mode = 0
        if (mode > 0 and mode < 5 and abs(i.id - mode) < 2) or (i.id > 3 and i.id != 4) or mode == -1:
            mode = i.id

    if mode == 1 and runLidar:
        if lidar_driving.callback(laserdata):
            runLidar = False
        
    elif mode == 2:
        if runApproach1:
            if ar_approach.callback(data, 0.4):
                runApproach1 = False
        elif runTurnback:
            runTurnback = False
            ar_turnback.main()

    elif mode == 4 and runEndDQN:
        if dqn_drive_end.callback(laserdata):
            runEndDQN = False

                
    elif (mode == 5 or mode == 6) and runYolo:
        yoloObject_flag = False
        #print('callback', yoloobject, boxdata)
        
        if boxdata is not None:
            for i in boxdata.bounding_boxes:
                if i.Class == yoloobject:
                    yoloObject_flag = True
                    
        if yoloObject_flag and boxdata:
            print('No backAndForth()')
            for i in boxdata.bounding_boxes:
                if i.Class == yoloobject:
                    print("yoloobject: ", yoloobject)
                    print("saw answer")
                    yolo_drive.callback(i)
        else:
            print('backAndForth()')
            backAndForth(yoloobject)
            #rospy.sleep(5)
            
    elif mode == 9 and runApproach2:
        print("start mode nine")
        for i in data.markers:
            if i.id == 9:
                if ar_approach.callback(data, 0.45, yoloobject):
                    runApproach2 = False

    elif mode == 0:
        ar_parking.callback(data)

def backAndForth(yoloobject):
    pub = rospy.Publisher("xycar_motor", xycar_motor, queue_size=1)
    xycar_msg = xycar_motor()

    for i in range(1000):
        speed = -35
        if yoloobject == 'bicycle':
            angle = 10
        else:
            angle = -10
        xycar_msg.angle = angle
        xycar_msg.speed = speed
        pub.publish(xycar_msg)

    for i in range(800):
        speed = 30
        angle = 0
        xycar_msg.angle = angle
        xycar_msg.speed = speed
        pub.publish(xycar_msg)


#obj2_msg = rospy.Publisher('yolo_object', yolo_msg, queue_size = 1)
rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)
rospy.Subscriber('/scan', LaserScan, lasercallback, queue_size=1)
rospy.Subscriber('/darknet_ros/bounding_boxes', BoundingBoxes, boxcallback)
rate = rospy.Rate(20)

rospy.spin()
     

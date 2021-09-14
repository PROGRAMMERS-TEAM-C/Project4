#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import rospy, math
import time
from sensor_msgs.msg import LaserScan
from xycar_msgs.msg import xycar_motor
from std_msgs.msg import Int32MultiArray
from ar_track_alvar_msgs.msg import AlvarMarkers
from visualization_msgs.msg import Marker, MarkerArray
    
motor_pub = rospy.Publisher('xycar_motor', xycar_motor, queue_size=1)
xycar_msg = xycar_motor()
turnIndex = 0
time_start = time.time()

def shut():
    exit()


def main():
    time.sleep(3)
    #rospy.init_node('lidar_drive')

    
    # mode 1 상태에서 lidar_driving 하다가 2번 AR TAG를 보면 ar_turnback을 해야한다.
    # 그래서 2번 AR TAG를 보면 return 0를 통해 ar_main으로 다시 이동하고 mode 2로 바꾸어 ar_turnback 호출
    def ar_callback(data):
        for i in data.markers:
            ar_id = i.id
            print(ar_id)
            if ar_id == 2:
                exit()

    def drive(Angle, Speed):
        global motor_pub, xycar_msg
        xycar_msg.angle = Angle
        xycar_msg.speed = Speed
        motor_pub.publish(xycar_msg)


    def callback(data):
        global turnIndex
        global time_start
        
        if turnIndex == 0:
            for i in range(20000):
                drive(30, 60)
            turnIndex += 1
            
            
        speed = 40
        lidar_data = data.ranges
        increment = 0.714285708755853066

        r_list = lidar_data[-125:-75] #[int(270 * increment)]
        r_list = list(r_list)
        r_list[:] = [value for value in r_list if value != 0]
        
        fr_list = lidar_data[-75:-25] #[int(315 * increment)]
        fr_list = list(fr_list)
        fr_list[:] = [value for value in fr_list if value != 0]
        
        fm_list = lidar_data[-25:]+lidar_data[:25] #[int(0 * increment)]
        fm_list = list(fm_list)
        fm_list[:] = [value for value in fm_list if value != 0]
        
        fl_list = lidar_data[25:75] #[int(45 * increment)]
        fl_list = list(fl_list)
        fl_list[:] = [value for value in fl_list if value != 0]
        
        l_list = lidar_data[75:125] #[int(90 * increment)]
        l_list = list(l_list)
        l_list[:] = [value for value in l_list if value != 0]
                
        r = min(r_list) if len(r_list) != 0 else 0
        fr = min(fr_list) if len(fr_list) != 0 else 0
        fm = min(fm_list) if len(fm_list) != 0 else 0
        fl = min(fl_list) if len(fl_list) != 0 else 0
        l = min(l_list) if len(l_list) != 0 else 0

        print("r: "+ str(r) + " fr: " + str(fr) + " fm: " + str(fm) + " fl: " + str(fl) + " l: " + str(l))
       
        '''
        if fl < 1.125 and fr > 0.5625:
            drive(50, 30)
        elif fl > 0.5625:
            drive(-50, 30)
        else:
            drive(0, 30)
        '''
        
        """
        if fl < 0.2 and fl < fr:
            drive(-50, speed)
        elif fr < 0.2:
            drive(50, speed)
        else:
            drive(0, speed)
        """
        
        if fm < 0.3 and fm != 0:
            if r > l:
                for i in range(9000):
                    drive(-50, -60)
            else:
                for i in range(9000):
                    drive(50, -60)
                    
        if l + r > 2.8 and (time.time()-time_start > 2.0):
            print("manual turn")
            
            if turnIndex == 1:
                for i in range(13000):
                    drive(-40, 60)
                turnIndex += 1
            elif turnIndex == 2:
                for i in range(13000):
                    drive(50, 60)
                turnIndex += 1
            elif turnIndex == 3:
                for i in range(10000):
                    drive(-40, 60)
            time_start = time.time()
                

        

        #angle = (fr - fl) * 100 + (r - l) * 100
        if fr+r > fl+l:
            drive(30, speed)
        else:
            drive(-30, speed)



                    
        """

        if l < 0.9 and fr > 1.5:
            print("to the left")
            drive(-50, 40)
        elif r < 0.9 and fl > 1.5:
            print("to the right")
            drive(50, 40)
                    
        if (fr > 0.9 and fr > fl):
            drive(50, 30)
        elif fl > 0.9:
            drive(-50, 30)
        else:
            drive(0, 30)
        
        """

        """
        
        if l + fl + fm + fr + r == 0:       # 모든 값이 0인 경우, 라이다 값이 들어올 때까지 정지
            drive(0, 0)
#        elif abs(r + fr - fl - l) < 0.2:
#            drive(0, speed)
        else:
            angle = (fr - fl) * 80 + (r - l) * 100
            
            if r > 1.5:
                angle = 50
            elif l > 1.5:
                angle = -50
                
            print(angle)
            drive(angle, speed)
            
         """

    rospy.Subscriber('/scan', LaserScan, callback, queue_size=1)
    rospy.Subscriber('ar_pose_marker', AlvarMarkers, ar_callback)      

    
    rospy.spin()




from xycar_msgs.msg import xycar_motor
import rospy

pub = rospy.Publisher("xycar_motor", xycar_motor, queue_size=1)

def callback(box):
    center = (box.xmax + box.xmin)/2
    print('angle: ',int(50.0*((center - 320.0)/320.0)))
    drive((int(50.0*((center - 320.0)/320.0))), 17)


def drive(angle, speed):
    msg = xycar_motor()
                    
    msg.angle = angle
    msg.speed = speed
    pub.publish(msg)
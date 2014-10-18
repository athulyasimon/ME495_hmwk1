#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist, Vector3
from math import*
from std_msgs.msg import String, Int32
from turtlesim.srv import TeleportAbsolute
import rosbag

T= raw_input("How fast you want to turtle to complete a figure 8? Or hit enter for default period of 8 seconds:") or 8


def calculations(current_time):
    #x=3*math.sin(4*pie*current_time/T)
    #y=3*math.sin(2*pie*current_time/T)
    t = current_time

    vx=12*pi*cos(4*pi*t/T)/T
    vy=6*pi*cos(2*pi*t/T)/T

    ax = -48*pi*pi*sin(4*pi*t/T)/(T*T)
    ay = -12*pi*pi*sin(2*pi*t/T)/(T*T)

    v_turtle = sqrt(vx**2+vy**2)
    theta_dot = ((ay*vx-ax*vy)/(vx*vx+vy*vy))

    return [v_turtle, theta_dot]

def send_cmd_vel():

    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
    rospy.init_node('send_cmd_vel', anonymous=True)

    r=rospy.Rate(60) 

    start = rospy.get_time()
    
    while not rospy.is_shutdown():
    	current_time = rospy.get_time()
        current_time = current_time - start

    	v_turtle = calculations(current_time)[0]
        theta_dot = calculations(current_time)[1]
		
     	velocities_cmd_vel = Twist(Vector3(v_turtle,0,0),Vector3(0,0,(theta_dot)))
    	
    	rospy.loginfo(velocities_cmd_vel)
    	pub.publish(velocities_cmd_vel)
    	r.sleep()

if __name__ == '__main__':
    try:
        rospy.wait_for_service('turtle1/teleport_absolute')
        turtle_pos = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
        turtle_pos(5.54444,5.544444,0.5)
        send_cmd_vel()
    except rospy.ROSInterruptException: pass



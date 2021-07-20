#!/usr/bin/env python

import rospy
import paho.mqtt.client as mqtt
from std_msgs.msg import Float32

pitch_pub = rospy.Publisher('/pitch', Float32, queue_size = 10)
roll_pub = rospy.Publisher('/roll', Float32, queue_size = 10)

def talker():
    broker_address = "broker.mqttdashboard.com"
    pitch_client = mqtt.Client("pitch")
    pitch_client.on_message = pitch_on_message
    pitch_client.connect(broker_address)
    roll_client = mqtt.Client("roll")
    roll_client.on_message = roll_on_message
    roll_client.connect(broker_address)

    rospy.init_node('mqtt2ROS', anonymous=True)

    rate = rospy.Rate(60)

    pitch_client.loop_start()
    roll_client.loop_start()
    pitch_client.subscribe("DAGOHOOGESCHOOL/pitch")
    roll_client.subscribe("DAGOHOOGESCHOOL/roll")

    while not rospy.is_shutdown():
        rate.sleep()

    roll_client.loop_stop()
    pitch_client.loop_stop()

def pitch_on_message(client, userdata, message):
    temp_pitch = float(message.payload.decode("utf-8"))
    pitch_pub.publish(temp_pitch)

def roll_on_message(client, userdata, message):
    temp_roll = float(message.payload.decode("utf-8"))
    roll_pub.publish(temp_roll)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

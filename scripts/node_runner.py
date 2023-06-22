#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import subprocess

def callback(data):
    rospy.loginfo("Received message: %s", data.data)
    command = data.data

    # Split the command string by whitespace
    split_command = command.split()

    # Extract the two values
    pkg_name = split_command[1]
    node_name = split_command[2]

    print("Package Name:", pkg_name)
    print("Node Name:", node_name)
    run_command(pkg_name, node_name)

def run_command(pkg_name, node_name):
    ros_command = f"rosrun {pkg_name} {node_name}"
    try:
        subprocess.Popen(ros_command, shell=True)
        print("Command executed successfully")
    except rospy.ROSInterruptException as ee:
        print(ee)

def listener():
    rospy.init_node('command')
    rospy.loginfo("Node started")

    rospy.Subscriber("/node_command", String, callback)

    rospy.spin()

if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

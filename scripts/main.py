#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import tkinter as tk
from PIL import ImageTk, Image
import cv2
global flag
flag = 0
cv_image = None  # Define the cv_image variable
label = None  # Define the label variable
container_width = 480
container_height = 240
status = 0



def send_data():
    node_name = entry_node_name.get()
    node_type = entry_type.get()
    pkg_name = entry_pkg_name.get()

    ros_command = f"rosrun {pkg_name} {node_type}"
    rospy.loginfo(ros_command)
    print(ros_command)
    pub.publish(ros_command)

def kill_node():
    node_name = entry_kill_node.get()
    ros_command = f"rosnode kill {node_name}"
    rospy.loginfo(ros_command)
    print(ros_command)
   

    
    

def clear_input_fields():
    entry_node_name.delete(0, tk.END)
    entry_type.delete(0, tk.END)
    entry_pkg_name.delete(0, tk.END)
    entry_kill_node.delete(0, tk.END)
    rospy.loginfo("Clearing")

def update_video_frame():
    global cv_image, label, flag  # Make cv_image and label accessible
    
    if cv_image is not None and label is not None:
        # Convert the OpenCV image to PIL format
        image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Resize the image to fit the container
        image = image.resize((container_width, container_height), Image.ANTIALIAS)

        # Create a PhotoImage object from the resized image
        photo = ImageTk.PhotoImage(image)

        # Update the image in the label
        label.config(image=photo)
        label.image = photo
        
    else:
        
        if flag == 0:
        
            # Create a canvas inside the label
            canvas = tk.Canvas(label, width=container_width, height=container_height, bg="gray")
            canvas.pack()

            # Add text in the center of the canvas
            text = "Enter the Image Topic"
            text_x = container_width // 2  # x-coordinate of the center
            text_y = container_height // 2  # y-coordinate of the center
            canvas.create_text(text_x, text_y, text=text, fill="black", font=("Arial", 14), justify="center")
            
            flag = 1

    
    # Repeat the process after a certain delay (in milliseconds)
    label.after(100, update_video_frame)

def image_callback(msg):
    global cv_image  # Make cv_image accessible
    bridge = CvBridge()
    try:
        # Convert the compressed image data to OpenCV format
        cv_image = bridge.compressed_imgmsg_to_cv2(msg, desired_encoding="passthrough")
    except Exception as e:
        rospy.logerr(e)
        return

def main():
    
    rospy.init_node("tkinter_ros_node")

    window = tk.Tk()
    window.title("ROS Node GUI")

    input_frame = tk.Frame(window)
    input_frame.pack( anchor="nw", padx=10, pady=10)
    


    label_node_name = tk.Label(input_frame, text="Node name:")
    label_node_name.grid(row=0, column=0, sticky="e")
    global entry_node_name
    entry_node_name = tk.Entry(input_frame)
    entry_node_name.grid(row=0, column=1, padx=10, pady=5)

    label_type = tk.Label(input_frame, text="Type:")
    label_type.grid(row=1, column=0, sticky="e")
    global entry_type 
    entry_type = tk.Entry(input_frame)
    entry_type.grid(row=1, column=1, padx=10, pady=5)

    label_pkg_name = tk.Label(input_frame, text="pkg_name:")
    label_pkg_name.grid(row=2, column=0, sticky="e")
    global entry_pkg_name
    entry_pkg_name = tk.Entry(input_frame)
    entry_pkg_name.grid(row=2, column=1, padx=10, pady=5)

    label_kill_node = tk.Label(input_frame, text="Node to kill:")
    label_kill_node.grid(row=2, column=2, sticky="e")
    global entry_kill_node
    entry_kill_node = tk.Entry(input_frame)
    entry_kill_node.grid(row=2, column=3, padx=10, pady=5)

    send_button = tk.Button(input_frame, text="Run a node from here", command=send_data)
    send_button.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    clear_button = tk.Button(input_frame, text="Clear", command=clear_input_fields)
    clear_button.grid(row=3, column=2, padx=10, pady=5, sticky="w")

    kill_button = tk.Button(input_frame, text="Kill Node", command=kill_node)
    kill_button.grid(row=3, column=3, padx=10, pady=5, sticky="w")

   
    
    
    
    container_width = 480
    container_height = 240

    global label  # Make label accessible
    label = tk.Label(window, width=container_width, height=container_height)
    label.place(x= 20, y = 220)

    global pub,topicname
    pub = rospy.Publisher("/node_command", String, queue_size=10)
    rospy.Subscriber("/image_raw/compressed", CompressedImage, image_callback)
    
    
    
        
    # rospy.Subscriber("/image_compressed", CompressedImage, image_callback)

    update_video_frame()
    
    window.mainloop()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

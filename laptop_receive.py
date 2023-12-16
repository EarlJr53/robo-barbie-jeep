"""
Script that receives image streamed from RPi on laptop. Run this before 
running the sending script on the RPI.
"""

import cv2
import imagezmq

image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    rpi_name, image = image_hub.recv_image()
    cv2.imshow(rpi_name, image)
    cv2.waitKey(1)
    image_hub.send_reply(b"OK")

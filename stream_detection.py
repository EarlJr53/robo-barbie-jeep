import numpy as np
import cv2 as cv
import socket
import time
from matplotlib import pyplot as plt
from imutils.video import VideoStream
import imagezmq
from picamera2 import Picamera2

picam2 = Picamera2()

sender = imagezmq.ImageSender(connect_to='tcp://192.168.16.96:5555')
rpi_name = socket.gethostname()  # send RPi hostname with each image

picam2.start()
time.sleep(2.0)

while True:
    img = picam2.capture_array()
    # img = cv.imread('sidewalk_olin_1.jpeg')
    hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    h_channel= hsv_img[:, :, 0]  # Hue channel
    s_channel = hsv_img[:, :, 1]  # Saturation channel
    v_channel = hsv_img[:, :, 2]  # Value channel
    # print(h_channel, s_channel, v_channel)
    lower_color = np.array([200, 200, 200])
    upper_color = np.array([255,255, 255])

    color_mask = cv.inRange(img, lower_color, upper_color)

    assert img is not None, "file could not be read, check with os.path.exists()"

    edges = cv.Canny(color_mask,200,300)

    plt.subplot(121),plt.imshow(color_mask)
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()

    # # Find contours in the edges
    # contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    # # Find the contour with the largest area
    # largest_contour = max(contours, key=cv.contourArea)

    # # Draw the largest contour on a blank image (optional)
    # largest_contour_image = np.zeros_like(img)
    # cv.drawContours(largest_contour_image, [largest_contour], -1, (255), thickness=cv.FILLED)

    # # Display the results
    # cv.imshow('Original Image', img)
    # cv.imshow('Canny Edges', edges)
    # cv.imshow('Largest Contour', largest_contour_image)
    # cv.waitKey(0)
    # cv.destroyAllWindows()

    sender.send_image(rpi_name, edges)

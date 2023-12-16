---
title: "System Architecture"
meta_title: "System Architecture Overview"
description: "Walkthrough of software and system architecture/algorithms for sidewalk detection project."
image: "/images/project-image.png" #! Put something useful here
draft: false
---

<!-- System architecture: In detail describe each component of your project. Make sure to touch upon both code structure as well as algorithms. -->

## Streaming vs. Pre-recorded Footage

Although the core sidewalk detection aspects of our project are consistent, we have multiple types of wrappers for this code that work for different inputs. For live video on the Raspberry Pi, we use Picamera2 to capture the camera module's feed. This is then passed into OpenCV for processing and sidewalk detection. Finally, the OpenCV feed is passed to ImageZMQ, which streams the feed over the network to a laptop. One downside of this system is that we couldn't get the Raspberry Pi to create a hotspot network, so we were tied to the OLIN-ROBOTICS network. This meant that doing extensive real-world testing on live video was very difficult.

Similar to the live feed processing, we use a similar structure to process pre-recorded video. Based on our initial program that processes a single image, we load in the video and then loop through all of its frames, running the sidewalk detection algorithm on each one and saving the result to a new OpenCV video buffer. At the end, we break out of the loop and save the video to disk. This solution worked very well for tuning the detection algorithm without continually having to walk around campus with the Raspberry Pi and camera module.

## Detection

The software begins by reading frames from a video file, representing a sequence of images captured from a camera. Each frame is converted from the standard RGB color space to HSV (Hue, Saturation, Value) color space, which is more effective for color-based segmentation in image processing. We then define a specific region in the image, known as the Region of Interest (ROI), where we expect to find the sidewalk. This ROI is a smaller section of the image, focusing on the area in front of the camera where the sidewalk is most likely to appear. Within this ROI, we analyze the color distribution to calibrate our HSV settings, ensuring that we can accurately distinguish the sidewalk from other parts of the image.

To achieve this, we use histograms to find the most dominant hues, saturations, and values (brightness levels) in the ROI. These dominant values serve as a basis to create a mask that highlights the sidewalk. The software then searches for contours, which are continuous lines or curves that bound the sidewalk area. We apply filters to select the largest contour, assuming it represents the sidewalk. We split the image up into vertical strips. Within each section, we calculate the average x-coordinate of the points that make up the sidewalk's contour. This average point is considered the center of the sidewalk in that particular section. By calculating these center points for each section, we can map out the general path the sidewalk takes. To make the detected sidewalk path smoother and more consistent, we use Savitzky-Golay filtering, which helps in reducing noise and irregularities in the contour. Finally, the software calculates the central path of the detected sidewalk and draws it on the image. This path is crucial for navigation, as it shows the direction in which to steer to stay on the sidewalk. Additionally, the software provides directional guidance by comparing the position of the sidewalk's center with the image's center, advising whether to adjust left or right to stay aligned with the path. This whole process repeats for each frame of the video, allowing for real-time sidewalk detection and navigation guidance.


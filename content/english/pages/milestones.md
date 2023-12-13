---
title: "CompRobo Final Project: Project Milestones"
meta_title: "Project Milestones"
description: "Descriptions of project progress at defined milestones."
image: "/images/project-image.png" # add something useful here
draft: false
---

<!-- Twice during the project you will be writing up your progress on your project thus far. You should include these milestones as part of your project website, so try to keep the writing suitable for a general audience (e.g., someone who doesn’t have much context about the class). You will be coming up with your best guess as to how far you will be by each of the project milestones as part of your project proposal. -->

## Milestone 1

The milestone we set for this week was getting the Raspberry Pi setup with ROS, deciding on the algorithm to use, and starting to write pseudo-code/decide on packages to use. So far, we have installed an OS on the RPi, figured out how to install ROS, and did some work deciding on a pipeline and algorithm. We are hoping to use OpenCV contours to detect sidewalks, and are thinking about how to stream the OpenCV output to our computer so we can see how accurate the detection is.

## Milestone 2

At this point in the project, we have implemented image streaming between the Raspberry Pi and laptop. We are able to pipe the Picamera2 output into OpenCV and then use ImageZMQ to send the video feed over the network to the laptop. We have also been exploring 2 different (but related) methods of contour detection as our method for sidewalk detection. A barebones version of the sidewalk detection has been integrated with video streaming as well. Next, we will be improving the sidewalk detection algorithm to the point where the streamed video will have an overlay of the boundaries of the sidewalk.

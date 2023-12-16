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
<!-- Reuben words here -->
```python

```

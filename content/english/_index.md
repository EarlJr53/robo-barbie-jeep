---
# Banner
banner:
  title: "Sidewalk Detection (\"Robo Barbie Jeep\")"
  content: "Reuben Lewis, Brooke Moss, Swasti Jain"
  image: "/images/demo.png"
  button:
    enable: true
    label: "Project Architecture"
    link: "architecture/"

# You should create a project website. The project website will serve two purposes: to explain how your system works and to document the story of how you arrived at your final product. You should create these deliverables for multiple audiences: general readers interested in your project, potential employers, other students in the course, and the CompRobo teaching staff (course assistants and faculty).

# Show it off: Describe the main idea of your project. What does your system do? Why would you want to do this? What are the major components to your system and how do they fit together? Hopefully you will have some cool videos to put in the website by this point.

# Features (simplified to a single section for the project introduction)
features:
  - title: "Our Method"
    image: "images/robo_hand.png"
    content: "Sidewalk Detection Algorithm"
    bulletpoints:
    - "Sidewalk Detection Using Color: The code aims to detect sidewalks in images by analyzing colors using the HSV (Hue, Saturation, Value) color space."
    - "Dynamic Calibration with Trackbars: It uses interactive sliders to dynamically calibrate the range of HSV values that best represent the sidewalk in the image."
    - "Region of Interest (ROI) Focused Analysis: The code focuses on a specific area (Region of Interest) in the lower part of the image, where the sidewalk is most likely to be found."
    - "Ideal for a range of audio recognition applications"
    - "HSV Range Calculation: It calculates the median HSV values in the ROI and uses these to set initial slider positions, providing a starting point for the detection."
    - "Contour Detection and Visualization: The code identifies the contours of the detected sidewalk area and draws them on the original image, allowing for visual verification of the detection accuracy."
    - "Smooth Path Estimation: It uses the Savitzky-Golay filter to smooth the detected path of the sidewalk, providing a more continuous and accurate representation of its trajectory."
    - "Turn Suggestion: Using the determined sidewalk trajectory, it decides whether the “vehicle” should turn left or right to remain on the sidewalk."
    button:
    button:
      enable: false
---

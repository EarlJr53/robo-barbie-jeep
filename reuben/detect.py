import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
image_path = 'sidewalk.jpeg'
image = cv2.imread(image_path)

# Make sure the image path is correct and the image is loaded properly
if image is None:
    raise ValueError("Could not load the image, check the file path.")

# Convert the image to the HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define the range of grey color in HSV
lower_grey = np.array([0, 0, 50])
upper_grey = np.array([180, 50, 220])

# Create a mask for grey color
mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)

# Now you can find contours in the mask
contours, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Now, we will highlight the detected sidewalk in yellow on the original image.
# Yellow in BGR code is (0, 255, 255).

# Create a copy of the original image to draw the highlights
highlighted_image = image.copy()

# Now you can find contours in the mask
contours, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours based on contour area and get the largest contour
# The largest contour should correspond to the largest continuous grey area (the sidewalk)
largest_contour = max(contours, key=cv2.contourArea)

# Create a copy of the original image to draw the highlights
highlighted_image = image.copy()

# Draw the largest contour with yellow color on the original image
cv2.drawContours(highlighted_image, [largest_contour], -1, (0, 255, 255), thickness=cv2.FILLED)

# Blend the highlighted image with the original image
alpha = 0.4  # Transparency factor.
result_highlighted = cv2.addWeighted(highlighted_image, alpha, image, 1 - alpha, 0)

# Save the result
output_path_highlighted = 'sidewalk_highlighted_yellow.png'
cv2.imwrite(output_path_highlighted, result_highlighted)

# Display the result
plt.imshow(cv2.cvtColor(result_highlighted, cv2.COLOR_BGR2RGB))
plt.axis('off')
plt.show()

# Return the path to the saved result
output_path_highlighted

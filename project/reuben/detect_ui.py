import cv2
import numpy as np

# Callback function for the trackbar
def update_image(*args):
    # HSV color mask parameters
    lower_grey = np.array([0, 0, 50])
    upper_grey = np.array([180, 50, 220])

    # Create a mask for grey color
    mask_grey = cv2.inRange(hsv, lower_grey, upper_grey)
    contours, _ = cv2.findContours(mask_grey, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Retrieve the current positions of the trackbars
    min_area = cv2.getTrackbarPos('Min Area', 'Sidewalk Detection')
    max_area = cv2.getTrackbarPos('Max Area', 'Sidewalk Detection')

    # Find the largest contour
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)

        if min_area < area < max_area:
            # Create a copy of the original image to draw the largest contour
            image_copy = original_image.copy()
            cv2.drawContours(image_copy, [largest_contour], -1, (0, 255, 255), 2)
        else:
            # If not within range, display the original image
            image_copy = original_image.copy()
    else:
        # If no contours found, display the original image
        image_copy = original_image.copy()

    # Display the updated image
    cv2.imshow('Sidewalk Detection', image_copy)

# Load the image
image_path = 'sidewalk.jpeg'
original_image = cv2.imread(image_path)
hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

# Create a window
cv2.namedWindow('Sidewalk Detection', cv2.WINDOW_NORMAL)

# Create the trackbars
cv2.createTrackbar('Min Area', 'Sidewalk Detection', 0, 10000, update_image)
cv2.createTrackbar('Max Area', 'Sidewalk Detection', 10000, 100000, update_image)

# Initialize the image
update_image()

# Wait for the user to press 'q' to exit
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()

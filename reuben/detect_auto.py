import cv2
import numpy as np
from scipy.signal import savgol_filter

def update_image(*args):
    # Retrieve the current positions of the trackbars
    h_range = cv2.getTrackbarPos('H Range', 'Sidewalk Detection')
    s_range = cv2.getTrackbarPos('S Range', 'Sidewalk Detection')
    v_range = cv2.getTrackbarPos('V Range', 'Sidewalk Detection')

    # Calibrate using the current trackbar values
    lower_hsv, upper_hsv , _ = calibrate_sidewalk_hsv(hsv_roi, h_range, s_range, v_range)

    # Create a mask for the calibrated HSV range and find contours in the ROI
    mask_roi = cv2.inRange(hsv_roi, lower_hsv, upper_hsv)
    contours_roi, _ = cv2.findContours(mask_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Offset the contours by the ROI's starting y-coordinate
    offset_contours_roi = [contour + (0, roi_y_start) for contour in contours_roi]

    # Create a mask for the entire image
    mask_full = cv2.inRange(hsv, lower_hsv, upper_hsv)
    contours_full, _ = cv2.findContours(mask_full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the largest contour from the ROI on the original image
    image_copy = original_image.copy()
    if offset_contours_roi:
        largest_contour_roi = max(offset_contours_roi, key=cv2.contourArea)
        cv2.drawContours(image_copy, [largest_contour_roi], -1, (0, 255, 0), 2)  # Green for ROI contour

    # Draw the largest contour from the full image
    if contours_full:
        largest_contour_full = max(contours_full, key=cv2.contourArea)
        cv2.drawContours(image_copy, [largest_contour_full], -1, (0, 255, 255), 2)

        # Convert the contour to a set of points
        points = np.vstack(largest_contour_full).squeeze()

        # Initialize an empty list to store the center points
        center_points = []

        # Divide the image into sections along the vertical axis
        num_sections = 5
        section_height = image_copy.shape[0] // num_sections

        for i in range(num_sections):
            # Get the points in the current section
            section_points = points[(points[:, 1] >= i * section_height) & (points[:, 1] < (i + 1) * section_height)]
            
            # Skip if there are no points in this section
            if len(section_points) == 0:
                continue

            # Calculate the center point of the sidewalk in the current section
            center_x = np.mean(section_points[:, 0])
            center_y = i * section_height + section_height / 2

            # Add the center point to the list
            center_points.append((int(center_x), int(center_y)))

        # Convert the list of center points to a numpy array
        center_points = np.array(center_points, dtype=np.int32)

        # Apply the Savitzky-Golay filter to the x and y coordinates of the points
        # Adjust window_length and polynomial_order as needed
        window_length, polynomial_order = 5, 2
        x_smooth = savgol_filter(center_points[:, 0], window_length, polynomial_order)
        y_smooth = savgol_filter(center_points[:, 1], window_length, polynomial_order)

        # Combine the smoothed x and y coordinates into a single array
        center_points_smooth = np.column_stack((x_smooth, y_smooth))

        # Convert the smoothed center points to a numpy array
        center_points_smooth = np.array(center_points_smooth, dtype=np.int32)

        # Draw a polyline that connects the smoothed center points
        cv2.polylines(image_copy, [center_points_smooth], False, (255, 0, 0), 2)

        # Calculate the x-coordinate of the center of the image
        image_center_x = image_copy.shape[1] // 2

        # Calculate the x-coordinate of the center point of the sidewalk in the middle section
        sidewalk_center_x = center_points[len(center_points) // 2, 0]

        # Define a tolerance range around the center of the image
        tolerance = 100  # Adjust this value as needed

        # Compare the two x-coordinates to determine whether to adjust to the left or right
        if sidewalk_center_x < image_center_x - tolerance:
            direction = "Adjust to the left"
        elif sidewalk_center_x > image_center_x + tolerance:
            direction = "Adjust to the right"
        else:
            direction = "Stay on course"

        # Calculate the size of the text
        text_size, _ = cv2.getTextSize(direction, cv2.FONT_HERSHEY_SIMPLEX, 2, 2)

        # Draw a filled rectangle behind the text
        cv2.rectangle(image_copy, (10, image_copy.shape[0] - 20 - text_size[1]), (10 + text_size[0], image_copy.shape[0] - 20), (255, 255, 255), -1)

        # Display the direction in the image
        cv2.putText(image_copy, direction, (10, image_copy.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2)

        # Display the updated image
        cv2.imshow('Sidewalk Detection', image_copy)

    # Also display the ROI for reference
    #roi_image = cv2.cvtColor(mask_roi, cv2.COLOR_GRAY2BGR)  # Convert mask to BGR for display
    #cv2.imshow('ROI', roi_image)

def calibrate_sidewalk_hsv(hsv_cropped, h_range, s_range, v_range):
    # Calculate the histograms
    h_hist = cv2.calcHist([hsv_cropped], [0], None, [180], [0, 180])
    s_hist = cv2.calcHist([hsv_cropped], [1], None, [256], [0, 256])
    v_hist = cv2.calcHist([hsv_cropped], [2], None, [256], [0, 256])

    # Calculate the medians
    h_median = np.argmax(np.cumsum(h_hist) >= np.sum(h_hist)/2)
    s_median = np.argmax(np.cumsum(s_hist) >= np.sum(s_hist)/2)
    v_median = np.argmax(np.cumsum(v_hist) >= np.sum(v_hist)/2)

    # Calculate the lower and upper HSV values
    lower_hsv = np.array([max(h_median - h_range, 0), max(s_median - s_range, 0), max(v_median - v_range, 0)])
    upper_hsv = np.array([min(h_median + h_range, 180), min(s_median + s_range, 255), min(v_median + v_range, 255)])
    
    return lower_hsv, upper_hsv, (h_median, s_median, v_median)  # Return median HSV values

'''
def calibrate_sidewalk_hsv(hsv_cropped, h_range, s_range, v_range):
    # Calculate the histograms
    h_hist = cv2.calcHist([hsv_cropped], [0], None, [180], [0, 180])
    s_hist = cv2.calcHist([hsv_cropped], [1], None, [256], [0, 256])
    v_hist = cv2.calcHist([hsv_cropped], [2], None, [256], [0, 256])

    # Calculate the means
    h_mean = int(np.average(np.arange(180), weights=h_hist.flatten())) if np.sum(h_hist) > 0 else 0
    s_mean = int(np.average(np.arange(256), weights=s_hist.flatten())) if np.sum(s_hist) > 0 else 0
    v_mean = int(np.average(np.arange(256), weights=v_hist.flatten())) if np.sum(v_hist) > 0 else 0

    # Calculate the lower and upper HSV values
    lower_hsv = np.array([max(h_mean - h_range, 0), max(s_mean - s_range, 0), max(v_mean - v_range, 0)])
    upper_hsv = np.array([min(h_mean + h_range, 180), min(s_mean + s_range, 255), min(v_mean + v_range, 255)])
    
    return lower_hsv, upper_hsv, (h_mean, s_mean, v_mean)  # Return mean HSV values
'''

# Load the image and define ROI
image_path = 'data/sidewalk_olin_2.jpeg'
original_image = cv2.imread(image_path)
hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
roi_height = int(original_image.shape[0] * 0.3)  # Height of the ROI (e.g., 30% of the image height)
roi_y_start = original_image.shape[0] - roi_height  # Y-coordinate where the ROI starts
roi = (0, roi_y_start, original_image.shape[1], original_image.shape[0])  # (x_start, y_start, x_end, y_end)
hsv_roi = hsv[roi[1]:roi[3], roi[0]:roi[2]]

# Calculate initial HSV calibration values
default_range = 30  # Default range value for H, S, and V
_, _, (h_peak, s_peak, v_peak) = calibrate_sidewalk_hsv(hsv_roi, default_range, default_range, default_range)

# Create a window with trackbars
cv2.namedWindow('Sidewalk Detection', cv2.WINDOW_NORMAL)
cv2.createTrackbar('H Range', 'Sidewalk Detection', h_peak, 180, update_image)
cv2.createTrackbar('S Range', 'Sidewalk Detection', s_peak, 255, update_image)
cv2.createTrackbar('V Range', 'Sidewalk Detection', v_peak, 255, update_image)


# Initialize the image
update_image()

# Wait for the user to press 'q' to exit or the window to be closed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Sidewalk Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Cleanup
cv2.destroyAllWindows()
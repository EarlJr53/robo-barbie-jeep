import cv2
import numpy as np
from scipy.signal import savgol_filter

def calculate_initial_peaks(lab_cropped):
    # Calculate the mean of each channel in the LAB color space
    l_mean = int(np.mean(lab_cropped[:, :, 0]))
    a_mean = int(np.mean(lab_cropped[:, :, 1]))
    b_mean = int(np.mean(lab_cropped[:, :, 2]))
    return l_mean, a_mean, b_mean


def calculate_lab_ranges(lab_cropped, l_range, a_range, b_range):
    l_peak, a_peak, b_peak = calculate_initial_peaks(lab_cropped)
    lower_lab = np.array([max(l_peak - l_range, 0), max(a_peak - a_range, -127), max(b_peak - b_range, -127)])
    upper_lab = np.array([min(l_peak + l_range, 100), min(a_peak + a_range, 127), min(b_peak + b_range, 127)])
    return lower_lab, upper_lab

window_length = 5
polynomial_order = 2    

def update_image(*args):
    # Retrieve the current positions of the trackbars
    l_range = cv2.getTrackbarPos('L Range', 'Sidewalk Detection')
    a_range = cv2.getTrackbarPos('a Range', 'Sidewalk Detection')
    b_range = cv2.getTrackbarPos('b Range', 'Sidewalk Detection')

    # Calibrate using the current trackbar values
    lower_lab, upper_lab = calibrate_sidewalk_lab(lab_roi, l_range, a_range, b_range)

    # Create a mask for the calibrated LAB range and find contours in the ROI
    mask_roi = cv2.inRange(lab_roi, lower_lab, upper_lab)
    contours_roi, _ = cv2.findContours(mask_roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Offset the contours by the ROI's starting y-coordinate
    offset_contours_roi = [contour + (0, roi_y_start) for contour in contours_roi]

    # Create a mask for the entire image
    mask_full = cv2.inRange(lab, lower_lab, upper_lab)
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
        if len(center_points) >= window_length:
            x_smooth = savgol_filter(center_points[:, 0], window_length, polynomial_order)
            y_smooth = savgol_filter(center_points[:, 1], window_length, polynomial_order)

            # Combine the smoothed x and y coordinates into a single array
            center_points_smooth = np.column_stack((x_smooth, y_smooth))

            # Draw a polyline that connects the smoothed center points
            cv2.polylines(image_copy, [center_points_smooth], False, (255, 0, 0), 2)
        else:
            # Handle the case where there are not enough points
            # For example, you might just draw the unsmoothed points
            if len(center_points) > 1:
                cv2.polylines(image_copy, [center_points], False, (255, 0, 0), 2)

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

def calibrate_sidewalk_lab(lab_cropped, l_range, a_range, b_range):
    # Calculate the histograms
    l_hist = cv2.calcHist([lab_cropped], [0], None, [256], [0, 256]).flatten()
    a_hist = cv2.calcHist([lab_cropped], [1], None, [256], [-127, 127]).flatten()
    b_hist = cv2.calcHist([lab_cropped], [2], None, [256], [-127, 127]).flatten()

    # Calculate the mean of the histograms
    l_mean = int(np.average(np.arange(256), weights=l_hist))
    a_mean = int(np.average(np.arange(256) - 127, weights=a_hist))
    b_mean = int(np.average(np.arange(256) - 127, weights=b_hist))

    # Calculate the lower and upper LAB values
    lower_lab = np.array([max(l_mean - l_range, 0), max(a_mean - a_range, -127), max(b_mean - b_range, -127)])
    upper_lab = np.array([min(l_mean + l_range, 100), min(a_mean + a_range, 127), min(b_mean + b_range, 127)])
    
    return lower_lab, upper_lab

# Load the image and define ROI
image_path = 'data/sidewalk_olin_2.jpeg'
original_image = cv2.imread(image_path)
lab = cv2.cvtColor(original_image, cv2.COLOR_BGR2Lab)
roi_height = int(original_image.shape[0] * 0.3)  # Height of the ROI (e.g., 30% of the image height)
roi_y_start = original_image.shape[0] - roi_height  # Y-coordinate where the ROI starts
roi = (0, roi_y_start, original_image.shape[1], original_image.shape[0])  # (x_start, y_start, x_end, y_end)
lab_roi = lab[roi[1]:roi[3], roi[0]:roi[2]]

# Calculate the initial peak values
l_peak, a_peak, b_peak = calculate_initial_peaks(lab_roi)

# Create a window with trackbars
cv2.namedWindow('Sidewalk Detection', cv2.WINDOW_NORMAL)
cv2.createTrackbar('L Range', 'Sidewalk Detection', l_peak, 100, update_image)
cv2.createTrackbar('a Range', 'Sidewalk Detection', a_peak, 255, update_image)
cv2.createTrackbar('b Range', 'Sidewalk Detection', b_peak, 255, update_image)

# Initialize the image
update_image()

# Wait for the user to press 'q' to exit or the window to be closed
while True:
    if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty('Sidewalk Detection', cv2.WND_PROP_VISIBLE) < 1:
        break

# Cleanup
cv2.destroyAllWindows()
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression

def update_image(*args):
    # Retrieve the current positions of the trackbars
    h_range = cv2.getTrackbarPos('H Range', 'Sidewalk Detection')
    s_range = cv2.getTrackbarPos('S Range', 'Sidewalk Detection')
    v_range = cv2.getTrackbarPos('V Range', 'Sidewalk Detection')

    # Calibrate using the current trackbar values
    lower_hsv, upper_hsv = calibrate_sidewalk_hsv(hsv_roi, h_range, s_range, v_range)

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
        x = points[:, 0]
        y = points[:, 1]

        # Fit a polynomial regression model
        degree = 2  # Degree of the polynomial
        model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
        model.fit(x.reshape(-1, 1), y)

        # Generate points along the polynomial curve
        x_fit = np.linspace(x.min(), x.max(), 500)
        y_fit = model.predict(x_fit[:, np.newaxis])

        # Draw the polynomial curve
        curve_points = np.array([x_fit, y_fit], dtype=np.int32).T
        cv2.polylines(image_copy, [curve_points], False, (255, 0, 0), 2)

    # Display the updated image
    cv2.imshow('Sidewalk Detection', image_copy)

    # Also display the ROI for reference
    #roi_image = cv2.cvtColor(mask_roi, cv2.COLOR_GRAY2BGR)  # Convert mask to BGR for display
    #cv2.imshow('ROI', roi_image)

def calibrate_sidewalk_hsv(hsv_cropped, h_range, s_range, v_range):
    # Assuming the peak of histograms represent the sidewalk
    h_peak = np.argmax(cv2.calcHist([hsv_cropped], [0], None, [180], [0, 180]))
    s_peak = np.argmax(cv2.calcHist([hsv_cropped], [1], None, [256], [0, 256]))
    v_peak = np.argmax(cv2.calcHist([hsv_cropped], [2], None, [256], [0, 256]))

    lower_hsv = np.array([max(h_peak - h_range, 0), max(s_peak - s_range, 0), max(v_peak - v_range, 0)])
    upper_hsv = np.array([min(h_peak + h_range, 180), min(s_peak + s_range, 255), min(v_peak + v_range, 255)])
    
    return lower_hsv, upper_hsv

# Load the image and define ROI
image_path = '../data/sidewalk_3.jpg'
original_image = cv2.imread(image_path)
hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
roi_height = int(original_image.shape[0] * 0.3)  # Height of the ROI (e.g., 30% of the image height)
roi_y_start = original_image.shape[0] - roi_height  # Y-coordinate where the ROI starts
roi = (0, roi_y_start, original_image.shape[1], original_image.shape[0])  # (x_start, y_start, x_end, y_end)
hsv_roi = hsv[roi[1]:roi[3], roi[0]:roi[2]]

# Create a window with trackbars
cv2.namedWindow('Sidewalk Detection', cv2.WINDOW_NORMAL)
cv2.createTrackbar('H Range', 'Sidewalk Detection', 15, 180, update_image)
cv2.createTrackbar('S Range', 'Sidewalk Detection', 56, 255, update_image)
cv2.createTrackbar('V Range', 'Sidewalk Detection', 208, 255, update_image)

# Initialize the image
update_image()

# Wait for the user to press 'q' to exit
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
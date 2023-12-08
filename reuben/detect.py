import cv2
import numpy as np
from scipy.interpolate import UnivariateSpline

def update_image(*args):
    # Retrieve the current positions of the trackbars
    h_range = cv2.getTrackbarPos('H Range', 'Sidewalk Detection')
    s_range = cv2.getTrackbarPos('S Range', 'Sidewalk Detection')
    v_range = cv2.getTrackbarPos('V Range', 'Sidewalk Detection')

    # Calibrate using the current trackbar values
    lower_hsv, upper_hsv = calibrate_sidewalk_hsv(hsv_roi, h_range, s_range, v_range)

    # Create a mask for the calibrated HSV range and find contours in the ROI
    mask_full = cv2.inRange(hsv, lower_hsv, upper_hsv)
    contours_full, _ = cv2.findContours(mask_full, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_copy = original_image.copy()
    if contours_full:
        # Find the largest contour and its bounding rectangle
        largest_contour_full = max(contours_full, key=cv2.contourArea)
        cv2.drawContours(image_copy, [largest_contour_full], -1, (0, 255, 255), 3)

        # Simplify the contour to a sequence of points
        curve = np.vstack(largest_contour_full).squeeze()
        curve = curve[curve[:, 0].argsort()]  # Sort points by x coordinate

        # Fit splines to the sorted points of the contour
        spline_x = UnivariateSpline(curve[:, 0], curve[:, 1], k=3, s=0.5)
        spline_y = UnivariateSpline(curve[:, 1], curve[:, 0], k=3, s=0.5)

        # Draw points at regular intervals along the x-axis
        num_points = 20
        x_vals = np.linspace(curve[:, 0].min(), curve[:, 0].max(), num_points)
        y_vals = spline_x(x_vals)
        points = np.column_stack((x_vals, y_vals)).astype(int)

        # Draw the points on the image
        for point in points:
            cv2.circle(image_copy, tuple(point), 5, (255, 0, 0), -1)

    # Display the updated image
    cv2.imshow('Sidewalk Detection', image_copy)


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

import cv2
import cv2.aruco as aruco

# Load the image where you want to detect the ArUco code
image_path = '6.jpg'
image = cv2.imread(image_path)

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Load the predefined dictionary
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Initialize the detector parameters using default values
parameters = aruco.DetectorParameters()

# Detect the markers in the image
corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

# Check if at least one marker was detected
if ids is not None:
    # Draw detected markers
    image_with_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)

    # Display the image with detected markers
    cv2.imshow('Detected ArUco Markers', image_with_markers)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No ArUco markers detected.")

# Optionally, you can save the image with detected markers
cv2.imwrite('output_image_with_markers.jpg', image_with_markers)
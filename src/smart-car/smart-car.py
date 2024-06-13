import numpy as np
import cv2
import sys
import socket
import cv2.aruco as aruco
import requests

# Sources:
# ArUco marker detection tutorial: https://docs.opencv.org/4.x/d5/dae/tutorial_aruco_detection.html
# HSV masking: https://docs.opencv.org/3.4/d9/d6a/group__aruco.html 
# Socket connection with Arduino: https://forum.arduino.cc/t/solved-elegoo-smart-robot-car-v4-0-socket-programming-not-working/1207472


# Constants for configuration
livestream_address = "http://@192.168.4.1:81/stream"
commands_ip = "192.168.4.1"
commands_port = 1234
socket_timeout = 0.1

# Initialize socket for communication with the device
car = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
car.settimeout(socket_timeout)

def getCenterOfWhitePixelMass(mask):
    height = mask.shape[0]
    row_height = height // 10 * 1
    last_30_rows = mask[-row_height:]
    mass_x, mass_y = np.where(last_30_rows >= 255)
    # mass_x and mass_y are the list of x indices and y indices of mass pixels
    cent_y = np.average(mass_x)
    cent_x = np.average(mass_y)

    print("Center of mass of white pixels in the last 30 rows:", cent_x)
    return [cent_x, cent_y]

# Function to connect to the device
def connect_to_device():
    try:
        car.connect((commands_ip, commands_port))
        print(f"Connected to {commands_ip}:{commands_port}")
    except Exception as e:
        print(f"Error connecting to device: {e}")
        sys.exit(1)

# Function to send a command to the device
def send_command(command):
    try:
        car.sendall(command.encode('utf-8'))
        print(f"Sent command: {command}")
    except Exception as e:
        print(f"Error sending command: {e}")
        # Handle error gracefully if needed

# Function to receive data from the device
def receive_data():
    try:
        data = car.recv(1024).decode()
        if data:
            print(f"Received data from {commands_ip}:{commands_port}: {data}")
        return data
    except socket.timeout:
        print("Timeout: No data received")
    except Exception as e:
        print(f"Error receiving data: {e}")
        # Handle error gracefully if needed
    return None

# Configure camera settings via HTTP requests to the device
def configure_camera():
    try:
        requests.get("http://192.168.4.1:80/control?var=vflip&val=0")   # Ensure image is not upside down
        requests.get("http://192.168.4.1:80/control?var=framesize&val=9")  # Set resolution to a certain size
        requests.get("http://192.168.4.1:80/control?var=quality&val=4")  # Adjust quality for performance
    except Exception as e:
        print(f"Error configuring camera: {e}")
        

def follow_red_line():
    cap = cv2.VideoCapture(livestream_address)

    while True:
        ret, image = cap.read()
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        if not ret:
            print("Failed to read from camera")
            break
        # Define range of red color in HSV
        lower_red_1 = np.array([0,50,50])
        upper_red_1 = np.array([15,255,255])
        lower_red_2 = np.array([170,50,50])
        upper_red_2 = np.array([255,255,255])

        # Create a mask based of HSV values for the red line
        red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_red_1, upper_red_1), cv2.inRange(hsv, lower_red_2, upper_red_2))
        # Calculate the approximate horizontal center of red line
        [cent_x, _] = getCenterOfWhitePixelMass(red_mask)

        try:
            # Get the image width
            max_value = image.shape[1]
            # Map the horizontal pixel value to a percentage
            mapped_value = int(100 * cent_x / max_value)
            print("X percentage:", mapped_value)
            print(mapped_value)

            # Either send -1 if the horizontal value can not be accurately determined
            # or send the percentage value
            if mapped_value == 0:
                send_command(f"{-1}\n")
            else:
                send_command(f"{mapped_value}\n")
        except:
            print("Cent_x is not a number")
            # There is no red line found and cent_x is therefore not a number

        cv2.imshow('video', red_mask)

        # Handle key press events (ESC to exit loop)
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # ESC key
            cap.release()
            break

# Main function to process video frames and detect traffic lights
def process_video():
    cap = cv2.VideoCapture(livestream_address)

    while True:
        ret, image = cap.read()
        if not ret:
            print("Failed to read from camera")
            break

        image = cv2.GaussianBlur(image, (3, 3), 0)  # Apply Gaussian blur for noise reduction
        green_channel = image[:, :, 1]  # Green channel for thresholding

        # Prepare a black overlay to restrict detection to a specific area (traffic light location)
        black_box = np.ones_like(image)
        x = image.shape[1] // 10
        y = image.shape[0] // 4
        y_2 = y * 3
        black_box[:, 0:x * 7] = 0
        black_box[:y, :] = 0
        black_box[y_2:, :] = 0

        # Thresholding on the green channel
        mask = cv2.inRange(green_channel, 245, 255)
        mask = cv2.bitwise_and(mask, mask, mask=black_box[:, :, 0])

        # HSV range for green color
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lower_green = np.array([45, 50, 100])
        upper_green = np.array([95, 255, 255])
        hsv_green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
        hsv_green_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

        # Calculate area of white pixels in the mask
        white_pixel_area = np.sum(hsv_green_mask == 255)
        print(f"Area of white pixels in the mask: {white_pixel_area}.")

        # Send command to device if traffic light is green
        if white_pixel_area > 50:
            print("Traffic light is green!")
            send_command("1\n")  # Send command to the device

        cv2.imshow('video', hsv_green_mask)

        # Handle key press events (ESC to exit loop)
        k = cv2.waitKey(30) & 0xff
        if k == 27:  # ESC key
            send_command("1\n")  # Send command to stop
            break

        # Check for response from the device acknowledging the green light
        if receive_data() is not None:
            print("Exiting traffic light detection loop")
            break

    cap.release()

# Function to detect ArUco markers in the video stream
def detect_aruco_markers():
    cap = cv2.VideoCapture(livestream_address)

    # Read the video stream per image frame
    while True:
        ret, image = cap.read()
        if not ret:
            print("Failed to read from camera")
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # ArUco detection works best on grayscale images
        aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250) # Get the set of predefined possible ArUco markers
        parameters = aruco.DetectorParameters() #

        # Detect markers in the image
        corners, ids, rejected_img_points = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

        if ids is not None:
            print("ArUco marker detected.")
            average_x_position_aruco = np.average(corners[0][:, :, 0])
            max_value = image.shape[1]
            mapped_value = int(100 * average_x_position_aruco / max_value)
            send_command(f"{mapped_value}\n")  # Send command to the device

            # Draw detected markers
            image_with_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)
            cv2.imshow('video', image_with_markers if image_with_markers is not None else image)
        else:
            print("No ArUco markers detected.")
            send_command(f"{-1}\n")  # Send command indicating no marker detected
            cv2.imshow('video', image)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # ESC key to exit loop
            break

    cap.release()

# Main execution starts here
if __name__ == "__main__":
    try:
        connect_to_device()
        configure_camera()
        process_video()
        # After traffic light detection, resize camera output for better performance
        requests.get("http://192.168.4.1:80/control?var=framesize&val=6")
        detect_aruco_markers()
        # Disabled, for testing purposes only
        # follow_red_line()
    except KeyboardInterrupt:
        print("Keyboard Interrupt: Exiting...")
    finally:
        car.close()  # Close socket connection
        cv2.destroyAllWindows()  # Close OpenCV windows


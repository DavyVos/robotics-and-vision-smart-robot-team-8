import numpy as np
import cv2
import sys
import socket
import cv2.aruco as aruco
import requests

livestream_adress = "http://@192.168.4.1:81/stream"
commands_ip = "192.168.4.1"
commands_port = 1234
car = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
car.settimeout(0.1)

cap = cv2.VideoCapture(livestream_adress)

requests.get("http://192.168.4.1:80/control?var=vflip&val=0")
requests.get("http://192.168.4.1:80/control?var=framesize&val=9")
requests.get("http://192.168.4.1:80/control?var=quality&val=4")

# http_connection.request("GET", "192.168.4.1:80/control?var=vflip&val=0")
# http_connection.request("GET", "192.168.4.1:80/control?var=framesize&val=9")
# http_connection.request("GET", "192.168.4.1:80/control?var=quality&val=4")

print('Connect to {0}:{1}'.format(commands_ip, commands_port))
try:
    car.connect((commands_ip, commands_port))
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Connected!')

def sendCommand(command):
    try:
    # Send the car a message
        car.sendall(command.encode('utf-8'))
        print('Sent: ' + command)
    except:
        print('Error: ', sys.exc_info()[0])
        # sys.exit()


def recieve():
    data = None
    try:
        data = car.recv(1024).decode()
        print('Receive from {0}:{1}'.format(commands_ip, commands_port))
        print('Received: ', data)
    except:
        print('Error: ', sys.exc_info()[0])
        # sys.exit()
    return data


while True:
    ret, image = cap.read()
    image = cv2.GaussianBlur(image,(3,3),0)

    # Prepare for green thresholding
    green_scale = image[:,:,1]

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # create a black overlay to only detect the traffic light in a specific location
    black_box = np.ones_like(image)
    x = image.shape[1] // 10
    y = image.shape[0] // 4
    y_2 = y * 3
    black_box[:, 0:x * 7] = 0
    black_box[:y, :] = 0
    black_box[y_2:, :] = 0

    # Perform thresholding
    mask = cv2.inRange(green_scale, 245, 255)

    # Combine with black overlay
    mask = cv2.bitwise_and(mask, mask, mask=black_box[:, :, 0])

    # HSV lower and upper bounds for green
    lower_green = np.array([45, 50, 100])
    upper_green = np.array([95, 255, 255])

    # Perform HSV range selection
    hsv_green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    # Combine the threshold mask and HSV mask
    hsv_green_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)

    # Calulate the amount of white pixels
    white_pixel_area = np.sum(hsv_green_mask == 255)


    print(f"The area of white pixels in the bit mask is: {white_pixel_area}.")

    # if the amount of white pixels is higher than 4 the traffic light must be green
    if 50 < white_pixel_area:
        print("The traffic light is green!")
        sendCommand("1\n")

    cv2.imshow('video', hsv_green_mask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        sendCommand("1\n")
        break

    # If the robots sends a response, that means our green light is acknowledged
    if recieve() is not None:
        print("Exiting traffic light")
        break

requests.get("http://192.168.4.1:80/control?var=framesize&val=4")

print("Trying to detect aruco...")
while True:
    ret, image = cap.read()
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
        print("ArUco marker detected.")
        average_x_position_aruco = np.average(corners[0][: ,: ,0 ])

        max_value = image.shape[1]

        mapped_value = int(100 * average_x_position_aruco / max_value )

        sendCommand(f"{mapped_value}\n")

        # Draw detected markers
        image_with_markers = aruco.drawDetectedMarkers(image.copy(), corners, ids)

        # Dipslay either the detected aruco or base image
        if image_with_markers is not None:
            cv2.imshow('video', image_with_markers)
        else:
            cv2.imshow('video', image)
    else:
        print("No ArUco markers detected.")
        sendCommand(f"{-1}\n")
        cv2.imshow('video', image)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

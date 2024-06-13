import numpy as np
import cv2
import sys
import socket
import time

livestream_adress = "http://@192.168.4.1:81/stream"
commands_ip = "192.168.4.1"
commands_port = 1234
car = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
        sys.exit()

cap = cv2.VideoCapture(livestream_adress)

while True:
    ret, image = cap.read()
    image = cv2.GaussianBlur(image,(3,3),0)

    green_scale = image[:,:,1]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    black_box = np.ones_like(image)

    x = image.shape[1] // 10
    y = image.shape[0] // 4
    y_2 = y * 3
    black_box[:, 0:x * 7] = 0
    black_box[:y, :] = 0
    black_box[y_2:, :] = 0

    mask = cv2.inRange(green_scale, 245, 255)

    mask = cv2.bitwise_and(mask, mask, mask=black_box[:, :, 0])

    lower_green = np.array([45, 50, 100])
    upper_green = np.array([95, 255, 255])

    hsv_green_mask = cv2.inRange(hsv_image, lower_green, upper_green)
    hsv_green_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
    # result = cv2.cvtColor(hsv_masked, cv2.COLOR_HSV2BGR)

    white_pixel_area = np.sum(hsv_green_mask == 255)


    print(f"The area of white pixels in the bit mask is: {white_pixel_area}.")

    if 4 < white_pixel_area:
        print("The traffic light is green!")
        sendCommand("1\n")
        car.close()
    # else:
    #     sendCommand("0")


    cv2.imshow('video', hsv_green_mask)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break

    # time.sleep(1)

    # lower_red_1 = np.array([0,50,50])
    # upper_red_1 = np.array([15,255,255])
    # lower_red_2 = np.array([170,50,50])
    # upper_red_2 = np.array([255,255,255])

    # hsv_red_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=mask)
    # hsv_red_mask = cv2.bitwise_or(cv2.inRange(hsv_image, lower_red_1, upper_red_1), cv2.inRange(hsv_image, lower_red_2, upper_red_2))
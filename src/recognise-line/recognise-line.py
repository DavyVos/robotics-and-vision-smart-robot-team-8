import numpy as np
import cv2
from matplotlib import pyplot as plt
import os
from scipy import ndimage

# capture video frame 79 

# vidcap = cv2.VideoCapture('\\assets\RV_CV_Assignment2_Rubik.mp4')
# success,image = vidcap.read()
# count = 79
# while success:
#   cv2.imwrite("frame%d.jpg" % count, image)     
#   success,image = vidcap.read()
#   print('Read a new frame: ', success)
#   count += 1

image = cv2.imread('test_yellow_dead_center.png')

cv2.imshow('original', image)
image = cv2.GaussianBlur(image,(5,5),0)

# Convert BGR to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define range of yellow color in HSV
lower_yellow = np.array([15,80,50])
upper_yellow = np.array([50,255,255])

# define range range for red in HSV red is both the upper and lower end of the hue spectrum
lower_red_1 = np.array([0,50,50])
upper_red_1 = np.array([15,255,255])
lower_red_2 = np.array([170,50,50])
upper_red_2 = np.array([255,255,255])

lower_green = np.array([45, 50, 70])
upper_green = np.array([95, 255, 240])

yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
red_mask = cv2.bitwise_or(cv2.inRange(hsv, lower_red_1, upper_red_1), cv2.inRange(hsv, lower_red_2, upper_red_2))
green_mask = cv2.inRange(hsv, lower_green, upper_green)

def getCenterOfWhitePixelMass(mask):
    last_30_rows = mask[-30:]
    mass_x, mass_y = np.where(last_30_rows >= 255)
    # mass_x and mass_y are the list of x indices and y indices of mass pixels
    cent_y = np.average(mass_x)
    cent_x = np.average(mass_y)

    len()

    print("Center of mass of white pixels in the last 30 rows:", cent_y)
    return [cent_x, cent_y]


[cent_x, cent_y] = getCenterOfWhitePixelMass(yellow_mask)
# display the mask and masked image
cv2.imshow('Mask',yellow_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(0)

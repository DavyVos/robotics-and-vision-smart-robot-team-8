import numpy as np
import cv2
from matplotlib import pyplot as plt

image = cv2.imread('red_3.jpg')

green_scale = image[:,:,1]
red_scale = image[:,:,2]
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define a punchout like the original image
punchout_template = np.ones_like(green_scale)

# Create a template to select the right hand side and only the middle 50 percent
x = image.shape[1] // 2
y = image.shape[0] // 4
y_2 = y * 3
punchout_template[:, 0:x] = 0
punchout_template[:y, :] = 0
punchout_template[y_2:, :] = 0

# Define HSV thresholds for the green traffic light
lower_green = np.array([45, 20, 100])
upper_green = np.array([95, 255, 255])

# Define the threshold for the red traffic light, note: red may have two locations on the hue spectrum
lower_red_1 = np.array([0,50,100])
upper_red_1 = np.array([15,255,255])
lower_red_2 = np.array([170,50,100])
upper_red_2 = np.array([255,255,255])

# Perform thresholding on the green channel
green_threshold_mask = cv2.inRange(green_scale, 240, 255)
green_threshold_mask = cv2.bitwise_and(green_threshold_mask, green_threshold_mask, mask=punchout_template)

# Perform thresholding on the red channel
red_threshold_mask = cv2.inRange(red_scale, 240, 255)
red_threshold_mask = cv2.bitwise_and(red_threshold_mask, red_threshold_mask, mask=punchout_template)

# Combine the threshold mask for green with the hsv image and punchout, then perform hsv color selection
green_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=green_threshold_mask)
green_mask = cv2.inRange(green_mask, lower_green, upper_green)

red_mask = cv2.bitwise_and(hsv_image, hsv_image, mask=red_threshold_mask)
red_mask = cv2.bitwise_or(cv2.inRange(red_mask, lower_red_1, upper_red_1), cv2.inRange(red_mask, lower_red_2, upper_red_2))

green_pixel_area = np.sum(green_mask == 255)
red_pixel_area = np.sum(red_mask == 255)


print(f"The area of green pixels in image is: {green_pixel_area}.")
print(f"The area of red pixels in image is: {red_pixel_area}.")

if 100 < green_pixel_area:
    print("The traffic light is green!")

if 100 < red_pixel_area:
    print("The traffic light is red!")


cv2.imshow('Green channel', green_scale)
cv2.imshow('Green threshold mask', red_threshold_mask)
cv2.imshow('Green mask', green_mask)

cv2.imshow('Red channel', red_scale)
cv2.imshow('Red mask', red_mask)

white_background = np.zeros_like(image)
wtf = cv2.bitwise_and(image, image, mask=punchout_template)

cv2.imshow('Punchout template', wtf)

cv2.waitKey(0)
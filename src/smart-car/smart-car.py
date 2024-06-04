import socket
import json
import sys
import cv2

commands_ip = "192.168.4.1"
commands_port = 100
livestream_adress = "http://@192.168.4.1:81/stream" 

msg = json.dumps({ "H": 1 , "N": 5 , "D1": 1 , "D2" : 30})

drive_forward = json.dumps({ "H": 1, "N": 1, "D1": 0, "D2": 255, "D3": 1 })

print('Connect to {0}:{1}'.format(commands_ip, commands_port))
car = socket.socket()
try:
    car.connect((commands_ip, commands_port))
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Connected!')

def sendCommand():
    try:
    # Send the car a message
        car.send(drive_forward.encode())
        print('Sent: ' + drive_forward)
    except:
        print('Error: ', sys.exc_info()[0])
        sys.exit()


def recieve():
    try:
        data = car.recv(1024).decode()
        print('Receive from {0}:{1}'.format(commands_ip, commands_port))
    except:
        print('Error: ', sys.exc_info()[0])
        sys.exit()
    print('Received: ', data)

cap = cv2.VideoCapture(livestream_adress)

while True:
    ret, frame = cap.read()
    cv2.imshow('video', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
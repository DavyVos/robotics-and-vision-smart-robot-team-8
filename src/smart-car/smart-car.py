import socket
import json
import sys
import cv2

commands_ip = "192.168.4.1"
commands_port = 100
livestream_adress = "http://@192.168.4.1:81/stream" 

print('Connect to {0}:{1}'.format(commands_ip, commands_port))
car = socket.socket()
try:
    car.connect((commands_ip, commands_port))
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Connected!')

print('Receive from {0}:{1}'.format(commands_ip, commands_port))

def recieve():
    try:
        data = car.recv(1024).decode()
    except:
        print('Error: ', sys.exc_info()[0])
        sys.exit()
    print('Received: ', data)
    

msg = { "H": 1 , "N": 5 , "D1": 1 , "D2" : 30}

jsonmsg = json.dumps(msg)

off = [0.007,  0.022,  0.091,  0.012, -0.011, -0.05]
try:
    # Send the car a message
    car.send(jsonmsg.encode())
    print('Sent: ' + jsonmsg)
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()


cap = cv2.VideoCapture(livestream_adress)

while True:

    # recieve()
    ret, frame = cap.read()
    cv2.imshow('video', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:  # press 'ESC' to quit
        break
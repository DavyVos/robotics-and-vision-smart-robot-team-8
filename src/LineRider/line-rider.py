import socket
import json
import sys
import cv2

commands_ip = "192.168.4.1"
commands_port = 100

# Set vehicle speed
speed = 65;

lcv = 61 # Left infrared correction value
mcv = 150 # Middel infrared correction value
rcv = 46 # right infrared correction value

thrs = 330 # Threshold infrared value for line detection

# Infrared values
LValue = 0
MValue = 0
RValue = 0


def FollowLine():
#   Set the maximum speed
#   analogWrite(pinLeftSpeed, speed)
#   analogWrite(pinRightSpeed, speed)

#   Drive straight 
    if LValue <= thrs and RValue >= thrs:
        print("drive forward")
        drive_forward = { "H": 1, "N": 1, "D1": 0, "D2": 10, "D3": 1 }
        sendCommand(drive_forward)

#   Turn Left
    elif LValue >= thrs:
        print("drive left")
        drive_left = { "H": 1, "N": 1, "D1": 1, "D2": 10, "D3": 1 }
        sendCommand(drive_left) 

#   Turn Right
    elif RValue <= thrs:
        print("drive right")
        drive_right = { "H": 1, "N": 1, "D1": 2, "D2": 10, "D3": 1 }
        sendCommand(drive_right) 

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

def sendCommand(command):
    json_command = json.dumps(command)
    try:
    # Send the car a message
        car.send(json_command.encode())
        print('Sent: ' + json_command)
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
    return data


def getYoDigits(value):
    return ''.join(char for char in value if char.isdigit())

recieve()

while True:
    print("get left value")
    get_left_infrared = { "H": 1 , "N": 22 , "D1": 0 }
    print("get middle value")
    get_middle_infrared = { "H": 1 , "N": 22 , "D1": 1 }
    print("get left value")
    get_right_infrared = { "H": 1 , "N": 22 , "D1": 2 }

    sendCommand(get_left_infrared)
    LValue = getYoDigits(recieve())
    LValue = int(LValue) if LValue else 0
    sendCommand(get_middle_infrared)
    MValue = getYoDigits(recieve())
    MValue = int(LValue) if MValue else 0
    sendCommand(get_right_infrared)
    RValue = getYoDigits(recieve())
    RValue = int(RValue) if RValue else 0

    FollowLine()


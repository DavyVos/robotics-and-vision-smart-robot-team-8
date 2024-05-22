import socket
import json
import sys
import time
import re

# Yes, I know thatt I'm not using time or re.

ip = "192.168.4.1"
port = 100
print('Connect to {0}:{1}'.format(ip, port))
car = socket.socket()
try:
    car.connect((ip, port))
except:
    print('Error: ', sys.exc_info()[0])
    sys.exit()
print('Connected!')

print('Receive from {0}:{1}'.format(ip, port))

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

recieve()
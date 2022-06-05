#!/usr/bin/env python
## SERVER

import argparse
import serial
import socket
import time
import os
import sys

serialPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
serialPort.flush()
if serialPort.isOpen():
    serialPort.close()
serialPort.open()

lastSerialSentAt = time.time()

def dataToSerialCommands(data):
    if ('w' in data) and ('s' in data):
        # Dont move
        sendSerialCommand(0,0,0)
    elif ('s' in data) and ('a' in data) and ('d' in data):
        # move backwards
        sendSerialCommand(1023,1023,1)
    elif ('s' not in data) and ('w' not in data) and ('a' in data) and ('d' in data):
        # move forewards
        sendSerialCommand(1023,1023,0)
    elif ('w' in data) and ('a' in data) and ('d' in data):
        # move forewards
        sendSerialCommand(1023,1023,0)
    elif ('s' in data) and ('a' in data):
        # move back to the left
        sendSerialCommand(0,1023,1)
    elif ('s' in data) and ('d' in data):
        # move back to the right
        sendSerialCommand(1023,0,1)
    elif ('w' in data) and ('a' in data) or ('a' in data):
        # move left
        sendSerialCommand(0,1023,0)
    elif ('w' in data) and ('d' in data) or ('d' in data):
        # move right
        sendSerialCommand(1023,0,0)
    elif ('w' in data):
        # move forewards
        sendSerialCommand(1023,1023,0)
    elif ('s' in data):
        # move back
        sendSerialCommand(1023,1023,1)
    else:
        sendSerialCommand(0,0,0)


def sendSerialCommand(leftMotorValue, rightMotorValue, direction):
    global lastSerialSentAt
    global serialPort
    l = (leftMotorValue).to_bytes(2, byteorder="big", signed=False)
    r = (rightMotorValue).to_bytes(2, byteorder="big", signed=False)
    d = (direction).to_bytes(1, byteorder="big", signed=False)
    if(time.time() - lastSerialSentAt < 0.2):
        # Make sure not to overflow the serial interface maan!
        return
    serialPort.write(l)
    serialPort.write(r)
    serialPort.write(d)
    serialPort.write("\n".encode())
    lastSerialSentAt = time.time()
    print("Sent to serial", l, r, d)


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(1) # N.o paralell clients
    while True:
        conn, address = server_socket.accept()  # Accept new connection
        print("Connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("Recieved from client: " + str(data))
            dataToSerialCommands(str(data))
        conn.close()
        serialPort.close()


if __name__ == '__main__':
    server_program()

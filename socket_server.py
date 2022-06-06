#!/usr/bin/env python
## SERVER

import argparse
import serial
import socket
import time
import os
import sys
import datetime
from pathlib import Path

simulatorModeOn = False
TOP_SPEED = 140
logFileName = None
serialPort = None
lastSerialSentAt = time.time()

def log(text):
    global logFileName
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    label = "INFO"
    logRow = str(t) + " " + str(label) + " " + str(text)
    print(logRow)
    with open(logFileName, "a+") as fp:
        fp.write(logRow+ "\n")

def openSerialConncetion():
    global serialPort
    try:
        serialPort = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        serialPort.flush()
        if serialPort.isOpen():
            log("Closing already open serial connection")
            serialPort.close()
        serialPort.open()
        log("New serial port opened")
    except Exception as e:
        log(str(e))
        raise e

def dataToSerialCommands(data):
    global TOP_SPEED
    if ('w' in data) and ('s' in data):
        # Dont move
        sendSerialCommand(0,0,0)
    elif ('s' in data) and ('a' in data) and ('d' in data):
        # move backwards
        sendSerialCommand(TOP_SPEED,TOP_SPEED,1)
    elif ('s' not in data) and ('w' not in data) and ('a' in data) and ('d' in data):
        # move forewards
        sendSerialCommand(TOP_SPEED,TOP_SPEED,0)
    elif ('w' in data) and ('a' in data) and ('d' in data):
        # move forewards
        sendSerialCommand(TOP_SPEED,TOP_SPEED,0)
    elif ('s' in data) and ('a' in data):
        # move back to the left
        sendSerialCommand(0,TOP_SPEED,1)
    elif ('s' in data) and ('d' in data):
        # move back to the right
        sendSerialCommand(TOP_SPEED,0,1)
    elif ('w' in data) and ('a' in data) or ('a' in data):
        # move left
        sendSerialCommand(0,TOP_SPEED,0)
    elif ('w' in data) and ('d' in data) or ('d' in data):
        # move right
        sendSerialCommand(TOP_SPEED,0,0)
    elif ('w' in data):
        # move forewards
        sendSerialCommand(TOP_SPEED,TOP_SPEED,0)
    elif ('s' in data):
        # move back
        sendSerialCommand(TOP_SPEED,TOP_SPEED,1)
    else:
        sendSerialCommand(0,0,0)


def sendSerialCommand(leftMotorValue, rightMotorValue, direction):
    global lastSerialSentAt
    global serialPort
    global simulatorMode
    l = (leftMotorValue).to_bytes(2, byteorder="big", signed=False)
    r = (rightMotorValue).to_bytes(2, byteorder="big", signed=False)
    d = (direction).to_bytes(1, byteorder="big", signed=False)
    if(time.time() - lastSerialSentAt < 0.2):
        # Make sure not to overflow the serial interface maan!
        return
    if not simulatorModeOn:
        serialPort.write(l)
        serialPort.write(r)
        serialPort.write(d)
        serialPort.write("\n".encode())

    lastSerialSentAt = time.time()
    log("Sent to serial (leftmotor, rightmotor, direction ): " + str(l) + ", " + str(r) + ", " + str(d))
    if simulatorModeOn:
        log("OK\n")
    else:
        log(serialPort.read(3))

def server_program():
    global serialPort
    # get the hostname
    host = "0.0.0.0"
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1) # N.o paralell clients
    log("Started webserver: " + str(host) + ":" + str(port))
    while True:
        time.sleep(0.1)
        conn, address = server_socket.accept()  # Accept new connection
        log("Got connection from: " + str(address))
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print("Datagram recieved: " + str(data))
            dataToSerialCommands(str(data))
        log("Lost connection from" + str(address))
        conn.close()
        if not simulatorModeOn:
            serialPort.close()

if __name__ == '__main__':
    try:
        if sys.argv[1] == "simulator":
            simulatorModeOn = True
    except Exception:
        pass

    if simulatorModeOn:
        logFileName = str(Path.home()) + "/lawnmower/logs/server-simulator-" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+".log"
        Path(logFileName).touch(exist_ok=True)
        log("Starting in simulator mode ON")
    else:
        logFileName = str(Path.home()) + "/lawnmower/logs/server-" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+".log"
        Path(logFileName).touch(exist_ok=True)
        log("Starting")
        openSerialConncetion()

    server_program()

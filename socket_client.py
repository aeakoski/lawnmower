#!/usr/bin/env python
## CLIENT

import socket
import tty
import sys
import keyboard
import time
from pathlib import Path
import datetime

logFileName = None

def log(text, silent = False):
    global logFileName
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    label = "INFO"
    logRow = str(t) + " " + str(label) + " " + str(text)
    if not silent:
        print(logRow)
    with open(logFileName, "a+") as fp:
        fp.write(logRow+ "\n")


def client_program():
    try:
        h = sys.argv[1]
    except Exception:
        h = socket.gethostname()
        print("Provide hostname as first argument, using default: " + str(h))
    try:
        p = int(sys.argv[2])
    except Exception:
        p = 5000
        print("Provide port as second argument, using default: " + str(p))
    x = 0
    lastMessage = " "
    host = h
    port = p

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server
    print("Connected")
    print("You can now use W-A-S-D keys to controll the mower")
    while True:
        time.sleep(0.01)

        x = ""
        if keyboard.is_pressed('w'):
            x = x + "w"
        if keyboard.is_pressed('a'):
            x = x + "a"
        if keyboard.is_pressed('s'):
            x = x + "s"
        if keyboard.is_pressed('d'):
            x = x + "d"
        elif keyboard.is_pressed('q'):
            break

        print("                ", end="\r")
        print("You pressed " + str(x), end="\r")
        if lastMessage == "" and x == "":
            pass
        else:
            log("Sending package with keypress: " + str(x), silent = True)
            client_socket.send(x.encode())  # send message
            lastMessage = x
            time.sleep(0.2)

    client_socket.close()  # close the connection
    raise Exception()

if __name__ == '__main__':
    try:
        logFileName = str(Path.home()) + "/lawnmower/logs/client-" + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')+".log"
        Path(logFileName).touch(exist_ok=True)
        log("Starting")

        client_program()
    except Exception as e:
        print("Exiting")
        print(e)

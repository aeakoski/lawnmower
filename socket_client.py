#!/usr/bin/env python
## CLIENT

import socket
import tty
import sys
import keyboard
import time

def client_program():
    x = 0
    lastMessage = " "
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

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
            client_socket.send(x.encode())  # send message
            lastMessage = x
            time.sleep(0.3)

    client_socket.close()  # close the connection
    raise Exception()

if __name__ == '__main__':
    try:
        client_program()
    except Exception as e:
        print("Exiting")
        print(e)

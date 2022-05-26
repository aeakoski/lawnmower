## CLIENT

import socket
import tty
import sys
import termios
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
    while True:
        time.sleep(0.01)

        x = " "

        if keyboard.is_pressed('w'):  # if key 'q' is pressed
            x= "w"
        elif keyboard.is_pressed('a'):  # if key 'q' is pressed
            x= "a"
        elif keyboard.is_pressed('s'):  # if key 'q' is pressed
            x= "s"
        elif keyboard.is_pressed('d'):  # if key 'q' is pressed
            x= "d"
        elif keyboard.is_pressed('q'):  # if key 'q' is pressed
            x= "q"
            break
        print("You pressed", x, end="\r")

        if lastMessage == " " and x == " ":
            pass
        else:
            client_socket.send(x.encode())  # send message
            lastMessage = x

        # TODO Make it so all new keypresses overwrite the previous one in the cosole

    client_socket.close()  # close the connection
    raise Exception()


if __name__ == '__main__':
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    try:
        client_program()

    except Exception as e:
        print("Exiting")
        print(e)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

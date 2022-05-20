## CLIENT

import socket
import tty
import sys
import termios

def client_program():
    x = 0
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    while True:
        x=sys.stdin.read(1)[0]
        if x == chr(27): # ESC
            break
        client_socket.send(x.encode())  # send message

        print("You pressed", x)
        # TODO Make it so all new keypresses overwrite the previous one in the cosole

    client_socket.close()  # close the connection
    raise Exception()


if __name__ == '__main__':
    orig_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin)

    try:
        client_program()

    except:
        print("Exiting")
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)

## SERVER

import socket


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
            print("from connected user: " + str(data))
            ## TODO call serial here with the parsed input from the socket
        conn.close()


if __name__ == '__main__':
    server_program()

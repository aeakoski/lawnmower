import numpy as np
import socket
import time


class Mower:
    def __init__(self, host, port):
        self.direction = 0
        self.frontFramePosition = [0,0]
        self.backFramePosition = [0,0]
        self.lawnPosition = [0,0]

        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((host, port))  # connect to the server

    def calculateOrientation(self):
        v1 = (1,0,0)
        v2 = (self.frontFramePosition[0]-self.backFramePosition[0],self.frontFramePosition[1]-self.backFramePosition[1], 0) / np.linalg.norm((self.frontFramePosition[0]-self.backFramePosition[0],self.frontFramePosition[1]-self.backFramePosition[1], 0))
        return np.arccos(np.clip(np.dot(v1, v2), -1.0, 1.0))*57.2957795
    def calculateMowerOrientationTowards(self, coodinate):
        mouseClick_v1 = (coodinate[0]-self.backFramePosition[0], coodinate[1]-self.backFramePosition[1],0) / np.linalg.norm((coodinate[0]-self.backFramePosition[0], coodinate[1]-self.backFramePosition[1],0))
        mower_v2 = (self.frontFramePosition[0]-self.backFramePosition[0],self.frontFramePosition[1]-self.backFramePosition[1], 0) / np.linalg.norm((self.frontFramePosition[0]-self.backFramePosition[0],self.frontFramePosition[1]-self.backFramePosition[1], 0))
        return np.arccos(np.clip(np.dot(mouseClick_v1, mower_v2), -1.0, 1.0))*57.2957795

    def turnLeft(self):
        print("Trying to turn Left1")
        self.client_socket.send("a".encode())
        time.sleep(0.3)
        print("Trying to turn Left2")
        self.client_socket.send("a".encode())
        time.sleep(0.3)
        print("Trying to turn Left3")
        self.client_socket.send("a".encode())
        time.sleep(0.3)
        print("Trying to turn Left4")
        self.client_socket.send("a".encode())
        time.sleep(1.5)
    def turnRight(self):
        print("Trying to turn Right")
        self.client_socket.send("d".encode())
        time.sleep(0.3)
        self.client_socket.send("d".encode())
        time.sleep(0.3)
        self.client_socket.send("d".encode())
        time.sleep(0.3)
        self.client_socket.send("d".encode())
        time.sleep(1.5)

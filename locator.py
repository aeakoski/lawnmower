import time
import cv2
import numpy as np
import Lawn
import Mower
import os

red_lower = np.array([160,200,40])
red_upper = np.array([180, 255, 255])
blue_lower = np.array([90,90,30])
blue_upper = np.array([130, 255, 255])

video = cv2.VideoCapture("rtsp://" + os.environ['RTSP_USER_COLON_PASSWORD'] + "@192.168.1.53:554/stream1")
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 540
LOG_FILTER=10

wScale = 2.0
hScale = 2.0
#the [x, y] for each right-click event will be stored here
boundary = list()

myLawn = Lawn.Lawn()
myMower = Mower.Mower("192.168.1.227", 5000)

import threading
class controllerThread(threading.Thread):
    def __init__(self, myMower, x, y):
        self.myMower = myMower
        self.mX = x
        self.mY = y
        threading.Thread.__init__(self)
    def run(self):
        print("RUNING THREAD FROM WITHIN")
        oldMowerAngle = self.myMower.calculateMowerOrientationTowards([self.mX, self.mY])
        mowerAngle = self.myMower.calculateMowerOrientationTowards([self.mX, self.mY])
        turnLeft = True
        print(self.mX, self.mY)
        print(mowerAngle, oldMowerAngle)
        while mowerAngle > 30:
            #Save current state
            oldMowerAngle = self.myMower.calculateMowerOrientationTowards([self.mX, self.mY])
            #Execute plan
            print("Running")
            if turnLeft:
                myMower.turnLeft()
            else:
                myMower.turnRight()

            #Evaluate
            print("Evaluating")
            noShows = 0
            while mowerAngle == self.myMower.calculateMowerOrientationTowards([self.mX, self.mY]):
                time.sleep(0.5)
                noShows += 1
                if noShows == 6:
                    return
            mowerAngle = self.myMower.calculateMowerOrientationTowards([self.mX, self.mY])
            print("OLD-MOWERANGLE: " + str(oldMowerAngle))
            print("MOWERANGLE: " + str(mowerAngle))
            if mowerAngle > oldMowerAngle :
                turnLeft = not turnLeft


#this function will be called whenever the mouse is right-clicked
def boundary_mouse_callback(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONUP:
        global boundary
        boundary.append([x, y]) #store the coordinates of the right-click event
        print(boundary)

def goto_mouse_callback(event, x, y, flags, params):
    global myMower
    global wScale
    global hScale
    if event == cv2.EVENT_LBUTTONUP:
        print("MOUSEEVENT")
        print("New thread created")
        thread1 = controllerThread(myMower, x*wScale, y*hScale)

        print("Starting")
        thread1.start()

def scalarMultiply(scalar, vector):
    return [x*scalar for x in vector]

def pickBoundary():
    print("Click four times to define the boundary of the mower")
    global wScale
    global hScale
    global video
    global boundary
    global myLawn
    w = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    while len(boundary) < 4:
        success, img = video.read()
        img = cv2.resize(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        cv2.namedWindow("Locator", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Locator", WINDOW_WIDTH, WINDOW_HEIGHT)
        cv2.setMouseCallback("Locator", boundary_mouse_callback)
        cv2.imshow("Locator", img)
        cv2.waitKey(1)

    wScale = w/WINDOW_WIDTH
    hScale = h/WINDOW_HEIGHT

    myLawn.defineBoundaries(
        [boundary[0][0]*wScale, boundary[0][1]*hScale],
        [boundary[1][0]*wScale, boundary[1][1]*hScale],
        [boundary[2][0]*wScale, boundary[2][1]*hScale],
        [boundary[3][0]*wScale, boundary[3][1]*hScale]
        )
    print("doneCalculating")
    return

def getCenterFromCountours(contours):
    global img
    center = []
    if len(contours) == 0 :
        return []
    for contour in contours:
        if cv2.contourArea(contour) > 1200:
            x, y, w, h = cv2.boundingRect(contour)
            #cv2.rectangle(img, (x,y), (x + w, y + h), (0,0,255), 3)
            ## Calculate center of colored area
            M = cv2.moments(contour)
            if M['m00'] != 0:
                center_x = int(M['m10']/M['m00'])
                center_y = int(M['m01']/M['m00'])
                center.append((center_x, center_y))
    if len(center) >= 1:
        return center
    else:
        return []


img = None
def main():
    global myLawn
    global goto
    global img
    while True:
        success, img = video.read()
        if not success:
            break

        image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        red_mask = cv2.inRange(image, red_lower, red_upper)
        blue_mask = cv2.inRange(image, blue_lower, blue_upper)

        back_contours, red_hierarchy = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        front_contours, blue_hierarchy = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        backCoordinates = myLawn.filterForCoordinatesOnLawn(getCenterFromCountours(back_contours))
        frontCoordinates = myLawn.filterForCoordinatesOnLawn(getCenterFromCountours(front_contours))

        #print(backCoordinates)
        #print(frontCoordinates)

        if (len(backCoordinates) == 1 and len(frontCoordinates) == 1 ):

            backCoordinates = backCoordinates[0]
            frontCoordinates = frontCoordinates[0]

            cv2.circle(img, backCoordinates, 7, (0, 0, 255), -1)
            cv2.circle(img, frontCoordinates, 7, (0, 0, 255), -1)
            cv2.arrowedLine(img, backCoordinates, frontCoordinates, (255, 255, 0), 9)
            myMower.frontFramePosition = frontCoordinates
            myMower.backFramePosition = backCoordinates
        ##print(f"x: {center_x} y: {center_y}")

        #blue_mask = cv2.resize(red_mask, (WINDOW_WIDTH, WINDOW_HEIGHT))
        #cv2.imshow("locator", blue_mask)

        cv2.polylines(img, [myLawn.getPlotableBoundaryCoordinates()], True, (0,255,0), thickness=3)

        img = cv2.resize(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        cv2.namedWindow("Locator", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Locator", WINDOW_WIDTH, WINDOW_HEIGHT)
        cv2.setMouseCallback("Locator", goto_mouse_callback)
        cv2.imshow("Locator", img)
        cv2.waitKey(1)


if __name__ == '__main__':
    #pickBoundary()
    myLawn.defineBoundaries([407*2, 201*2], [619*2, 235*2], [472*2, 532*2], [240*2, 415*2])
    main()

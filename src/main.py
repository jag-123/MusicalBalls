# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
    help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
    help="max buffer size")
args = vars(ap.parse_args())
 
# define the lower and upper boundaries of the colors in the HSV color space
lower = {'pink':(140, 30, 100), 'red':(0,100,130), 'orange':(10, 155, 125), 'yellow':(23, 30, 150), 'green':(40, 27, 129), 'blue':(97, 100, 117), 'white':(0,0,170)} #assign new item lower['blue'] = (93, 10, 0)
upper = {'pink':(180,150,255), 'red':(15,200,255), 'orange':(25,255,255), 'yellow':(40,230,255),  'green':(65,130,255), 'blue':(117,255,255), 'white':(35,40,255)}

# define standard colors for circle around the object
colors = {'pink':(160,50,200), 'red':(0,0,255),'green':(0,255,0), 'blue':(255,0,0), 'yellow':(0, 255, 217), 'orange':(0,140,255), 'white':(255,255,255)}

#pts = deque(maxlen=args["buffer"])
 
# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
    camera = cv2.VideoCapture(1)
# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

#start osc system
osc_startup()
# Make client channels to send packets.
osc_udp_client("127.0.0.1", 5050, "my_computer")

# keep looping
while True:

    # grab the current frame
    (grabbed, frame) = camera.read()
    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break
 
    # resize the frame, blur it, and convert it to the HSV
    # color space
    frame = imutils.resize(frame, width=600)

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    balls_array = []
    #for each color in dictionary check object in frame
    for key, value in upper.items():
        # construct a mask for the color from dictionary, then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        kernel = np.ones((9,9),np.uint8)
        mask = cv2.inRange(hsv, lower[key], upper[key])
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                
        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        
        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            # c = max(cnts, key=cv2.contourArea)
            for c in cnts:
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
                # only proceed if the radius meets a minimum size. Correct this value for your obect's size
                if radius > 35.0 and radius < 45.0:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points

                    cv2.circle(frame, (int(x), int(y)), int(radius), colors[key], 2)
                    cv2.putText(frame,key + " ball" , (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6,colors[key],2)
                    balls_array.append((key,int(x),int(y)))

    sorted_balls = []
    row_1,row_2,row_3,row_4 = [None,None,None,None], [None,None,None,None], [None,None,None,None], [None,None,None,None]
    for tup in balls_array:
        print(tup)
        if tup[2] > 0 and tup[2] < 100:
            if tup[1] > 60 and tup[1] < 200:
                row_1[0] = tup[0]
            if tup[1] > 200 and tup[1] < 320:
                row_1[1] = tup[0]
            if tup[1] > 320 and tup[1] < 450:
                row_1[2] = tup[0]
            if tup[1] > 450 and tup[1] < 580:
                row_1[3] = tup[0]
        if tup[2] > 100 and tup[2] < 220:
            if tup[1] > 60 and tup[1] < 200:
                row_2[0] = tup[0]
            if tup[1] > 200 and tup[1] < 320:
                row_2[1] = tup[0]
            if tup[1] > 320 and tup[1] < 450:
                row_2[2] = tup[0]
            if tup[1] > 450 and tup[1] < 580:
                row_2[3] = tup[0]
        if tup[2] > 220 and tup[2] < 360:
            if tup[1] > 60 and tup[1] < 200:
                row_3[0] = tup[0]
            if tup[1] > 200 and tup[1] < 320:
                row_3[1] = tup[0]
            if tup[1] > 320 and tup[1] < 450:
                row_3[2] = tup[0]
            if tup[1] > 450 and tup[1] < 580:
                row_3[3] = tup[0]
        if tup[2] > 360 and tup[2] < 500:
            if tup[1] > 60 and tup[1] < 200:
                row_4[0] = tup[0]
            if tup[1] > 200 and tup[1] < 320:
                row_4[1] = tup[0]
            if tup[1] > 320 and tup[1] < 450:
                row_4[2] = tup[0]
            if tup[1] > 450 and tup[1] < 580:
                row_4[3] = tup[0]

    sorted_balls.append(row_1)
    sorted_balls.append(row_2)
    sorted_balls.append(row_3)
    sorted_balls.append(row_4)

    for row in sorted_balls:
        print(row)

    for i,tup in enumerate(row_1):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage("/row1/"+str(i+1), None, [tup])

        osc_send(msg, "my_computer")
        osc_process()
    for i,tup in enumerate(row_2):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage("/row2/"+str(i+1), None, [tup])

        osc_send(msg, "my_computer")
        osc_process()
    for i,tup in enumerate(row_3):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage("/row3/"+str(i+1), None, [tup])

        osc_send(msg, "my_computer")
        osc_process()
    for i,tup in enumerate(row_4):
        # Build a message with autodetection of data types, and send it.
        msg = oscbuildparse.OSCMessage("/row4/"+str(i+1), None, [tup])

        osc_send(msg, "my_computer")
        osc_process()

     
    # show the frame to our screen
    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1) & 0xFF
    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        osc_terminate()
        break
 
# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
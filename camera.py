from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
camera.crop = (0,0,0,0)
rawCapture = PiRGBArray(camera, size=(640, 480))
#camera.color_effects = (128,128)

LEFT_cascade = cv2.CascadeClassifier('Left_3.xml')
RIGHT_cascade = cv2.CascadeClassifier('Right3.xml')
STOP_cascade = cv2.CascadeClassifier('Stop_3.xml')
TRAFFIC_cascade = cv2.CascadeClassifier('Traffic_3.xml')

time.sleep(0.5)
font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    image = image[50:400,0:640]
##    cv2.normalize(image,image,0,255,cv2.NORM_MINMAX)
    STOP = STOP_cascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=10)    
    LEFT = LEFT_cascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=10)
    RIGHT = RIGHT_cascade.detectMultiScale(image,scaleFactor=1.1,minNeighbors=10)
    TRAFFIC = TRAFFIC_cascade.detectMultiScale(image,scaleFactor=1.05,minNeighbors=10)
    gray = image

    
    for (x,y,w,h) in LEFT:
        h=h*.95
        h=int(h)
        dist = (((3.04*71.5*480)/(h*2.76))-55)/10
        if dist > 7 and dist < 20:
            cv2.putText(image,'LEFT: '+str(int(dist))+"cm",(x,y+h+25), font, 1,(0,255,0))
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
    
    for (x,y,w,h) in RIGHT:
        dist = (((3.04*70.5*480)/(h*2.76))-55)/10
        if dist > 7 and dist < 20:
            cv2.putText(image,'RIGHT: '+str(int(dist))+"cm",(x,y+h+25), font, 1,(255,0,0))
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),2)
        
    for (x,y,w,h) in STOP:
        dist = (((3.04*65*480)/(h*2.76))-55)/10
        if dist > 7 and dist < 20:
            cv2.putText(image,'STOP: ' +str(int(dist))+"cm",(x,y+h+25), font, 1,(0,0,255))
            cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255),2)

    for (x,y,w,h) in TRAFFIC:
        h=h*1.08
        h=int(h)
        y=y-((h*1.05)-h)
        y=int(y)
        y2 = int(y+h/2)
        dist = (((3.04*61*480)/(h*2.76))-55)/10
        if dist > 7 and dist < 20:
            cv2.putText(image,'TRAFFIC: ' +str(int(dist))+"cm",(x,y+h+25), font, 1,(0,255,255))
            cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),2)
            cv2.line(image,(x,y2),((x+w),y2), (255,0,0),2)
            trafficROI = image[y:(y+h),x:(x+w)]
            image2 = cv2.cvtColor(trafficROI,  cv2.COLOR_BGR2GRAY)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(image2)
            px = max_loc[0]+x
            py = max_loc[1]+y
            if max_val > 250 and py < y2:
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255),2)
                cv2.line(image,(x,y2),((x+w),y2), (0,0,255),2)
                cv2.circle(image, (px,py), 10, (0, 0, 255), 2)
                
            if max_val > 250 and py > y2:
                cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
                cv2.line(image,(x,y2),((x+w),y2), (0,255,0),2)
                cv2.circle(image, (px,py), 10, (0, 255, 0), 2)
            



    cv2.imshow("Frame", image)
    #cv2.imshow("G", image2)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)


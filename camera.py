from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import sys

camera = PiCamera()
camera.resolution = (640, 480)
camera.crop = (0,0,0,0)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
#camera.color_effects = (128,128)

LEFT_cascade = cv2.CascadeClassifier('LEFT_CASCADE.xml')
RIGHT_cascade = cv2.CascadeClassifier('RIGHT_CASCADE.xml')
STOP_cascade = cv2.CascadeClassifier('STOP_CASCADE_995.xml')

time.sleep(0.5)
font = cv2.FONT_HERSHEY_SIMPLEX

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image = frame.array
    image = image[80:440,0:640]
    STOP = STOP_cascade.detectMultiScale(image,scaleFactor=1.2,minNeighbors=55)    
    LEFT = LEFT_cascade.detectMultiScale(image,scaleFactor=1.2,minNeighbors=25)
    RIGHT = RIGHT_cascade.detectMultiScale(image,scaleFactor=1.2,minNeighbors=25)

    for (x,y,w,h) in LEFT:
        cv2.putText(image,'LEFT',(x,y-10), font, 1,(0,255,0))
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,255,0),2)
    
    for (x,y,w,h) in RIGHT:
        cv2.putText(image,'RIGHT',(x,y-10), font, 1,(255,0,0))
        cv2.rectangle(image, (x,y), (x+w, y+h), (255,0,0),2)
        
    for (x,y,w,h) in STOP:
        cv2.putText(image,'STOP',(x,y-10), font, 1,(0,0,255))
        cv2.rectangle(image, (x,y), (x+w, y+h), (0,0,255),2)


    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF

    rawCapture.truncate(0)


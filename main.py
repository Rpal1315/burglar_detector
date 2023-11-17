import cv2
import numpy as np
import datetime

cam = cv2.VideoCapture(0)
while cam.isOpened():
    ret,frame1 = cam.read()
    ret,frame2 = cam.read()
    diff = cv2.absdiff(frame1,frame2)
    grey = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey,(5,5),0)
    _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dialted = cv2.dilate(thresh,None,iterations=3)
    contours,_ = cv2.findContours(dialted,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    last_mean = 0
    date = datetime.datetime.now()
    
    for c in contours:
        if cv2.contourArea(c) < 5000:
            continue
        x,y,width,height = cv2.boundingRect(c)
        cv2.rectangle(frame1,(x,y),(x+width,y+height),(0,255,0),2)
        result = np.abs(np.mean(grey) - last_mean)
        if result > 0.3:
            print(f"Motion detected on {date.strftime('%d')}-{date.strftime('%m')}-{date.strftime('%Y')} at "
                  f"{date.strftime('%H')}{date.strftime('%M')}")

    if (cv2.waitKey(1) & 0xFF == ord('q')):
        break

    cv2.imshow('Burglar Cam',frame1)




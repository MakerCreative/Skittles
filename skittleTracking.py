'''
Created on Jul 28, 2014

@author: kedwards
'''

import cv2
import numpy as np
import cnc

def findSkittle(f):
    
    # work in grayscale
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)

    # equalize the histogram - spread out the gray's
    he = cv2.equalizeHist(gray)
    
    # blur the image a bit
    blur2 = cv2.GaussianBlur(he,(5,5),0)
  
    # threshold the iamge, find the right spot to separate the skittle from the background
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    # use a morphological operator to clean up the result
    kernelSize = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernelSize,kernelSize))
    atClose = cv2.morphologyEx(at, cv2.MORPH_CLOSE, kernel)
    
    # find the contours in the image, that is all the connected dots 
    contours,hierarchy = cv2.findContours(atClose,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    maxArea = 0
    maxC = []
    
    # loop through all the countours, find the biggest one
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxArea = area
            maxC = contour
            
    # at the end we've found the maximum contour
    # find the smallest circle that encloses that maximum contour
    minCircleCenter,minCircleRadius = cv2.minEnclosingCircle(maxC)
    
    
   
    
    # find the center of the image and draw a circle there
    frameSize = f.shape
    frameCenter = ( int(frameSize[1] / 2), int(frameSize[0] / 2 ))
    
    # instead of using the center of the min circle, let's use the moment of the contour
    m = cv2.moments(maxC)
    contourCenter = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
    
    
    # draw what we've found in the image
    
    # some colours to draw with - we are BGR from the webcam
    red   = ( 000 , 000 , 255 )    
    green = ( 000 , 255 , 000 )
    blue  = ( 255 , 000 , 000 )
   
    
    cv2.drawContours(f,maxC, -1,(255,255,255),-1)
    
    cv2.circle(f, (int(minCircleCenter[0]),int(minCircleCenter[1])), 5, green, -1)
    
    cv2.circle(f, frameCenter , 5, red, -1)
    
    # draw a line between the center of the image and the center of the skittle
    cv2.line(f, frameCenter , (int(minCircleCenter[0]),int(minCircleCenter[1])), red,2)
 
 
    cv2.circle(f, contourCenter, 5, blue, -1)

    
    cv2.imshow('TEST 11: Contour Circles',f)
    return

#####################################################################################
if __name__ == "__main__":
    
    #cnc.init()
        
    c = cv2.VideoCapture(0)
    
    goodImage,frameOld = c.read()
    
    while(goodImage):
    
        goodImage,frame = c.read()
        if not goodImage:
            break
  
        # make the image look right as if we are facing the front of the shapeoko  
        frame = cv2.flip(frame,-1)   
        
        
        #some temporal averaging for frame11
        frameAvg = cv2.addWeighted(frame,.9,frameOld,.1,0)
        findSkittle(frameAvg)
        frameOld = frameAvg.copy()
        
        # wait for a key press and see if we need to do anything
        key = cv2.waitKey(50) 
        if key == 27:
            break
                
    # program is done, clean up
    cv2.destroyAllWindows()
    c.release()

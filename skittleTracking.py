'''
Created on Jul 28, 2014

@author: kedwards
'''

import cv2
import numpy as np
import cnc
import time

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
    
    # find the center of the image and draw a circle there
    frameSize = f.shape
    frameCenter = ( int(frameSize[1] / 2), int(frameSize[0] / 2 ))
    
    # find the middle point of all the points on the contour
    m = cv2.moments(maxC)
    contourCenter = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
    
    delta = np.subtract( contourCenter , frameCenter)
    distance = np.linalg.norm(delta)

    # draw what we've found in the image
    # some colours to draw with - we are BGR from the webcam
    red   = ( 000 , 000 , 255 )    
    green = ( 000 , 255 , 000 )
    blue  = ( 255 , 000 , 000 )
    white = ( 255 , 255 , 255 )
    black = ( 000 , 000 , 000 )
    
    maxDistance = 200
    if distance < maxDistance: 
        cv2.drawContours(f,maxC, -1, white ,-1)
        
        cv2.circle(f, frameCenter , 7, red, -1)
        cv2.circle(f, frameCenter , 5, white, -1)
        cv2.circle(f, frameCenter , 3, red, -1)
        
        cv2.circle(f, contourCenter, 7, white, -1)
        cv2.circle(f, contourCenter, 5, black, -1)
        cv2.circle(f, contourCenter, 3, white, -1)
        
        cv2.line(f, frameCenter , contourCenter , red,2)
     
        dispString = "X: %d" % delta[0]
        cv2.putText(f, dispString, (0, 50), cv2.FONT_HERSHEY_PLAIN, 3.0, red ,3)
     
        dispString = "Y: %d" % delta[1]
        cv2.putText(f, dispString, (0, 100), cv2.FONT_HERSHEY_PLAIN, 3.0, red ,3)
        
        dispString = "D: %d" % distance
        cv2.putText(f, dispString, (0, 150), cv2.FONT_HERSHEY_PLAIN, 3.0, red ,3)
    
    cv2.imshow('TEST 11: Contour Circles',f)
    return delta

#####################################################################################
if __name__ == "__main__":
    
    
        
    c = cv2.VideoCapture(0)
    
    goodImage,frameOld = c.read()
    
    fourcc = cv2.cv.FOURCC('M', 'P', 'E', 'G')
    print fourcc
    outputVideo = cv2.VideoWriter('output.avi',fourcc ,fps=20,
                        frameSize = (640,480),
                        isColor=True)
    
    if not outputVideo.isOpened():
        print "Could not open file for writing"
        exit()
        
        
    cnc.init()
    cnc.setCoordRelative()
    lastMove = time.time()

    while(goodImage):
    
        goodImage,frame = c.read()
        if not goodImage:
            break
  
        # make the image look right as if we are facing the front of the shapeoko  
        frame = cv2.flip(frame,-1)   
        
        
        #some temporal averaging for frame11
        frameAvg = cv2.addWeighted(frame,.9,frameOld,.1,0)
        deltaPx = findSkittle(frameAvg)
        frameOld = frameAvg.copy()
        
        distanceToSkittlePx =     np.linalg.norm(deltaPx)
         
       
        now =  time.time()
        
        # move if we are too far away and havne't moved for a bit
        minError = 3 # pixels
        minTimeDelta = 1 #seconds
        if distanceToSkittlePx > minError and (( now - lastMove)> minTimeDelta):
                scalePxToMM = .05
                deltaMM = deltaPx * scalePxToMM 
                cnc.rapidmoveNoZ( (deltaMM[0] , -deltaMM[1]))
                lastMove = time.time()
                 
              
              
        outputVideo.write(frameAvg)
        
        # wait for a key press and see if we need to do anything
        key = cv2.waitKey(50) 
        if key == 27: # escape
            break
        
        #if key == 32: #space
            
                
    # program is done, clean up
    cv2.destroyAllWindows()
    c.release()
    outputVideo.release()

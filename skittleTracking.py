'''
Created on Jul 28, 2014

@author: kedwards
'''

import cv2
import numpy as np

def getthresholdedimg(hsv):
    
    # opencv hsv divids the 360 degrees of the color wheel by 2 to fit in 8 bits
    # http://www.hobbitsandhobos.com/wp-content/uploads/2011/06/colorWheel.png
    yellow = cv2.inRange(hsv,np.array((20,100,100)),np.array((30,255,255)))
    blue = cv2.inRange(hsv,np.array((100,100,100)),np.array((120,255,255)))
    green = cv2.inRange(hsv,np.array((45,50,50)),np.array((75,255,255)))
    both = cv2.add(yellow,blue)
    both = cv2.add(both,green)
    cv2.imshow('yellow',yellow)

    cv2.imshow('blue',blue)

    cv2.imshow('green', green)
    #cv2.imshow('both',both)

    return both

moviePath = r"trackTest.mp4"

c = cv2.VideoCapture(moviePath)

width,height = c.get(3),c.get(4)
print "frame width and height : ", width, height

# some code from
# https://github.com/abidrahmank/MyRoughWork/blob/master/roughnote/jay_abid_works/jay_abid_1.py
    
goodImage = True
while(goodImage):
    goodImage,f = c.read()
    if not goodImage:
        break; 

    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    
    
    he = cv2.equalizeHist(gray)
    
    blur2 = cv2.medianBlur(he,5)
    # gives a nice round edge on the skittle:
    #at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11 ,2 )
    
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,10)
    
    erosion_size = 1 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    cv2.imshow('adaptive threshold',dilate2)
    
    
    erode = cv2.erode(blur2,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    th3,otsu = cv2.threshold(dilate2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('otsu',otsu)
    #print 'Threshold is %d' % th3

    blur = cv2.medianBlur(f,5)
    
    
    both = getthresholdedimg(hsv)
    erode = cv2.erode(both,None)
    dilate = cv2.dilate(erode,None)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


    centers = []
    radii = []
    for contour in contours:
        area = cv2.contourArea(contour)

        # there is one contour that contains all others, filter it out
        if area <300:
            continue
    
        br = cv2.boundingRect(contour)
        radii.append(br[2])
    
        m = cv2.moments(contour)
        

        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        centers.append(center)
        
    print("There are {} circles".format(len(centers)))

    if len(radii) > 0:
        radius = int(np.average(radii)) + 5

        for center in centers:
            cv2.circle(f, center, 3, (255, 0, 0), -1)
            cv2.circle(f, center, radius, (0, 255, 0), 1)    

    cv2.imshow('img',f)

    if cv2.waitKey(25) == 27:
        break

cv2.destroyAllWindows()
c.release()

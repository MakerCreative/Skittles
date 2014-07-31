'''
Created on Jul 28, 2014

@author: kedwards
'''

import cv2
import numpy as np

def getthresholdedimg(hsv):
    yellow = cv2.inRange(hsv,np.array((20,100,100)),np.array((30,255,255)))
    blue = cv2.inRange(hsv,np.array((100,100,100)),np.array((120,255,255)))
    both = cv2.add(yellow,blue)
   # cv2.imshow('yellow',yellow)

    #cv2.imshow('blue',blue)

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
    #f = cv2.pyrDown(f)
    #f = cv2.flip(f,1)
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    #cv2.imshow('gray',gray)
    he = cv2.equalizeHist(gray)
    #cv2.imshow('Equalized histogram',he)
    blur2 = cv2.medianBlur(he,5)
    # gives a nice round edge on the skittle:
    #at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11 ,2 )
    
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,10)
    
    erosion_size = 1 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate = cv2.dilate(erode,kernel)
    cv2.imshow('adaptive threshold',dilate)
    
    th3,otsu = cv2.threshold(blur2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('otsu',otsu)
    #print 'Threshold is %d' % th3

    blur = cv2.medianBlur(f,5)
    
    
    both = getthresholdedimg(hsv)
    erode = cv2.erode(both,None)
    dilate = cv2.dilate(erode,None)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    '''for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2
        
        if 20 < hsv.item(cy,cx,0) < 30:
            cv2.rectangle(f,(x,y),(x+w,y+h),[0,255,255],2)
            print "yellow :", x,y,w,h
        elif 100 < hsv.item(cy,cx,0) < 120:
            cv2.rectangle(f,(x,y),(x+w,y+h),[255,0,0],2)
            print "blue :", x,y,w,h
'''
    cv2.imshow('img',f)

    if cv2.waitKey(25) == 27:
        break

cv2.destroyAllWindows()
c.release()

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
    return both

def getthresholdedimgk(hsv):
    
    # opencv hsv divids the 360 degrees of the color wheel by 2 to fit in 8 bits
    # http://www.hobbitsandhobos.com/wp-content/uploads/2011/06/colorWheel.png
    yellow = cv2.inRange(hsv,np.array((20,100,100)),np.array((30,255,255)))
    
    # moved the blue sv values up since theere is a blue reflection from LED off cutting board
    blue = cv2.inRange(hsv,np.array((100,50,150)),np.array((120,255,200)))
    green = cv2.inRange(hsv,np.array((45,50,50)),np.array((75,255,255)))
    both = cv2.add(yellow,blue)
    both = cv2.add(both,green)
    cv2.imshow('yellow',yellow)

    cv2.imshow('blue',blue)

    cv2.imshow('green', green)
    cv2.imshow('all', both)
    #cv2.imshow('both',both)

    return both
def test1 (frame):
    
    # this is from
    # https://github.com/abidrahmank/MyRoughWork/blob/master/roughnote/jay_abid_works/jay_abid_1.py
    blur = cv2.medianBlur(frame,5)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    both = getthresholdedimgk(hsv)
    erode = cv2.erode(both,None,iterations = 3)
    dilate = cv2.dilate(erode,None,iterations = 10)

    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        cx,cy = x+w/2, y+h/2
        
        if 20 < hsv.item(cy,cx,0) < 30:
            cv2.rectangle(frame,(x,y),(x+w,y+h),[0,255,255],2)
            print "yellow :", x,y,w,h
        elif 100 < hsv.item(cy,cx,0) < 120:
            cv2.rectangle(frame,(x,y),(x+w,y+h),[255,0,0],2)
            print "blue :", x,y,w,h

    cv2.imshow('TEST 1: img',frame)
    return

def test2(f):
    # test 2 had a lot of stuff got to be a mess, split into 3 and 4
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    
    
    he = cv2.equalizeHist(gray)
    
    #blur2 = cv2.medianBlur(he,5)
    blur2 = cv2.GaussianBlur(he,(5,5),0)
    # gives a nice round edge on the skittle:
    #at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11 ,2 )
    
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    cv2.imshow('TEST 2: adaptive threshold',at)
    
    
    # let's look for circles here
    
    
    
    erosion_size = 1 
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    cv2.imshow('TEST 2: adaptive threshold erode dialate',dilate2)
    
    
    erode = cv2.erode(blur2,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    th3,otsu = cv2.threshold(dilate2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('TEST 2: otsu',otsu)
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

    cv2.imshow('TEST 2: Contour Circles',f)
    return

def test3(f):

    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    
    
    he = cv2.equalizeHist(gray)
    
    blur2 = cv2.GaussianBlur(he,(5,5),0)
    
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    cv2.imshow('TEST 3: adaptive threshold',at)
    
    
    # let's look for circles here
    
    
    
    erosion_size = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    cv2.imshow('TEST 3: adaptive threshold erode dialate',dilate2)
    
    return

def test4(f):

    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

    
    
    he = cv2.equalizeHist(gray)
    
    #blur2 = cv2.medianBlur(he,5)
    blur2 = cv2.GaussianBlur(he,(5,5),0)
    
    erosion_size = 2
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    
    erode = cv2.erode(blur2,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    th3,otsu = cv2.threshold(dilate2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('TEST 4: otsu',otsu)
    #print 'Threshold is %d' % th3


    
    
    return


def test5(f):
    blur = cv2.medianBlur(f,5)
    
    hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)

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

    cv2.imshow('TEST 5: Contour Circles',f)

    return

def test6(f):
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    he = cv2.equalizeHist(gray)
    blur2 = cv2.GaussianBlur(he,(5,5),100)
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    erosion_size = 2
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate = cv2.dilate(erode,kernel)
    cv2.imshow('TEST 6: adaptive threshold erode dialate',dilate)
    
    # let's look for circles here
    contours,hierarchy = cv2.findContours(dilate,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)


    centers = []
    radii = []
    for contour in contours:
        area = cv2.contourArea(contour)

        # there is one contour that contains all others, filter it out
        if area < 1:
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

    cv2.imshow('TEST 6: Contour Circles',f)
    

    return


def test7(f):
    # help starting from (via google)
    # https://github.com/abidrahmank/OpenCV2-Python/blob/master/Official_Tutorial_Python_Codes/3_imgproc/houghcircles.py
    
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    he = cv2.equalizeHist(gray)
    blur2 = cv2.GaussianBlur(he,(5,5),100)
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    # let's look for circles here
    img = cv2.medianBlur(at,5)
    circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=100,param2=30,minRadius=100,maxRadius=300)
    
    if circles is None or 0 == len(circles):
        return
    
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        cv2.circle(f,(i[0],i[1]),i[2],(0,255,0),1)  # draw the outer circle
        cv2.circle(f,(i[0],i[1]),2,(0,0,255),3)     # draw the center of the circle    
    
    cv2.imshow('TEST 7: Hough Circles',f)
    

    return

if __name__ == "__main__":
    
    moviePath = r"trackTest.mp4"
    moviePath = r"trackTestCuttingBoard4cmabove.mp4"
    
    c = cv2.VideoCapture(moviePath)
    
    
    # some code from
        
    goodImage = True
    while(goodImage):
        goodImage,frame = c.read()
        if not goodImage:
            break; 
       
        cv2.imshow("ORIGINA MAFAKA", frame)   
        #frame1 = frame.copy()
        #test1(frame1)
        
        #frame2 = frame.copy()
        #test2(frame2)
        
        #frame3 = frame.copy()
        #test3(frame3)
        
        #otsu thresholding
        #frame4 = frame.copy()
        #test4(frame4)
        
        # contours
        #frame5 = frame.copy()
        #test5(frame5)
        
        # contours from adaptive thresholding , 3 and 5 combined
        #frame6 = frame.copy()
        #test6(frame6)
        
        # hough trasnform
        frame7 = frame.copy()
        test7(frame7)
        
        if cv2.waitKey(25) == 27:
            break
    
    cv2.destroyAllWindows()
    c.release()

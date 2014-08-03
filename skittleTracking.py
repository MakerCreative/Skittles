'''
Created on Jul 28, 2014

@author: kedwards
'''

import cv2
import numpy as np

tCanny1 = 50
tCanny2 = 60
tFrameNo = 100
tApSize = 5
tBlurSigma = 20

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

  
    
def test8(f):
    
    global tCanny1
    global tCanny2
    global tApSize
    global tBlurSigma
    
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
    
    
    cv2.imshow('TEST 8: Gray',gray)
    eh = cv2.equalizeHist(gray)
    cv2.imshow('TEST 8: eh',eh)
    
    print '\t %d' % tApSize
    edges = cv2.Canny(eh,tCanny1,tCanny2,tApSize)
    
    cv2.imshow('TEST 8: Basic Canny',edges)
    return

def trackChange(v):
    
    global tCanny1
    global tCanny2
    global tFrameNo
    global tApSize
    global tBlurSigma
    
    tCanny1 = cv2.getTrackbarPos('Canny1','Trackbars')
    tCanny2 = cv2.getTrackbarPos('Canny2','Trackbars')
    tFrameNo = int(cv2.getTrackbarPos('FrameNo','Trackbars'))
    tApSize = cv2.getTrackbarPos('ApSize','Trackbars')
    
    if tApSize % 2 == 0:
        tApSize = tApSize + 1 
    tBlurSigma = cv2.getTrackbarPos('BlurSigma','Trackbars')
    
    
    return

def test9(frame, tr, tg, tb):


    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #gray = cv2.equalizeHist(gray)

    #grayt = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    
    cv2.imshow("TEST9: input",frame)
    rr = cv2.matchTemplate(frame, tr, cv2.TM_CCOEFF_NORMED)
    rg = cv2.matchTemplate(frame, tg, cv2.TM_CCOEFF_NORMED)
    rb = cv2.matchTemplate(frame, tb, cv2.TM_CCOEFF_NORMED)

    res = cv2.add(rr,rg)
    res = cv2.add(res,rb)
    
    cv2.imshow("TEST9: result" , res)
    return

def test10(frame):
    # http://swarminglogic.com/article/2013_11_skittles
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    #s = cv2.equalizeHist(s)
    blur = cv2.GaussianBlur(s,(21,21),15)
    res = cv2.adaptiveThreshold(blur,100,cv2.ADAPTIVE_THRESH_MEAN_C , cv2.THRESH_BINARY_INV,7,2)
    cv2.imshow("test10 input",frame)
    cv2.imshow("test10 result",res)

def test11(f):
    # test 11 is a breakoff of test 2, which has the best borders around the skittles.
    
    gray = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
   # hsv = cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    he = cv2.equalizeHist(gray)
    
 
    blur2 = cv2.GaussianBlur(he,(5,5),0)
    # gives a nice round edge on the skittle:
    #at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11 ,2 )
    
    at = cv2.adaptiveThreshold(blur2,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,15 ,4)
    
    #cv2.imshow('TEST 11: adaptive threshold',at)
    
    
    # let's look for circles here
    
    
    
    erosion_size = 5
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(erosion_size,erosion_size))
    erode = cv2.erode(at,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    cv2.imshow('TEST 11: adaptive threshold erode dialate',dilate2)
    
    #at_open = cv2.morphologyEx(at, cv2.MORPH_OPEN, kernel)
    at_close = cv2.morphologyEx(at, cv2.MORPH_CLOSE, kernel)
    
    #cv2.imshow('TEST 11: at_open',at_open)
    cv2.imshow('TEST 11: at_close',at_close)
    
    '''
    erode = cv2.erode(blur2,kernel)
    dilate2 = cv2.dilate(erode,kernel)
    th3,otsu = cv2.threshold(dilate2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('TEST 11: otsu',otsu)
    #print 'Threshold is %d' % th3
    '''

    
   

    contours,hierarchy = cv2.findContours(at_close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    

    centers = []
    radii = []
    #print "there are %d contours" % len(contours)
    maxArea = 0
    maxC = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > maxArea:
            maxArea = area
            maxC = contour
            
            '''
        # there is one contour that contains all others, filter it out
        if area <300:
            continue
    
        br = cv2.boundingRect(contour)
        radii.append(br[2])
    
        m = cv2.moments(contour)
        

        center = (int(m['m10'] / m['m00']), int(m['m01'] / m['m00']))
        centers.append(center)
    '''
    # at the end we've found a maximum contour
    # TODO average frames from the camera - take a temporal average of N frames
    
    # find the smallest circle that encloses that maximum contour
    # let's hope it's a skittle!
    c,r = cv2.minEnclosingCircle(maxC)
    cv2.drawContours(f,maxC, -1,(255,255,255),-1)
    
    red = (0   , 0, 255)    
    green = (0, 255, 0)
    blue = (255, 0 , 0 )
    # draw a circle where we found the center of the skittles
    cv2.circle(f, (int(c[0]),int(c[1])), 5, green, -1)
    
    # find the center of the image and draw a circle there
    frameSize = f.shape
    img_c_y = frameSize[0] / 2 
    img_c_x = frameSize[1] / 2
    cv2.circle(f, (int(img_c_x),int(img_c_y)), 5, red, -1)
    
    # using a function attribute for a persistent variable
    # trying to use a weighted average of the center of the skittle to filter it
    weight = 0.3
    test11.centerx = int(test11.centerx * weight + c[0]*(1.0-weight))
    test11.centery = int(test11.centery * weight + c[1]*(1.0-weight))
    #cv2.circle(f, (test11.centerx , test11.centery), 10, red, -1)

    # draw a line between the center of the image and the center of the skittle
    cv2.line(f, (int(img_c_x),int(img_c_y)) , (int(c[0]),int(c[1])), red,2)
 
    cv2.imshow('TEST 11: Contour Circles',f)
    return

#####################################################################################
if __name__ == "__main__":
    global tCanny1
    global tCanny2
    global tFrameNo
    global tApSize
    global tBlurSigma
    
    moviePath = r"trackTest.mp4"
    moviePath = r"trackTestCuttingBoard4cmabove.mp4"
    
    c = cv2.VideoCapture(0)
    
    numFrames = int(c.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    
    '''
    cv2.namedWindow('Trackbars',cv2.WINDOW_NORMAL)
    cv2.cv.CreateTrackbar( 'Canny1', 'Trackbars',tCanny1, 100, trackChange)
    cv2.cv.CreateTrackbar( 'Canny2', 'Trackbars',tCanny2, 100, trackChange)
    cv2.cv.CreateTrackbar('FrameNo', 'Trackbars',tFrameNo, numFrames, trackChange)
    cv2.cv.CreateTrackbar( 'ApSize', 'Trackbars',tApSize, 50, trackChange)
    cv2.cv.CreateTrackbar( 'BlurSigma', 'Trackbars',tBlurSigma, 100, trackChange)
'''
    
        
    goodImage = True
    
    # for test9
    #r = cv2.imread('tr.png')
    #g = cv2.imread('tg.png')
    #b = cv2.imread('tb.png')
    goodImage,frame11_old = c.read()
    test11.centerx = 1.0
    test11.centery = 1.0
    while(goodImage):
        #print tFrameNo
        #c.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, frameNumber+20)
        #c.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,tFrameNo)
        goodImage,frame = c.read()
        
        # hit the end of the file
        if not goodImage:
            #c.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,0)
            #goodImage,frame = c.read()
            #continue
            break
       
        #cv2.imshow("ORIGNAL MAFAKA", frame)   
        
        # looking for colours in hsv and then contours
        #frame1 = frame.copy()
        #test1(frame1)
        
        # many threshold types together - a mess
        # however the current settings in this provide
        # a very good outline of each skittle colour
        #frame2 = frame.copy()
        #test2(frame2)
        
        #split from test 2
        # adaptive threshold
        # same good outline in the middle
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
        #frame7 = frame.copy()
        #test7(frame7)
        
        # basic canny edge to see what we get
        #frame8 = frame.copy()
        #test8(frame8)
        
        # let's try template matching
        #frame9 = frame.copy()
        #test9(frame9,r,g,b)
        
        # http://swarminglogic.com/article/2013_11_skittles
        #frame10 = frame.copy()
        #test10(frame10)
        
        # starting again from where test2 left off, it worked well
        # finding the skittle edges
        frame11 = frame.copy()
        
        #some temporal averaging for frame11
        frame11avg = cv2.addWeighted(frame11,.9,frame11_old,.1,0)
        test11(frame11avg)
        frame11_old = frame11avg.copy()
        
        key = cv2.waitKey(50) 
        if key == 27:
            break
        if key == 32:
            tFrameNo = tFrameNo + 1     
            cv2.setTrackbarPos('FrameNo','Trackbars',tFrameNo)

        
    
    cv2.destroyAllWindows()
    c.release()

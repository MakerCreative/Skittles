import serial
import cnc
import skittleTracking
import cv2
# all measurements in mm

# hole centers were 15 mm appart when drilled
pixelWidth = 12 # radius of a skittle [mm]
pixelSpace = 3  # spacing between skittles [mm]

global numPickUpSpots 
global curPickUpSpot 

numPickUpSpots = 16  
curPickUpSpot  = 0  

# mm from camera to picker need to subtract thsi from where we want the picker to go
cameraPickerOffset = (-10 , -2)


numRows = 15 # take from image
numCols = 15 # take from image
def getPickupLocation():
    global curPickUpSpot

    pickupY = 0 # by defn
    
    pickupX = 0 + (pixelWidth+pixelSpace)*curPickUpSpot
    curPickUpSpot = (curPickUpSpot + 1) % numPickUpSpots 
    return pickupX,pickupY

def getDropLocation(row_i,col_i):
    dropX = 0
    dropY = 0 

    xOffset = 0 
    yOffset = 30  

    dropX = xOffset + row_i * (pixelWidth + pixelSpace )  
    #dropY = yOffset + (col_i%3) * (pixelWidth + pixelSpace )  
    dropY = yOffset + 1 * (pixelWidth + pixelSpace )
    
    
    return dropX, dropY
    


def gotoLocation(dropX, dropY):
    cnc.rapidmove((dropX,dropY))
    return

def dropSkittle():
    cnc.spindleOff()
    return

def pickupSkittle():
    cnc.spindleOn()
    return

def connectToShapeoko():
    serialObject = serial.Serial(0)
    print serialObject.name

    return serialObject

def disconnectFromShapeoko(ser):
    ser.close()


def defgetColourIndex():
	return

def getReducedImage( colourIndex, inputImage):
	return




# some python snipits
# note "" is the start and end of multiline comments in python
"""
def getImageData(filename):
  [snip]
  return size, (format, version, compression), (width,height)
size, type, dimensions = getImageData(x)


http://pyserial.sourceforge.net/shortintro.html


"""



#shapeoko = connectToShapeoko()
cnc.init()
cnc.spindleOff()

skittleTracking.init()

#for row_i in range(0, numRows-1):
row_i = 0
while row_i < numPickUpSpots:
    #for col_i in range(0, numCols - 1):

    #comment out for now, just one pickup (0,0) and move put into grid from there
    #pixelColour = getPixelColour( reducedImage, row_i, col_i)
    
    pickUpX , pickUpY = getPickupLocation( )
    
   
    #cnc.rapidmoveNoZ( ( pickUpX- cameraPickerOffset[0], pickUpY- cameraPickerOffset[1] ))
    cnc.rapidmoveNoZ( ( pickUpX, pickUpY ))
    
    distanceToSkittle = 10
    
    cnc.setCoordRelative()
    skittleTracking.getFrame()
    skittleTracking.getFrame()
    while distanceToSkittle > 3:
        skittleTracking.getFrame()

        deltaPx = skittleTracking.findSkittle(skittleTracking.frameAvg)
        distanceToSkittle = skittleTracking.moveToSkittle(deltaPx)
        cv2.imshow('SKITTLE', skittleTracking.frameAvg)
        cv2.waitKey(50)
    # move over for camera - picker difference    
    cnc.rapidmoveNoZ(cameraPickerOffset)
    cnc.setCoordAbsolute()
    
    cnc.relMoveZ(-20)
    pickupSkittle()
    cnc.relMoveZ(20)

    dropX, dropY = getDropLocation( row_i, row_i )

    cnc.rapidmoveNoZ( ( dropX + cameraPickerOffset[0], dropY+ cameraPickerOffset[1] ))
    #cnc.setCoordRelative()
    #cnc.rapidmove((-11,-3))
    #cnc.setCoordAbsolute()

    cnc.relMoveZ(-20)
    dropSkittle()
    cnc.relMoveZ(20)

    row_i = row_i + 1

#cnc.rapidmoveNoZ( ( 0,0 ))

import serial
import cnc
import skittleTracking

# all measurements in mm

# hole centers were 15 mm appart when drilled
pixelWidth = 12 # radius of a skittle [mm]
pixelSpace = 3  # spacing between skittles [mm]

global numPickUpSpots 
global curPickUpSpot 

numPickUpSpots = 5  
curPickUpSpot  = 0  

#global skittleHeight
#skittleHeight = 7 # height of a skittle relative to origin

# where are we going to zero the picker head?
# let's have the X's be the pickup spots for each colour skittle
# they should each just have their own coordinates for fine tuning
# note these will have to have 3 coordinates, could pick and place on different levels.

# Z is an arbitrary zero spot

#**************************************************
#*   Z
#*
#*      X      X      X      X       X       X
#*
#*
#*
#*             ----------------------
#*             |                    |
#*             |                    |
#*             |                    |
#*             |                    |
#*             |                    |
#*             |                    |
#*             |                    |
#*             |                    |
#*             ----------------------
#*
#*
#*
#*
#***************************************************


# *************** this can be done offline

# get the set of colours we can use for this piece
#colourIndex = getColourIndex()

# get a 2d grid of pixels from our input image using our colour index
# might be able to do this with PIL or Pillow
#reducedImage = getReducedImage( colourIndex, inputImage)

# *************** end this can be done offline

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
    dropY = yOffset + col_i * (pixelWidth + pixelSpace )  
    
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
while row_i < 5:
    #for col_i in range(0, numCols - 1):

    #comment out for now, just one pickup (0,0) and move put into grid from there
    #pixelColour = getPixelColour( reducedImage, row_i, col_i)
    
    pickUpX , pickUpY = getPickupLocation( )
    
    gotoLocation(pickUpX , pickUpY)

    distanceToSkittle = 10
    
    cnc.setCoordRelative()
    while distanceToSkittle > 3:
        skittleTracking.getFrame()

        deltaPx = skittleTracking.findSkittle(skittleTracking.frameAvg)
       
        distanceToSkittle = skittleTracking.moveToSkittle(deltaPx)
        
    # move over for camera - picker difference    
    cnc.rapidmove((-11,-3))
    cnc.setCoordAbsolute()
        
    pickupSkittle()

    dropX, dropY = getDropLocation( row_i, row_i )

    gotoLocation(dropX, dropY)
    cnc.setCoordRelative()
    cnc.rapidmove((-11,-3))
    cnc.setCoordAbsolute()


    dropSkittle()
    row_i = row_i + 1


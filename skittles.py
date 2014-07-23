import serial
import cnc

# all measurements in mm

pixelWidth = 10 # radius of a skittle [mm]
pixelSpace =  7 # spacing between skittles [mm]

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
colourIndex = getColourIndex()

# get a 2d grid of pixels from our input image using our colour index
# might be able to do this with PIL or Pillow
reducedImage = getReducedImage( colourIndex, inputImage)

# *************** end this can be done offline

numRows = 4; # take from image
numCols = 4; # take from image

#shapeoko = connectToShapeoko()
cnc.init()

for row_i in range(0, numRows-1):
	for col_i in range(0, numCols - 1):

        #comment out for now, just one pickup (0,0) and move put into grid from there
		#pixelColour = getPixelColour( reducedImage, row_i, col_i)
	
		pickUpX , pickUpY = getPickupLocation( )
        pickUpX = 0 ; 
        pickUpY = 0 ; 
        pickUpZ = 0 ; 
		
        gotoLocation(pickUpX , pickUpY)

		pickupSkittle()

		dropX, dropY = getDropLocation( row_i, col_i )

		gotoLocation(dropX, dropY)

		dropSkittle()

def getDropLocation(row_i,col_i)
    dropX = 0;
    dropY = 0; 

    xOffset = 0 ;
    yOffset = 0 ; 

    dropX = xOffset + col_i * (pixelWidth + pixelSpace ) ; 
    dropY = yOffset + row_i * (pixelWidth + pixelSpace ) ; 
    
    return dropX, dropY
    


def gotoLocation(dropX, dropY)

    return

def dropSkittle()
    return

def pickupSkittle()
    return

def connectToShapeoko()
    serialObject = serial.Serial(0)
    print serialObject.name

    return serialObject

def disconnectFromShapeoko(ser)
    ser.close()


def defgetColourIndex()
	return

def getReducedImage( colourIndex, inputImage)
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


	



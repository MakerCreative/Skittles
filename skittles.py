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

numRows = 16; # take from image
numCols = 16; # take from image

for row_i in range(0, numRows-1):
	for col_i in range(0, numCols - 1):

		pixelColour = getPixelColour( reducedImage, row_i, col_i)
	
		pickUpX , pickUpY = getPickupLocation( pixelColour )

		gotoLocation(pickUpX , pickUpY)

		pickupSkittle()

		dropX, dropY = getDropLocation( row_i, col_i )

		gotoLocation(dropX, dropY)

		dropSkittle()



# some python snipits
# note "" is the start and end of multiline comments in python
""
def getImageData(filename):
  [snip]
  return size, (format, version, compression), (width,height)
size, type, dimensions = getImageData(x)


http://pyserial.sourceforge.net/shortintro.html


""


	



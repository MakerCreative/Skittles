# all measurements in mm

PixelWidth = # radius of a skittle
PixelSpace = # spacing between skittles

# where is zero going to be?

# *************** this can be done offline

# get the set of colours we can use for this piece
colourIndex = getColourIndex()

# get a 2d grid of pixels from our input image using our colour index
# might be able to do this with PIL or Pillow
reducedImage = getReducedImage( colourIndex, inputImage)

# *************** end this can be done offline


foreach row in image
   foreach column in image

	pixelColour = getPixelColour( reducedImage, row_i, col_i)
	
	pickUpX , pickUpY = getPickupLocation( pixelColour)

	gotoLocation(pickUpX , pickUpY)

	pickupSkittle()

	dropX, dropY = getDropLocation( row_i, col_i )

	gotoLocatoin(dropX, dropY)

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


	



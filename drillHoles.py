import serial
import time
import cnc


# let's drill a 16 x 16 grid of holes and then a 16 x 1 grid 2 rows above to pick from

cnc.init()

row = 0  
col = 0 

distance = 15  


x_offset = 0
#y_offset = 30 
y_offset = 0 


#while col < 16:
#	cnc.drill( (col*distance,0) ,2)
#	time.sleep(3)
#	col = col + 1
#

col = 0 
row = 0 
while row < 11:
	while col < 16:
		cnc.drill( (col*distance + x_offset , row*distance+y_offset), 2)
		time.sleep(3)
		col = col + 1
	col = 0 
	row = row + 1



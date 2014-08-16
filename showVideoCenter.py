'''
Created on Aug 15, 2014

@author: kedwards
'''
import skittleTracking
import cv2

if __name__ == "__main__":
    skittleTracking.init()    
    
    #fourcc = cv2.cv.FOURCC('M', 'P', 'E', 'G')
    #print fourcc
    #outputVideo = cv2.VideoWriter('output.avi',fourcc ,fps=20,
    #                   frameSize = (640,480),
    #                    isColor=True)
    
        
 


    while(True):
    
        skittleTracking.getFrame()

        deltaPx = skittleTracking.findSkittle(skittleTracking.frameAvg)
       
            
        # wait for a key press and see if we need to do anything
        key = cv2.waitKey(50) 
        if key == 27: # escape
            break
        
        #if key == 32: #space
            
                
    # program is done, clean up
    cv2.destroyAllWindows()
    skittleTracking.camera.release()

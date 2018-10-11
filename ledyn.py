# -*- coding: utf-8 -*-

   
def click_event(event, x, y, flags, param):
    '''
    get current mouse cordinates by left-clicking
    from http://www.acgeospatial.co.uk/interaction-opencv-python/
    '''
    if event == cv2.EVENT_LBUTTONDOWN:
        print ('X-coordinate:', x, ' Y-coordinate:', y)
        


def findNextPoint(sX, sY, sAngle, dist, thresholding, dAngleInc, limAngle, width, height):
    '''
    This function searches for black pixels at defined distances and if found return the position
    
    Input:
    
    sX - X coordinate of starting point
    sY - Y coordinate of starting point
    sAngle - Angle (in degree) to start searching 
    dist - distance (in pixels) at which search is being conducted    
    thresholding - Input image
    dAngleInc - angle increment (in degrees)
    limAngle - limit of search angle (in degrees)
    width - width of each frame (in px)
    height - height of each frame (in px)
        
    Output:
    
    fP - reports if black pixel is found (= 1)  
    eX - X coordinate of black pixel found
    eY - Y coordinate of black pixel found
    eAngle - angle at which the black pixel was found 
    l - absolute length to black pixel found
        
    '''
    i = 0
    dAngle = 0

    while dAngle <= limAngle and dAngle >= -limAngle :          #modify this for more/less accuracy 
        if i != 0 and i % 2 == 0 :
            dAngle = dAngle + dAngleInc
        #switch from negative to positive at each iteration:
        if i % 2 == 0 :
            absdAngle = -dAngle
        else :
            absdAngle = dAngle
        out = 0 #indicates wether the resulting vector is out of bounds (=1)        
        eAngleRad = (sAngle + absdAngle)* np.pi / 180  #convert to radiant
        #calculate (and round) the dist in px in x,Y direction:
        dX = np.sin(eAngleRad) * dist 
        dY = np.cos(eAngleRad) * dist
        dX = np.around(dX) #round x
        dY = np.around(dY) #round y
        
        l = np.sqrt(dX*dX + dY*dY)                  #calcluate the absolute l
        chkX = int(sX - dX)
        chkY = int(sY - dY)
        eAngle = eAngleRad * 180 / np.pi            #transform into degrees    
        #Check here if out of bounds:
        if chkX > width or chkX < 0:
            print ('chkX: ',chkX, ' Width: ', width, 'Out of bounds')
            out = 1
            break
        if chkY > height or chkX < 0:
            print ('chkY: ',chkY, ' Height: ', height, 'Out of bounds')
            out = 1
            break
        if out == 0:
            if thresholding[chkY, chkX] == 0:
                eX = chkX
                eY = chkY
                fP = 1
                return fP, eX, eY, eAngle, l
        fP = 0
        i = i + 1
    fP = 0
    eX = 0
    eY = 0
    eAngle = 0
    l = 0
    return fP, eX, eY, eAngle, l


def linesegmentation(startX, startY, startAngle, distance, deltaAngleInc, limitedAngle, distanceInc, maximumIter):
    '''

    '''    
    #Initial values (modify if needed, see documentation of findNextPoint.py for further details):
    sX = startX
    sY = startY
    sAngle = startAngle
    dist = distance # in Pixels        
    dAngleInc = deltaAngleInc
    limAngle = limitedAngle
    
   
    distInc = distanceInc
    maxIter = maximumIter        #will not work with 25 as out of bounds
#        
    
    
    x = [] #create an empty list where x values will be saved
    y = []
    
    #loop over one plant leaf
    while distInc <= maxIter:
        #print ('New starting point!')
        #print (distInc)
        fP, eX, eY, eAngle, l = findNextPoint(sX, sY, sAngle, dist, binary, dAngleInc, limAngle, width, height)
        
        if fP == 1:
            cv2.line(frame, (sX,sY),(eX,eY), (0,255,0), 2) #print line    
            sX = eX
            sY = eY
            sAngle = eAngle         
            x.append(sX)
            y.append(sY)
                
        if fP == 0:
            dist = dist + distInc               #here search further 
            distInc += 1 
        
        if distInc == maxIter:     #save data to container
            xCollector.append(x)
            yCollector.append(y)

    
    if showOrigTrack == 1:
        cv2.imshow('Original video with tracking',frame)
        cv2.setMouseCallback('Original video with tracking', click_event) #new left-click




def writeresults(xCollector, yCollector):
    '''
    write results to files: x.dat & y.dat. Each row is one frame
    '''    
    
    np.savetxt('x.tmp', xCollector, delimiter=",", fmt='%s')
    np.savetxt('y.tmp', yCollector, delimiter=",", fmt='%s')
    
    #do some formatting for nice Matlab readability:
    i = 0
    with open('x.tmp') as f:
        lines = f.readlines()
    
    
    while i < len(lines):
        #read line 1:
            s = lines[i]
            #truncate:
            s = s[1:-2]
            s += '\n'
            with open('x.dat','a') as g:          #this appends text
                g.write(s)
                i=i+1
                
    #replace brackets in Y
    i = 0

    with open('y.tmp') as f:
        lines = f.readlines()
    
    
    while i < len(lines):
        #read line 1:
            s = lines[i]
            #truncate:
            s = s[1:-2]
            s += '\n'
            with open('y.dat','a') as g:          #this appends text
                g.write(s)
                i=i+1
    
    #delete temporary files:
    os.remove('x.tmp')
    os.remove('y.tmp')

    print('Writing results complete')    




"""
LeDyn by Moritz Thom 2018

"""

import numpy as np
import cv2
import os

#Variables (modify if needed):
inVid = 'example-low-res.mp4' # Name of video file to be analysed
BINARY_Thresh = 145 # Sets the value for binary thresholding

#Variables for line-segmentation algorithm (modify if needed):
startX = 545
startY = 371
startAngle = 0
distance = 10 # in Pixels        
deltaAngleInc = 0.1
limitedAngle = 90
distanceInc = 0
maximumIter = 11        #will not work with 25 as out of bounds

# Display options(modify if needed):
showthresholdMov = 1 # Display thresholded binary video (optional)
showOrigTrack = 1 # Display original video with processed line segmentation visualized (optional) 

# Other variables (do not modify):
xCollector = []                                 #contains data from final segmentation
yCollector = []                                 #contains data from final segmentation 


cap = cv2.VideoCapture(inVid)

width = cap.get(3)              #width of video in pixel
height = cap.get(4)         #height of video in pixel
totalf = cap.get(cv2.CAP_PROP_FRAME_COUNT) #total number of frames


while(cap.isOpened()):  
    ret, frame = cap.read() # Capture frame-by-frame
    
    if ret: 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert to Grayscale
        ret,binary = cv2.threshold(gray, BINARY_Thresh, 250, cv2.THRESH_BINARY) #Convert to binary using the most simple threshold
        
        if showthresholdMov == 1:   # Display thresholded video if wanted
            cv2.imshow('Thresholded video',binary)
            cv2.setMouseCallback('Thresholded video', click_event) # Mouse button left-click to display coordinates
        
        linesegmentation(startX, startY, startAngle, distance, deltaAngleInc, limitedAngle, distanceInc, maximumIter) #Algorithm to do line sgmentation
              
    if cv2.waitKey(1) & 0xFF == ord('q'): # Quit by hitting 'q' in movie
        break

writeresults(xCollector, yCollector) # Write results to files: x.dat & y.dat


cap.release() # When everything is done release the capture
cv2.destroyAllWindows()




        


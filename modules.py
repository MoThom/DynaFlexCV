# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 15:50:36 2018

@author: Moritz Thom
"""




def segmentation(nameOfVid='example.mp4', thresh=140, percent=50):
    
    ''' 
    Segmentation module 
    
    quit by hitting 'q' in movie
    
    Input arguments:
        nameOfVid = name of the video in ""
        thresh = is the threshold to convert video in binary
        percent= determines window size in percent
    '''
    
    #import numpy as np
    import cv2
    #import os
    #import time
    
    #nameOfVid = 'WL400_064-low-res.mp4'            #this works
    #nameOfVid = 'example.mp4'                          #name of video to be analysed
    
    
    ''' Sets modified dimensions for videoframe '''
    def rescale_frame(frame,percent=75):         #from:https://www.youtube.com/watch?v=y76C3P20rwc
        scale_percent = percent
        width=int(frame.shape[1]*scale_percent/100)
        height=int(frame.shape[0]*scale_percent/100)               
        dim = (width,height)
        return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    
    cap = cv2.VideoCapture(nameOfVid)           #load video
    
    ''' Display some basic properties of the movie '''
    width = cap.get(3)
    height = cap.get(4)
    totalf = cap.get(cv2.CAP_PROP_FRAME_COUNT)  #total number of frames
    print ('Name of video to be analysed: ', nameOfVid)
    print ('Width: ', width, 'pixel')
    print ('Height: ', height, 'pixel')
    print ('Total number of frames: ', totalf)
    
    
    while(cap.isOpened()):  # check !
        ret, frame = cap.read()                     # capture frame-by-frame
        if ret: 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                                #Convert to Grayscale
            ret,simpleThreshold = cv2.threshold(gray, thresh, 250, cv2.THRESH_BINARY)        #Simple threshold
            simpleThreshold=rescale_frame(simpleThreshold, percent )                  #rescale frame
            cv2.imshow('Thresholding Method used',simpleThreshold)                        #open thresholded video in new window
        if cv2.waitKey(1) & 0xFF == ord('q'):    #quit by hitting 'q' in movie
            break
            
    # When everything is done release the capture
    cap.release()
    cv2.destroyAllWindows()        
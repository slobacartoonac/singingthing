#!/usr/bin/python
from Tkinter import *
import threading
import Queue
import tkMessageBox
import numpy as np
#from multiprocessing import Process, Queue
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk
import ttk
import singleton


settingsCon = singleton.settings()
fgbg = cv2.createBackgroundSubtractorMOG2(10, 50, 0)
"""
Parameters
history	Length of the history.
varThreshold	Threshold on the squared Mahalanobis distance between the pixel and the model to decide whether a pixel is well described by the background model.
                This parameter does not affect the background update.
detectShadows	If true, the algorithm will detect shadows and mark them. It decreases the speed a bit, so if you do not need this feature, set the parameter to false.
"""

def bgSubtraction(input, v, debug):
        
        try:
                fgmask = fgbg.apply(input)
                #image = cv2.GaussianBlur(fgmask,(5,5),3)
                image=cv2.dilate(fgmask, None, 10)
                image=cv2.erode(image, None, 10)
                _, cnts, _ = cv2.findContours(image.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)#cv2.RETR_EXTERNAL
                max_area = 200
                minv=(0,0)
                for c in cnts:
                # if the contour is too small, ignore it
                        if settingsCon['minArea'].get()<cv2.contourArea(c)<settingsCon['maxArea'].get():                                 
                                # compute the bounding box for the contour, draw it on the frame,
                                # and update the text
                                
                                (x, y, w, h) = cv2.boundingRect(c)
                                cv2.rectangle(input, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                cv2.circle(input,(x + w/2, y + h/2),10,(0, 0, 255),-1)
                                if y+h>minv[1]:
                                        minv=(x + w/2, y + h)

                if debug==1:
                        cv2.imshow('Mask', fgmask)
                return (input,minv)
                
        except:
                print 'Image grab failed.'
                return ('',(0,0))

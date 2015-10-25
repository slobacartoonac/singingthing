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

def manualDetect(input, bgrnd, debug):
        if bgrnd == None:
                return (input,(0,0))
                
        else:
                try:
                        image = input#cv2.GaussianBlur(input,(5,5),3)#3
                        maiorArea = 0
                        mask = cv2.absdiff(image,bgrnd)
                        gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
                        _, gray = cv2.threshold(gray, 50,255,cv2.THRESH_BINARY)

                        gray=cv2.dilate(gray, None, 3)#Opening is just another name of erosion followed by dilation.
                        #It is useful in removing noise, as we explained above. Here we use the function
                        gray=cv2.erode(gray, None, 3)#Closing is reverse of Opening, Dilation followed by Erosion.
                        #It is useful in closing small holes inside the foreground objects, or small black points on the object.
                        gray=cv2.dilate(gray, None, 3)#ovo je dodato nije sigurno da je dobro
                        _, cnts, _ = cv2.findContours(gray.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                        minv=(0,0)
                        for c in cnts:
                                # if the contour is too small, ignore it
                                if settingsCon['minArea'].get()<cv2.contourArea(c)<settingsCon['maxArea'].get():#<5000:
                                    #continue

                                    # compute the bounding box for the contour, draw it on the frame,
                                    # and update the text
                                    (x, y, w, h) = cv2.boundingRect(c)
                                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                    cv2.circle(image,(x + w/2, y + h/2),2,(0, 0, 255),-1)
                                    if y+h>minv[1]:
                                        minv=(x + w/2, y + h)
                        #cv2.imshow('im', image)
                        if debug==1:
                                cv2.imshow('Gray', gray)
                                cv2.imshow('Mask',mask)
                        return (image,minv)
                except:
                        #print 'Image grab failed'
                        return ('',(0,0))


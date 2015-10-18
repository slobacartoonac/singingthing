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

hog = cv2.HOGDescriptor()
hog.setSVMDetector( cv2.HOGDescriptor_getDefaultPeopleDetector() )

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh

def draw_detections(img, rects, thickness = 1):
    minv=(0,0)
    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15*w), int(0.05*h)
        cv2.rectangle(img, (x+pad_w, y+pad_h), (x+w-pad_w, y+h-pad_h), (0, 255, 0), thickness)
        cv2.circle(img,(x + w/2, y + h/2),10,(0, 0, 255),-1)
        if y+h>minv[1]:
               minv=(x + w/2, y + h)
    return minv

def hogDetect(input, v, debug):
        
        try:
                img=input
                minv=(0,0) 
                found, w = hog.detectMultiScale(img, winStride=(8,8), padding=(32,32), scale=1.05)
                found_filtered = []
                for ri, r in enumerate(found):
                    for qi, q in enumerate(found):
                        if ri != qi and inside(r, q):
                            break
                    else:
                        found_filtered.append(r)
                draw_detections(img, found)
                minv=draw_detections(img, found_filtered, 3)
                print '%d (%d) found' % (len(found_filtered), len(found))
                input = img
                return (input,minv)
           
        
        except:
            print 'loading error'
            return ('',(0,0))

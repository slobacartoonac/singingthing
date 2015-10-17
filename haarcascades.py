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

classifier1='haarcascade_fullbody.xml'
classifier2='haarcascade_frontalcatface_extended.xml'
cascadeClassifier1 = cv2.CascadeClassifier(classifier1)
cascadeClassifier2 = cv2.CascadeClassifier(classifier2)

def haarcascades(input, v, debug):
    
    print 'haarcascades'
    # Create the haar cascade
    print 'classifier'
    try:
        # Read the image
       
        #image = cv2.imread(imagePath)
        gray = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)

        print 'bgr to gray'
        # Detect faces in the image
        if v==1:
            classifier=cascadeClassifier1
        else:
            classifier=cascadeClassifier2
        detects = classifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )
        print 'detects'

        print "Found {0} faces!".format(len(detects))

        # Draw a rectangle around the faces
        for (x, y, w, h) in detects:
            cv2.rectangle(input, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.circle(input,(x + w/2, y + h/2),10,(0, 0, 255),-1)
        print 'rect drawn'
        #cv2.imshow("Faces found", image)
       
        if debug==1:
                cv2.imshow('Gray', gray)
        return input
    except:
            print 'Image grab failed.'

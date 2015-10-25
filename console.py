#!/usr/bin/python
#from Tkinter import *
import threading
import Queue
import tkMessageBox
import numpy as np
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
#import Tkinter as tk
import ttk
import settingsWindow
import hogDetect
import haarcascades
import bgSubtraction
import manualDetect
import sys
sys.path.append("sound")
import play_move
import projection
import singleton
import math

background=None

var1=None

class IntVar:
    def __init__(self):
        self.val=0
    def set(self,v):
        self.val=float(v)
    def get(self):
        return self.val
class StringVar:
    def __init__(self):
        self.val=""
    def set(self,v):
        self.val=v
    def get(self):
        return self.val

def setValues():
       try:
           f=open("settings.txt")
           settings=f.readlines()
           f.close()
           settingsCon['minArea'].set(settings[5][:-1])
           settingsCon['maxArea'].set(settings[6][:-1])
           settingsCon['bgHistory'].set(settings[7][:-1])
           settingsCon['bgTresh'].set(settings[8][:-1])
           settingsCon['minSpeed'].set(settings[9][:-1])
           settingsCon['maxSpeed'].set(settings[10][:-1])
           settingsCon['minFreq'].set(settings[11][:-1])
           settingsCon['maxFreq'].set(settings[11][:-1])
           settingsCon['audioRate'].set(settings[13][:-1])
           settingsCon['positionBuff'].set(settings[14][:-1])
           #newdata.set(settings[15][:-1])
           print 'settings loaded'
       except:   
           var1.set('2')
           print 'default values set'





def camProperties():

        try:
                f=open("settings.txt")
                print 'file opened'
                var=f.readlines()
                print 'lines read'
                x=float((var[0][:-1]))
                print 'var added'
                y=float((var[1][:-1]))
                hc=float((var[2][:-1]))
                dc=float((var[3][:-1]))
                print 'close'
                f.close()
                prmsg = (x*math.pi/180, y*math.pi/180, hc, dc)
                print prmsg
                return (x*math.pi/180, y*math.pi/180, hc, dc)

        except:
                print sys.exc_info()[0]
                return (3.14/4, 3.14/5, 10, 10)

def showFreq(fff):
    if fff!=None:
                        tf='Frequency is: %d'%int(fff[2])
                        txy='Coordinates of object are: %.2f and %.2f'%(fff[0],fff[1])
                        settingsCon['freq'].set(tf)
                        settingsCon['xy'].set(txy)
def quit_():
   cv2.destroyAllWindows()
   play_move.end()

def getProcMet(var, input):
        v = var.get()
        settingsCon = singleton.settings()
        settPlay=(float(settingsCon['minSpeed'].get()),float(settingsCon['maxSpeed'].get()),
                  float(settingsCon['minFreq'].get()),float(settingsCon['maxFreq'].get()),
                  float(settingsCon['audioRate'].get()),float(settingsCon['positionBuff'].get()),settingsCon['mute'].get())
        global background
        if v == 1:
                 #print "m1"
                 if background==None:
                        background = input
                 output=manualDetect.manualDetect(input, background, int(settingsCon['debug'].get()))
                 fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                 showFreq(fff)
                 return output[0]
        elif v == 2:
                if background!=None:
                        background = None
                #print "m2"
                output=bgSubtraction.bgSubtraction(input, (), int(settingsCon['debug'].get()))
                #print "bilopre"
                #print "calling ", output[1]
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                #print fff
                showFreq(fff)

                return output[0]

        elif v == 3:
                #print "m3"
                output=haarcascades.haarcascades(input, 1, int(settingsCon['debug'].get()))
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                showFreq(fff)
                return output[0]
                
        else:
                if background!=None:
                        background = None
                #print "m0"
                output=hogDetect.hogDetect(input, (), ())
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                showFreq(fff)
                return output[0]

def getVideoSize(source):
        vidFile = cv2.VideoCapture(source)
        vidFile.set(3, 640)     #horizontal pixels
        vidFile.set(4, 480)		#vertical pixels
        for x in range(0,5):
                try:
                        flag, frame=vidFile.read()
                        (h,w,c)= frame.shape
                        return h,w
                except:
                        print 'Can not get size of video'
        vidFile.release()


settingsCon = singleton.settings()


if __name__ == '__main__':
   args=sys.argv     
   settingsCon = singleton.settings()
   
   source =  0#"final2.avi"

   h, w = getVideoSize(source)
   camSet=camProperties()
   settingsCon['ccam']=projection.cammera(w,h,camSet[0],camSet[1])
   settingsCon['ccam'].set_position(camSet[2], camSet[3])
   videoSize = 'Video size: %d x %d'%(w,h)
   print videoSize

   queue = Queue.Queue(maxsize=5)
   global var1
   var1 = IntVar()
   var1.set('2')
   
   settingsCon['mute'] = IntVar()
   settingsCon['minArea'] = IntVar()
   settingsCon['maxArea'] = IntVar()
   settingsCon['bgHistory'] = IntVar()
   settingsCon['bgTresh'] = IntVar()
   settingsCon['freq'] = StringVar()
   settingsCon['xy'] = StringVar()
   settingsCon['minArea'].set('300')
   settingsCon['maxArea'].set('5000')
   settingsCon['bgHistory'].set('10')
   settingsCon['bgTresh'].set('50')
   settingsCon['bgHistoryOld']=-1
   settingsCon['bgTreshOld']=-1
   settingsCon['minSpeed'] = IntVar()
   settingsCon['maxSpeed'] = IntVar()
   settingsCon['minFreq'] = IntVar()
   settingsCon['maxFreq'] = IntVar()
   settingsCon['minSpeed'].set('1')
   settingsCon['maxSpeed'].set('10')
   settingsCon['minFreq'].set('100')
   settingsCon['maxFreq'].set('500')
   settingsCon['audioRate'] = IntVar()
   settingsCon['positionBuff'] = IntVar()
   settingsCon['audioRate'].set('10')
   settingsCon['positionBuff'].set('5')
   settingsCon['newdata']=IntVar()
   settingsCon['newdata'].set('1')
   settingsCon['debug']=IntVar()
   settingsCon['debug'].set('0')
   if(len(args)==12):
           var1.set(args[1])
           settingsCon['minArea'].set(args[2])
           settingsCon['maxArea'].set(args[3])
           settingsCon['bgHistory'].set(args[4])
           settingsCon['bgTresh'].set(args[5])
           settingsCon['minSpeed'].set(args[6])
           settingsCon['maxSpeed'].set(args[7])
           settingsCon['minFreq'].set(args[8])
           settingsCon['maxFreq'].set(args[9])
           settingsCon['audioRate'].set(args[10])
           settingsCon['positionBuff'].set(args[11])

   
   print settingsCon['minArea']
   print settingsCon['maxArea']
   print settingsCon['bgHistory']
   print settingsCon['bgTresh']

   vidFile = cv2.VideoCapture(source)
   vidFile.set(3, 640)     #horizontal pixels
   vidFile.set(4,480)		#vertical pixels

   flag, frame=vidFile.read()
   cv2.imshow("done",frame)
   while vidFile.isOpened():
             e=0
             
             if settingsCon['newdata'].get():
                     flag, frame=vidFile.read()
             frame=getProcMet(var1,frame)
             try:
                             cv2.putText(frame,settingsCon['freq'].get(), (10,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                             cv2.putText(frame,settingsCon['xy'].get(), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                             cv2.putText(frame,"mode "+str(var1.get()), (10,75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 255)
                             cv2.imshow("done",frame)
             except:
                             e=1
             #print "pokazi"
             k=cv2.waitKey(7)
             if k!=-1:
                     print k
             if  k % 0x100 == 27:
                 break
             if k==ord('q'):
                     
                     v=int(var1.get())
                     v+=1
                     v=v%4
                     var1.set(str(v))
                     print "change mode"
             if k==ord('a'):
                     v=int(var1.get())
                     v-=1
                     if v<0:
                             v=3
                     var1.set(str(v))
             if k==ord('p'):
                     v=int(settingsCon['newdata'].get())
                     v+=1
                     v=v%2
                     settingsCon['newdata'].set((v))
                     print "pause"
             if k==ord('b'):
                     v=int(settingsCon['debug'].get())
                     v+=1
                     v=v%2
                     settingsCon['debug'].set((v))
             if k==ord('l'):
                     setValues()
                     
             continue
   vidFile.release()
quit_()
print "Gotov je tred ovo nije problem"

   

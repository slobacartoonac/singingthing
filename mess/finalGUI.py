#!/usr/bin/python
from Tkinter import *
import threading
import Queue
import tkMessageBox
import numpy as np
from Queue import Empty
import cv2
from PIL import Image, ImageTk
import time
import Tkinter as tk
import ttk
import settingsWindow
import hogDetect
import haarcascades
import bgSubtraction
import manualDetect
sys.path.append("sound")
import play_move
import projection
import singleton
import math


global tmpImg
tmpImg = None
global background
background = None
global debug
debug = 0
settingsCon = singleton.settings()

def onScale():

        
        print 'scroll'
                
    
def debugMode():
        global debug
        debug+=1
        debug = debug % 2
        if debug==0:
                cv2.destroyAllWindows()
def showFreq(fff):
        if fff!=None:
                        tf='Frequency is: %d'%int(fff[2])
                        txy='Coordinates of object are: %.2f and %.2f'%(fff[0],fff[1])
                        settingsCon['freq'].set(tf)
                        settingsCon['xy'].set(txy)
                        

def getProcMet(var, input):
        v = var.get()
        settingsCon = singleton.settings()
        settPlay=(float(settingsCon['minSpeed'].get()),float(settingsCon['maxSpeed'].get()),
                  float(settingsCon['minFreq'].get()),float(settingsCon['maxFreq'].get()),
                  float(settingsCon['audioRate'].get()),float(settingsCon['positionBuff'].get()),settingsCon['mute'].get())
        #print v
        if v == 1:
                 output=manualDetect.manualDetect(input, background, debug)
                 fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                 showFreq(fff)
                 return output[0]
        elif v == 2:
                output=bgSubtraction.bgSubtraction(input, (), debug)
                #print "bilopre"
                #print "calling ", output[1]
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                #print fff
                showFreq(fff)
                #else :print "BUG"
                #print "bilosta"
                #if(output[1]==(0,0)):
                #        print "ne sviraj majke ti ga"
                return output[0]

                
                
        elif v == 3:
                output=haarcascades.haarcascades(input, 1, debug)
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                showFreq(fff)
                return output[0]
                
        else:
                output=hogDetect.hogDetect(input, (), ())
                fff=play_move.motion(output[1],settingsCon['ccam'],settPlay)
                showFreq(fff)
                return output[0]


def captureBg(queue):#Snima pozadinsku sliku za manualDetect
        global background
        background = queue.get()
        print 'get background'
        print background.shape
        #cv2.imshow('bg', background)
        
def quit_(root, process):
   global runTk
   runTk = 0
   cv2.destroyAllWindows()
   play_move.end()
   root.destroy()

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

def banner(text):
        settingsCon = singleton.settings()
        text = text[1:] + text [0]
        settingsCon['banner'].set(text)
        
        




#tkinter GUI functions----------------------------------------------------------


def update_image(image_label, queue, var):
        
        try:
           #frame = None
           framein = queue.get(False)
           frame = getProcMet(var,framein)
           #print 'frame', frame.shape
           im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
           a = Image.fromarray(im)
           b = ImageTk.PhotoImage(image=a)
           image_label.configure(image=b)
           image_label._image_cache = b  # avoid garbage collection
           settingsCon = singleton.settings()
           #Scrollso text in the bootom right corner
           tTime =time.time()
           if tTime>settingsCon['oldTime'] + 0.2:
                   banner(settingsCon['banner'].get())
                   settingsCon['oldTime']=tTime            
           
           root.update()
           

        except:
                x=1
                #print 'Update failed'

def update_all(root, image_label, queue, var):
   update_image(image_label, queue, var)
   root.after(0, func=lambda: update_all(root, image_label, queue, var))

#multiprocessing image processing functions-------------------------------------
def image_capture(queue, run, source):
        vidFile = cv2.VideoCapture(source)
        vidFile.set(3, 640)     #horizontal pixels
        vidFile.set(4,480)		#vertical pixels
        flag, frame=vidFile.read()
        while vidFile.isOpened():
                if runTk == 0:
                        print "\nrunTk kill this thread\n"
                        break
                else:
                      try:
                         if settingsCon['newdata'].get():
                                 flag, frame=vidFile.read()
                         
                         if flag==0:
                            print "\nflag kill this thread\n"
                            break
                 #cv2.imshow("Input file", frame)
                         queue.put(frame)
                         cv2.waitKey(20)
                       
                        
                      except:
                         continue
        print "Gotov je tred ovo nije problem"
        vidFile.release()
        

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

if __name__ == '__main__':

   settingsCon = singleton.settings()
   
   source =  "fortest3.avi"

   h, w = getVideoSize(source)
   camSet=camProperties()
   settingsCon['ccam']=projection.cammera(w,h,camSet[0],camSet[1])
   settingsCon['ccam'].set_position(camSet[2], camSet[3])
   print h
   print w 
   videoSize = 'Video size: %d x %d'%(w,h) 
   
   
   global runTk
   runTk = 1
   queue = Queue.Queue(maxsize=5)
   print 'queue initialized...'
   root = tk.Tk()
   root.title('SingThing')
   print 'GUI initialized...'
   var1 = IntVar()
   var1.set('2')

   


   settingsCon['banner'] = StringVar()
   settingsCon['banner'].set('   Program created by Slobodan: slobacartoonac@hotmail.com and Marko: markoni985@hotmail.com')
   
   settingsCon['mute'] = IntVar()
   settingsCon['minArea'] = IntVar()
   settingsCon['maxArea'] = IntVar()
   settingsCon['bgHistory'] = IntVar()
   settingsCon['bgTresh'] = IntVar()
   settingsCon['freq'] = StringVar()
   settingsCon['xy'] = StringVar()
   settingsCon['minArea'].set('1000')
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
   settingsCon['minFreq'].set('40')
   settingsCon['maxFreq'].set('500')
   settingsCon['audioRate'] = IntVar()
   settingsCon['positionBuff'] = IntVar()
   settingsCon['audioRate'].set('10')
   settingsCon['positionBuff'].set('5')
   settingsCon['newdata']=IntVar()
   settingsCon['newdata'].set('0')
   
   print settingsCon['minArea']
   print settingsCon['maxArea']
   print settingsCon['bgHistory']
   print settingsCon['bgTresh']

   settingsCon['oldTime']=time.time()
   frame= Frame(root, height=500, width=1200)
   frame.grid(row=0, column=0)
   frame2= Frame(root, height=500, width=500)
   frame2.grid(row=0, column=1)
   # Controll buttons
   tk.Button(frame2, text='CAPTURE', command=lambda: captureBg(queue), height=5, width=20).grid(row=0, column=0)
   tk.Button(frame2, text='DEBUG  ', command=lambda: debugMode(), height=5, width=20).grid(row=1, column=0, sticky = N)
   tk.Button(frame2, text='QUIT   ', command=lambda: quit_(root,p), height=5, width=20).grid(row=3, column=0, sticky = N)
   # Mode buttons
   Radiobutton(frame2, text="Mode 1", variable=var1, value=1, indicatoron = 0,width = 14,padx = 20,).grid(row=4, column=0,sticky=('W', 'E'))#, sticky=W)  
   Radiobutton(frame2, text="Mode 2", variable=var1, value=2, indicatoron = 0,width = 14,padx = 20,).grid(row=5, column=0,sticky=('W', 'E'))#, sticky=W)
   Radiobutton(frame2, text="Mode 3", variable=var1, value=3, indicatoron = 0,width = 14,padx = 20,).grid(row=6, column=0,sticky=('W', 'E'))#, sticky=W)
   Radiobutton(frame2, text="Mode 4", variable=var1, value=4, indicatoron = 0,width = 14,padx = 20,).grid(row=7, column=0,sticky=('W', 'E'))#, sticky=W)
   # Volume
   tk.Checkbutton(frame2, text="Mute", variable=settingsCon['mute'],indicatoron = 0).grid(column=0, row=8, sticky=('W', 'E'))
   tk.Checkbutton(frame2, text="Play", variable=settingsCon['newdata'],indicatoron = 0).grid(column=0, row=9, sticky=('W', 'E'))
   #tk.Label(frame2, text="Volume").grid(column=0, row=8)
   #volumeSk = ttk.LabeledScale(frame2, from_=0, to=100,variable=volume)
   #volumeSk.grid(column=0, row=9, sticky=('W', 'E'))
   # Configure menu
   tk.Button(frame2, text='CONFIGURE   ', command=lambda: settingsWindow.settingsWindow(), height=2, width=20).grid(row=10, column=0, sticky = N)
   
  # label for the video frame
   image_label = tk.Label(frame)#, height=480, width=640)#.grid(row=0)
   image_label.grid(column=0, row=0, sticky = ('W', 'N'))
   #Video Size Label
   size_label = tk.Label(frame, text = videoSize)
   size_label.grid(column= 0, row=1,sticky = W)
   size_label = tk.Label(frame, textvariable = settingsCon['xy'])
   size_label.grid(column= 0, row=2,sticky = W)
   # Sound freq indicator
   sound_label = tk.Label(frame2, textvariable = settingsCon['freq'])
   sound_label.grid(column=0, row=11)
   # OpenCV parameter settings
   n = ttk.Notebook(root)
   n.grid(column=2, row=0, sticky=('S', 'N'))
   f1 = ttk.Frame(n)   # first page, which would get widgets gridded into it
   f2 = ttk.Frame(n)   # second page
   f3 = ttk.Frame(n)
   n.add(f1, text='Video')
   n.add(f2, text='Speed/Freq')
   n.add(f3, text='Audio')
   tk.Label(f1, text="Min Area").grid(column=0, row=0)
   tk.Label(f1, text="Max Area").grid(column=1, row=0)
   tk.Label(f1, text="History").grid(column=2, row=0)
   tk.Label(f1, text="Threshold").grid(column=3, row=0)
   minAreaSk = Scale(f1, from_=5000, to=0,variable=settingsCon['minArea'],length=400)
   minAreaSk.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   maxAreaSk = Scale(f1, from_=15000, to=0,variable=settingsCon['maxArea'],length=400)
   maxAreaSk.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   history = Scale(f1, from_=300, to=0,variable=settingsCon['bgHistory'],length=400)
   history.grid(column=2, row=1,rowspan =9, sticky=('S', 'N'))
   Threshold = Scale(f1, from_=1000, to=0,variable=settingsCon['bgTresh'],length=400)
   Threshold.grid(column=3, row=1,rowspan =9, sticky=('S', 'N'))
   tk.Label(f2, text="Min Speed").grid(column=0, row=0)
   tk.Label(f2, text="Max speed").grid(column=1, row=0)
   tk.Label(f2, text="Min Freq").grid(column=2, row=0)
   tk.Label(f2, text="Max Freq").grid(column=3, row=0)
   tk.Label(f3, text="Audio Rate").grid(column=0, row=0)
   tk.Label(f3, text="Buffer").grid(column=1, row=0)
   minAreaSk = Scale(f2, from_=10, to=0,variable=settingsCon['minSpeed'],length=400)
   minAreaSk.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   maxAreaSk = Scale(f2, from_=20, to=5,variable=settingsCon['maxSpeed'],length=400)
   maxAreaSk.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   history = Scale(f2, from_=2000, to=40,variable=settingsCon['minFreq'],length=400)
   history.grid(column=2, row=1,rowspan =9, sticky=('S', 'N'))
   Threshold = Scale(f2, from_=2000, to=40,variable=settingsCon['maxFreq'],length=400)
   Threshold.grid(column=3, row=1,rowspan =9, sticky=('S', 'N'))
   audioRate = Scale(f3, from_=30, to=1,variable=settingsCon['audioRate'],length=400)
   audioRate.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   positionBuff = Scale(f3, from_=10, to=3,variable=settingsCon['positionBuff'],length=400)
   positionBuff.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   creators = tk.Label(root, textvariable=settingsCon['banner'], width= 30, justify=LEFT)#, wraplength=200)
   creators.grid(column = 2, row=1 , sticky=E)

   print 'GUI image label initialized...'
   # Image capture thread
   p = threading.Thread(target=image_capture,args=(queue, runTk, source))
   p.start()
   print 'image capture process has started...'
   # quit button
   #quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   #quit_button.pack()
   print 'quit button initialized...'
   # setup the update callback
   update_all(root, image_label, queue, var1)
   print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   runTk=0
   p.join()
   print 'image capture process exit'

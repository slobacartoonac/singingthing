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


global tmpImg
tmpImg = None
global background
background = None
global debug
debug = 0

                
                
    
def debugMode():
        global debug
        debug+=1
        debug = debug % 2
        if debug==0:
                cv2.destroyAllWindows()

def getProcMet(var, input,ccam):
        v = var.get()
        #print v
        if v == 1:
                 output=manualDetect.manualDetect(input, background, debug)
                 play_move.motion(output[1],ccam)
                 return output[0]
        elif v == 2:
                output=haarcascades.haarcascades(input, 1, debug)
                return output
        elif v == 3:
                output=bgSubtraction.bgSubtraction(input, (), debug)
                #print "bilopre"
                play_move.motion(output[1],ccam)
                #print "bilosta"
                #if(output[1]==(0,0)):
                #        print "ne sviraj majke ti ga"
                return output[0]
        else:
                output=hogDetect.hogDetect(input, (), ())
                return output


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
                return (x*math.pi/180, y*math.pi/180, hc, dc)

        except:
                print sys.exc_info()[0]
                return (3.14/4, 3.14/5, 10, 10)




#tkinter GUI functions----------------------------------------------------------


def update_image(image_label, queue, var,ccam):
        
        try:
           #frame = None
           framein = queue.get(False)
           frame = getProcMet(var,framein,ccam)
           #print 'frame', frame.shape
           im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
           a = Image.fromarray(im)
           b = ImageTk.PhotoImage(image=a)
           image_label.configure(image=b)
           image_label._image_cache = b  # avoid garbage collection
           root.update()

        except:
                x=1
                #print 'Update failed'

def update_all(root, image_label, queue, var,ccam):
   update_image(image_label, queue, var,ccam)
   root.after(0, func=lambda: update_all(root, image_label, queue, var,ccam))

#multiprocessing image processing functions-------------------------------------
def image_capture(queue, run, source):
        vidFile = cv2.VideoCapture(source)
        while vidFile.isOpened():
                if runTk == 0:
                        print "\nrunTk kill this thread\n"
                        break
                else:
                      try:
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
        for x in range(0,5):
                try:
                        flag, frame=vidFile.read()
                        (h,w,c)= frame.shape
                        return h,w
                except:
                        print 'Can not get size of video'
        vidFile.release()

if __name__ == '__main__':
   source = "fortest3.avi"
   
   h, w = getVideoSize(source)
   camSet=camProperties()
   ccam=projection.cammera(w,h,camSet[0],camSet[1])
   ccam.set_position(camSet[2], camSet[3])
   print h
   print w
   global runTk
   runTk = 1
   queue = Queue.Queue(maxsize=5)
   print 'queue initialized...'
   root = tk.Tk()
   print 'GUI initialized...'
   var1=IntVar()
   var1.set('3')
   freq = StringVar()
   freq.set('0000')
   volume = IntVar()
   volume.set('0')
   frame= Frame(root, height=500, width=900)
   frame.grid(row=0, column=0)
   frame2= Frame(root, height=500, width=400)
   frame2.grid(row=0, column=1)
   # Controll buttons
   tk.Button(frame2, text='CAPTURE', command=lambda: captureBg(queue), height=5, width=20).grid(row=0, column=0)
   tk.Button(frame2, text='DEBUG  ', command=lambda: debugMode(), height=5, width=20).grid(row=1, column=0, sticky = N)
   tk.Button(frame2, text='QUIT   ', command=lambda: quit_(root,p), height=5, width=20).grid(row=3, column=0, sticky = N)
   # Mode buttons
   Radiobutton(frame2, text="Mode 1", variable=var1, value=1, indicatoron = 0,width = 14,padx = 20,).grid(row=4)#, sticky=W)  
   Radiobutton(frame2, text="Mode 2", variable=var1, value=2, indicatoron = 0,width = 14,padx = 20,).grid(row=5)#, sticky=W)
   Radiobutton(frame2, text="Mode 3", variable=var1, value=3, indicatoron = 0,width = 14,padx = 20,).grid(row=6)#, sticky=W)
   Radiobutton(frame2, text="Mode 4", variable=var1, value=4, indicatoron = 0,width = 14,padx = 20,).grid(row=7)#, sticky=W)
   # Volume 
   tk.Label(frame2, text="Volume").grid(column=0, row=8)
   volumeSk = ttk.LabeledScale(frame2, from_=0, to=100,variable=volume)
   volumeSk.grid(column=0, row=9, sticky=('W', 'E'))
   # Configure menu
   tk.Button(frame2, text='CONFIGURE   ', command=lambda: settingsWindow.settingsWindow(), height=2, width=20).grid(row=10, column=0, sticky = N)
  # label for the video frame
   image_label = tk.Label(frame)#, height=480, width=640)#.grid(row=0)
   image_label.pack(side=TOP)
   # Sound freq indicator
   sound_label = tk.Label(frame2, textvariable = freq)
   sound_label.grid(column = 0, row =11)
   print 'GUI image label initialized...'
   # Image capture thread
   p = threading.Thread(target=image_capture,args=(queue, runTk, source))
   p.start()
   print 'image capture process has started...'
   # quit button
   quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   #quit_button.pack()
   print 'quit button initialized...'
   # setup the update callback
   update_all(root, image_label, queue, var1,ccam)
   print 'root.after was called...'
   root.mainloop()
   print 'mainloop exit'
   runTk=0
   p.join()
   print 'image capture process exit'

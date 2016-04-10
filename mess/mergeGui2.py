#!/usr/bin/python
from Tkinter import *
import sys
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
import wx
import time

global tmpImg
tmpImg = None
global background
background = None
global debug
debug = 0
settingsCon = singleton.settings()


#//////////////////////////////////////////
class ShowCapture(wx.Panel):
    def __init__(self, parent, queue, fps=10):
        wx.Panel.__init__(self, parent, -1,size = (640, 480))

        #self.capture = capture
        frame = queue.get(False)
        print "Camera opend to set wx element"
        height = 480
        width = 640
        #height, width = frame.shape[:2]
        self.SetSize((width, height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(width, height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, lambda event: self.NextFrame(event,var1,queue))
        #capture.release()
        print "Camera released by wx"


    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event, var, queue):
        

        #frame = None
        framein = queue.get(False)
        #print "stage"
        frame = getProcMet(var,framein)
        #print "stage"
        #print 'frame', frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.bmp.CopyFromBuffer(frame)

        self.Refresh()
        
        
           




class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,size = (400, 500))
        l1 = wx.StaticText(self, -1, "Min Area", style=wx.ALIGN_CENTRE)
        minAreaSk = wx.Slider(self, value=200, minValue=0, maxValue=5000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l2 = wx.StaticText(self, -1, "Max Area", style=wx.ALIGN_CENTRE)
        maxAreaSk = wx.Slider(self, value=200, minValue=0, maxValue=15000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l3 = wx.StaticText(self, -1, "History", style=wx.ALIGN_CENTRE)
        history = wx.Slider(self, value=200, minValue=0, maxValue=300, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l4 = wx.StaticText(self, -1, "Threshold", style=wx.ALIGN_CENTRE)
        Treshold = wx.Slider(self, value=200, minValue=0, maxValue=1000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        minAreaSk.Bind(wx.EVT_SCROLL, lambda event: self.OnSliderScroll(event, settingsCon['minArea']))
        maxAreaSk.Bind(wx.EVT_SCROLL, lambda event: self.OnSliderScroll(event, settingsCon['maxArea']))
        history.Bind(wx.EVT_SCROLL, lambda event: self.OnSliderScroll(event, settingsCon['bgHistory']))
        Treshold.Bind(wx.EVT_SCROLL, lambda event: self.OnSliderScroll(event, settingsCon['bgTresh']))

        gridSizerOne = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer12 = wx.BoxSizer(wx.VERTICAL)
        sizer13 = wx.BoxSizer(wx.VERTICAL)
        sizer14 = wx.BoxSizer(wx.VERTICAL)

        sizer11.Add(l1, 0, wx.EXPAND|wx.ALL)
        sizer11.Add(minAreaSk, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(l2, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(maxAreaSk, 0, wx.EXPAND|wx.ALL)
        sizer13.Add(l3, 0, wx.EXPAND|wx.ALL)
        sizer13.Add(history, 0, wx.EXPAND|wx.ALL)
        sizer14.Add(l4, 0, wx.EXPAND|wx.ALL)
        sizer14.Add(Treshold, 0, wx.EXPAND|wx.ALL)
        gridSizerOne.Add(sizer11, 0, wx.EXPAND)
        gridSizerOne.Add(sizer12, 0, wx.EXPAND)
        gridSizerOne.Add(sizer13, 0, wx.EXPAND)
        gridSizerOne.Add(sizer14, 0, wx.EXPAND)
        self.SetSizer(gridSizerOne)
        self.SetBackgroundColour("YELLOW")
    def OnSliderScroll(self, e, target):
        
        obj = e.GetEventObject()
        val = obj.GetValue()
        valst= '(%d)' %val
        target.set(val)
        print val
        #self.txt.SetLabel(str(val)) 
        
        

        #button1 = wx.Button(self, -1, label="click me")

class PageTwo(wx.Panel):
    def __init__(self, parent,size = (400, 500)):
        wx.Panel.__init__(self, parent)
        l1 = wx.StaticText(self, -1, "Min Speed", style=wx.ALIGN_CENTRE)
        minSpeedSk = wx.Slider(self, value=200, minValue=0, maxValue=10, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l2 = wx.StaticText(self, -1, "Max Speed", style=wx.ALIGN_CENTRE)
        maxSpeedSk = wx.Slider(self, value=200, minValue=5, maxValue=20, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l3 = wx.StaticText(self, -1, "Min Freq", style=wx.ALIGN_CENTRE)
        minFreq = wx.Slider(self, value=200, minValue=40, maxValue=2000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l4 = wx.StaticText(self, -1, "Max Freq", style=wx.ALIGN_CENTRE)
        maxFreq = wx.Slider(self, value=200, minValue=40, maxValue=2000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        gridSizerOne = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer12 = wx.BoxSizer(wx.VERTICAL)
        sizer13 = wx.BoxSizer(wx.VERTICAL)
        sizer14 = wx.BoxSizer(wx.VERTICAL)

        sizer11.Add(l1, 0, wx.EXPAND|wx.ALL)
        sizer11.Add(minSpeedSk, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(l2, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(maxSpeedSk, 0, wx.EXPAND|wx.ALL)
        sizer13.Add(l3, 0, wx.EXPAND|wx.ALL)
        sizer13.Add(minFreq, 0, wx.EXPAND|wx.ALL)
        sizer14.Add(l4, 0, wx.EXPAND|wx.ALL)
        sizer14.Add(maxFreq, 0, wx.EXPAND|wx.ALL)
        
        gridSizerOne.Add(sizer11, 0, wx.EXPAND)
        gridSizerOne.Add(sizer12, 0, wx.EXPAND)
        gridSizerOne.Add(sizer13, 0, wx.EXPAND)
        gridSizerOne.Add(sizer14, 0, wx.EXPAND)
        self.SetSizer(gridSizerOne)

class PageThree(wx.Panel):
    def __init__(self, parent,size=(400, 500)):
        wx.Panel.__init__(self, parent)
        l1 = wx.StaticText(self, -1, "Audio Rate", style=wx.ALIGN_CENTRE)
        audioRate = wx.Slider(self, value=200, minValue=1, maxValue=30, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l2 = wx.StaticText(self, -1, "Buffer", style=wx.ALIGN_CENTRE)
        positionBuff = wx.Slider(self, value=200, minValue=3, maxValue=10, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)


        gridSizerOne = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.VERTICAL)
        sizer12 = wx.BoxSizer(wx.VERTICAL)


        sizer11.Add(l1, 0, wx.EXPAND|wx.ALL)
        sizer11.Add(audioRate, 0, wx.EXPAND|wx.ALL)

        sizer12.Add(l2, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(positionBuff, 0, wx.EXPAND|wx.ALL)

        gridSizerOne.Add(sizer11, 0, wx.EXPAND)
        gridSizerOne.Add(sizer12, 0, wx.EXPAND)
        self.SetSizer(gridSizerOne)



class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,size = (1200, 600))
        #sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
        
        #topPanel = wx.Panel(self)
        #print topPanel.GetSize()
        
        panel1 = ShowCapture(self, queue)
        #panel1 = wx.Panel(topPanel, -1,pos=(0,100),size=(100,100))
        #button1 = wx.Button(panel1, -1, label="click me")
        panel2 = wx.Panel(self, -1,size = (200, 600))
        panel3 = wx.Panel(self, -1,size = (400, 600))
        panel1.SetBackgroundColour("BLUE")
        panel2.SetBackgroundColour("GREEN")
        panel3.SetBackgroundColour("RED")
        p1size = panel1.GetSize()
        p2size = panel2.GetSize()
        p3size = panel3.GetSize()
        fsize = (p1size[0]+p2size[0]+p3size[0]+20,p1size[1]+p2size[1]+p3size[1]+0)
        #self.SetSize(fsize)

        
        button1 = wx.Button(panel2, -1, label="CAPTURE")
        button2 = wx.Button(panel2, -1, label="DEBUG")
        button3 = wx.Button(panel2, -1, label="QUIT")

        button1.Bind(wx.EVT_BUTTON, lambda event: captureBg(queue))
        button2.Bind(wx.EVT_BUTTON, lambda event: debugMode())
        button3.Bind(wx.EVT_BUTTON, lambda event: quit_(root,p))

        rb1 = wx.RadioButton(panel2, label='MODE 1', style=wx.RB_GROUP)
        rb2 = wx.RadioButton(panel2, label='MODE 2' )
        rb3 = wx.RadioButton(panel2, label='MODE 3' )
        rb4 = wx.RadioButton(panel2, label='MODE 4' )

        tb1 = wx.ToggleButton(panel2, label='MUTE')
        tb2 = wx.ToggleButton(panel2, label='PLAY')
        button4 = wx.Button(panel2, -1, label="CONFIG")
        button4.Bind(wx.EVT_BUTTON, self.Config)

        tb1.Bind(wx.EVT_TOGGLEBUTTON, self.Mute)
        tb2.Bind(wx.EVT_TOGGLEBUTTON, self.Play)

        nb = wx.Notebook(panel3, -1, style=wx.NB_TOP, size = (400, 600))
        nb.SetBackgroundColour("BLUE")
        #sheet1  = wx.Panel(panel3, -1, style=wx.SUNKEN_BORDER)
        #sheet2  = wx.Panel(panel3, -1, style=wx.SUNKEN_BORDER)
        #sheet3  = wx.Panel(panel3, -1, style=wx.SUNKEN_BORDER)
        sheet1 = PageOne(nb)
        sheet2 = PageTwo(nb)
        sheet3 = PageThree(nb)
        nb.AddPage(sheet1, "Video")
        nb.AddPage(sheet2, "Speed/Frequency")
        nb.AddPage(sheet3, "Audio")
        sheet1.SetFocus()

        sizerN = wx.BoxSizer(wx.VERTICAL)
        sizerN.Add(nb, -1, wx.EXPAND|wx.ALL)
        panel3.SetSizer(sizerN)

        

        sizerB = wx.BoxSizer(wx.VERTICAL)
        sizerB.Add(button1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(button2,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(button3,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(rb1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(rb2,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(rb3,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(rb4,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(tb1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(tb2,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(button4,0,wx.EXPAND|wx.ALL,border=10)
        panel2.SetSizer(sizerB)

        #sizerB.Add(nb,0,wx.EXPAND|wx.ALL,border=10)
        #panel3.SetSizer(sizerB)
        
        #print topPanel.GetSize()
        print panel1.GetSize()
        print panel2.GetSize()
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel1,0,wx.EXPAND|wx.ALL,border=10)
        sizer.Add(panel2,0,wx.EXPAND|wx.ALL,border=10)
        sizer.Add(panel3,0,wx.EXPAND|wx.ALL,border=10)

        self.SetSizer(sizer)
    
    def Mute(self, e):

            obj = e.GetEventObject()
            isPressed = obj.GetValue()
                
            if isPressed:
                settingsCon['mute'].set('1')
            else:
                settingsCon['mute'].set('0')

    def Play(self, e):

            obj = e.GetEventObject()
            isPressed = obj.GetValue()
                    
            if isPressed:
                settingsCon['newdata'].set('1')
            else:
                settingsCon['newdata'].set('0')
            print settingsCon['newdata']

    def Config(self, e):
        
        print "CONFIG"
        settingsWindow.settingsWindow()
        print "CONFIG DONE"
        


        



class MyApp(wx.App):
     def OnInit(self):
         frame = MyFrame(None, -1, 'Sing Thing')
         frame.Show(True)
         return True


#//////////////////////////////////////////


def onScale():

        
        print 'scroll'
                
    
def debugMode():
        print "Debug"
        global debug
        debug+=1
        debug = debug % 2
        if debug==0:
                cv2.destroyAllWindows()
        print  debug
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
        print "Bacground capture"
        global background
        background = queue.get()
        print 'get background'
        print background.shape
        #cv2.imshow('bg', background)
        
def quit_(root, process):
   print "Quit"
   global runTk
   runTk = 0
   cv2.destroyAllWindows()
   play_move.end()
   root.destroy()

def camProperties():
        print "Trying to open settings file"
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
                print "Opening failed, using degoult values"
                print sys.exc_info()[0]
                return (3.14/4, 3.14/5, 10, 10)

def banner(text):
        settingsCon = singleton.settings()
        text = text[1:] + text [0]
        settingsCon['banner'].set(text)
        
        








#multiprocessing image processing functions-------------------------------------
def image_capture(queue, run, source):
        vidFile = cv2.VideoCapture(source)
        vidFile.set(3, 640)     #horizontal pixels
        vidFile.set(4, 480)     #vertical pixels
        flag, frame=vidFile.read()
        while vidFile.isOpened():
                #print "capture loop"
                if runTk == 0:
                        print "\nrunTk kill this thread\n"
                        break
                else:
                      try:
                         if settingsCon['newdata'].get():
                                 flag, frame=vidFile.read()
                                 #print "Image queued"
                         
                         if flag==0:
                            print "\nflag kill this thread\n"
                            break
                         #cv2.imshow("Input file", frame)
                         queue.put(frame)
                         cv2.waitKey(20)
                       
                        
                      except:
                         print "continue"
                         continue
        print "Gotov je tred ovo nije problem"
        vidFile.release()
        

def getVideoSize(source):
        print "Opening Camera to get  h and w"
        vidFile = cv2.VideoCapture(source)
        vidFile.set(3, 640)     #horizontal pixels
        vidFile.set(4, 480)     #vertical pixels
        for x in range(0,5):
                try:
                        flag, frame=vidFile.read()
                        (h,w,c)= frame.shape
                        return h,w
                except:
                        print 'Can not get size of video'
        vidFile.release()
        print "Closing camera (h,w)"

if __name__ == '__main__':

   settingsCon = singleton.settings()
   print "Singleton initialised"
   
   source =  0#"18.avi"

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
   #root.title('SingThing')
   #print 'GUI initialized...'
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
   settingsCon['newdata'].set('1')
   
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
   time.sleep(3)
   print 'image capture process has started...'
   # quit button
   #quit_button = tk.Button(master=root, text='Quit',command=lambda: quit_(root,p))
   #quit_button.pack()
   print 'quit button initialized...'
   # setup the update callback
   #update_all(root, image_label, queue, var1)
   print 'root.after was called...'
   #root.mainloop()
   app = MyApp(0)
   app.MainLoop()
   
   print 'mainloop exit'
   runTk=0
   quit_(root,p)
   p.join()
   print 'image capture process exit'

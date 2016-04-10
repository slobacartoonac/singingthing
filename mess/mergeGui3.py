#!/usr/bin/python
#from Tkinter import *
import sys
import threading
import Queue
#import tkMessageBox
import numpy as np
from Queue import Empty
import cv2
#from PIL import Image, ImageTk
import time
#import Tkinter as tk
#import ttk
import settingsWindow2 as settingsWindow
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
        wx.Panel.__init__(self, parent, -1, size = (640, 520))
        empty = wx.EmptyBitmap(480, 640)
        x=1
        topSizer = wx.BoxSizer(wx.VERTICAL)
        self.panel1 = wx.Panel(self, -1,size = (640, 480))
        self.panel2 = wx.Panel(self, -1,size = (640, 40))
        self.l1 = wx.StaticText(self.panel2, -1, "", style=wx.ALIGN_CENTRE)
        #self.capture = capture
        while(x!=0):
            try:
                frame = queue.get(False)
                print "Camera opend to set wx element"
                height = 480
                width = 640
                #height, width = frame.shape[:2]
                self.SetSize((width, height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                self.bmp = wx.BitmapFromBuffer(width, height, frame)
                x=0
            except:
                x=1
            
        topSizer.Add(self.panel1, -1, wx.EXPAND|wx.ALL)
        topSizer.Add(self.panel2, -1, wx.EXPAND|wx.ALL)
        self.SetSizer(topSizer)
        self.panel1.timer = wx.Timer(self.panel1)
        self.panel1.timer.Start(1000./fps)

        self.panel1.Bind(wx.EVT_PAINT, self.OnPaint)
        self.panel1.Bind(wx.EVT_ERASE_BACKGROUND , self.DoNothing)
        self.panel1.Bind(wx.EVT_TIMER, lambda event: self.NextFrame(event,var1,queue))
        #capture.release()
        print "Camera released by wx"

    def DoNothing(self, evt):
        mrk = 1

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self.panel1)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event, var, queue):
             
           framein = None
           try:
               pom=queue.get_nowait()
               framein=pom
               #framein = queue.get(False)
               #print "stage"
               frame = getProcMet(var,framein)
               #print "stage"
               #print 'frame', frame.shape
               frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
               self.bmp.CopyFromBuffer(frame)
               self.l1.SetLabel(settingsCon['freq'])
               self.Refresh()
               #print "stage"
           except:
               framein=framein
               #print "none"

class FloatSlider(wx.Slider):

    def __init__(self, parent, id, value, minval, maxval, res, target,
                 size=(400, 500), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE):
        self._value = value
        self._min = minval
        self._max = maxval
        self._res = res
        self._target = target
        ival, imin, imax = [round(v/res) for v in (value, minval, maxval)]
        self._islider = super(FloatSlider, self)
        self._islider.__init__(
            parent, id, ival, imin, imax, size=size, style=style        )
        self.Bind(wx.EVT_SCROLL, self._OnScroll)

    def _OnScroll(self, event):
        ival = self._islider.GetValue()
        imin = self._islider.GetMin()
        imax = self._islider.GetMax()
        if ival == imin:
            self._value = self._min
        elif ival == imax:
            self._value = self._max
        else:
            self._value = ival * self._res
        event.Skip()
        print 'OnScroll: value=%f, ival=%d' % (self._value, ival)
        if(self._target==1):
            settingsCon['minSpeed'] = self._value
        else:
            settingsCon['maxSpeed'] = self._value
        #print target

    def GetValue(self):
        return self._value

    def GetMin(self):
        return self._min

    def GetMax(self):
        return self._max

    def GetRes(self):
        return self._res

    def SetValue(self, value):
        self._islider.SetValue(round(value/self._res))
        self._value = value

    def SetMin(self, minval):
        self._islider.SetMin(round(minval/self._res))
        self._min = minval

    def SetMax(self, maxval):
        self._islider.SetMax(round(maxval/self._res))
        self._max = maxval

    def SetRes(self, res):
        self._islider.SetRange(round(self._min/res), round(self._max/res))
        self._islider.SetValue(round(self._value/res))
        self._res = res


class PageOne(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent,size = (450, 500))
        l1 = wx.StaticText(self, -1, "Min Area", style=wx.ALIGN_CENTRE)
        minAreaSk = wx.Slider(self, value=settingsCon['minArea'], minValue=0, maxValue=5000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l2 = wx.StaticText(self, -1, "Max Area", style=wx.ALIGN_CENTRE)
        maxAreaSk = wx.Slider(self, value=settingsCon['maxArea'], minValue=0, maxValue=15000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l3 = wx.StaticText(self, -1, "History", style=wx.ALIGN_CENTRE)
        history = wx.Slider(self, value=settingsCon['bgHistory'], minValue=0, maxValue=300, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l4 = wx.StaticText(self, -1, "Threshold", style=wx.ALIGN_CENTRE)
        treshold = wx.Slider(self, value=settingsCon['bgTresh'], minValue=0, maxValue=1000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        minAreaSk.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 1))
        maxAreaSk.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 2))
        history.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 3))
        treshold.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 4))

        topSizer = wx.BoxSizer(wx.VERTICAL)
        gridSizerOne = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        gridSizerTwo = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer24 = wx.BoxSizer(wx.HORIZONTAL)

        sizer11.Add(l1, -1, wx.EXPAND|wx.ALL)
        sizer21.Add(minAreaSk, -1, wx.EXPAND|wx.ALL)
        sizer12.Add(l2, -1, wx.EXPAND|wx.ALL)
        sizer22.Add(maxAreaSk, -1, wx.EXPAND|wx.ALL)
        sizer13.Add(l3, -1, wx.EXPAND|wx.ALL)
        sizer23.Add(history, -1, wx.EXPAND|wx.ALL)
        sizer14.Add(l4, -1, wx.EXPAND|wx.ALL)
        sizer24.Add(treshold, -1, wx.EXPAND|wx.ALL)
        
        gridSizerOne.Add(sizer11, -1, wx.EXPAND)
        gridSizerOne.Add(sizer12, -1, wx.EXPAND)
        gridSizerOne.Add(sizer13, -1, wx.EXPAND)
        gridSizerOne.Add(sizer14, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer21, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer22, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer23, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer24, -1, wx.EXPAND)

        topSizer.Add(gridSizerOne, 1, wx.EXPAND)
        topSizer.Add(gridSizerTwo, 9, wx.EXPAND)
        self.SetSizer(topSizer)
        #self.SetBackgroundColour("YELLOW")
        
def OnSliderScroll(e, target):
        
    obj = e.GetEventObject()
    val = obj.GetValue()
    
    if(target==1):
        settingsCon['minArea'] = val
    elif(target==2):
        settingsCon['maxArea'] = val
    elif(target==3):
        settingsCon['bgHistory'] = val
    elif(target==4):
        settingsCon['bgTresh'] = val
    elif(target==5):
        settingsCon['minSpeed'] = val
    elif(target==6):
        settingsCon['maxSpeed'] = val
    elif(target==7):
        settingsCon['minFreq'] = val
    elif(target==8):
        settingsCon['maxFreq'] = val
    elif(target==9):
        settingsCon['audioRate'] = val
    elif(target==10):
        settingsCon['positionBuff'] = val
        
    print val
    print target
        

class PageTwo(wx.Panel):
    def __init__(self, parent,size = (450, 500)):
        wx.Panel.__init__(self, parent)
        l1 = wx.StaticText(self, -1, "Min Speed x5", style=wx.ALIGN_CENTRE)
        minSpeedSk = FloatSlider(self,-1,  settingsCon['minSpeed'],0, 10, 0.2, 1)
        minSpeedSk.SetValue(settingsCon['minSpeed'])

        l2 = wx.StaticText(self, -1, "Max Speed x5", style=wx.ALIGN_CENTRE)
        maxSpeedSk = FloatSlider(self,-1,  settingsCon['maxSpeed'],2, 20, 0.5, 2)


        l3 = wx.StaticText(self, -1, "Min Freq", style=wx.ALIGN_CENTRE)
        minFreq = wx.Slider(self, value=settingsCon['minFreq'], minValue=40, maxValue=2000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l4 = wx.StaticText(self, -1, "Max Freq", style=wx.ALIGN_CENTRE)
        maxFreq = wx.Slider(self, value=settingsCon['maxFreq'], minValue=40, maxValue=4000, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        #minSpeedSk.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 5))
        #maxSpeedSk.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 6))
        minFreq.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 7))
        maxFreq.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 8))

        topSizer = wx.BoxSizer(wx.VERTICAL)
        gridSizerOne = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        gridSizerTwo = wx.GridSizer(rows=1, cols=4, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        sizer13 = wx.BoxSizer(wx.HORIZONTAL)
        sizer14 = wx.BoxSizer(wx.HORIZONTAL)
        sizer21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer23 = wx.BoxSizer(wx.HORIZONTAL)
        sizer24 = wx.BoxSizer(wx.HORIZONTAL)

        sizer11.Add(l1, 0, wx.EXPAND|wx.ALL)
        sizer21.Add(minSpeedSk, 0, wx.EXPAND|wx.ALL)
        sizer12.Add(l2, 0, wx.EXPAND|wx.ALL)
        sizer22.Add(maxSpeedSk, 0, wx.EXPAND|wx.ALL)
        sizer13.Add(l3, 0, wx.EXPAND|wx.ALL)
        sizer23.Add(minFreq, 0, wx.EXPAND|wx.ALL)
        sizer14.Add(l4, 0, wx.EXPAND|wx.ALL)
        sizer24.Add(maxFreq, 0, wx.EXPAND|wx.ALL)
        
        gridSizerOne.Add(sizer11, -1, wx.EXPAND)
        gridSizerOne.Add(sizer12, -1, wx.EXPAND)
        gridSizerOne.Add(sizer13, -1, wx.EXPAND)
        gridSizerOne.Add(sizer14, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer21, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer22, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer23, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer24, -1, wx.EXPAND)

        topSizer.Add(gridSizerOne, 1, wx.EXPAND)
        topSizer.Add(gridSizerTwo, 9, wx.EXPAND)
        self.SetSizer(topSizer)

class PageThree(wx.Panel):
    def __init__(self, parent,size=(450, 500)):
        wx.Panel.__init__(self, parent)
        l1 = wx.StaticText(self, -1, "Audio Rate", style=wx.ALIGN_CENTRE)
        audioRate = wx.Slider(self, value=settingsCon['audioRate'], minValue=1, maxValue=30, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)

        l2 = wx.StaticText(self, -1, "Buffer", style=wx.ALIGN_CENTRE)
        positionBuff = wx.Slider(self, value=settingsCon['positionBuff'], minValue=3, maxValue=10, 
            size=(400, -1), style=wx.SL_VERTICAL| wx.SL_AUTOTICKS|wx.SL_LABELS|wx.SL_LEFT|wx.SL_INVERSE)
        audioRate.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 9))
        positionBuff.Bind(wx.EVT_SCROLL, lambda event: OnSliderScroll(event, 10))



        topSizer = wx.BoxSizer(wx.VERTICAL)
        gridSizerOne = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        gridSizerTwo = wx.GridSizer(rows=1, cols=2, hgap=5, vgap=5)
        sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        sizer12 = wx.BoxSizer(wx.HORIZONTAL)

        sizer21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer22 = wx.BoxSizer(wx.HORIZONTAL)



        sizer11.Add(l1, 0, wx.EXPAND|wx.ALL)
        sizer21.Add(audioRate, 0, wx.EXPAND|wx.ALL)

        sizer12.Add(l2, 0, wx.EXPAND|wx.ALL)
        sizer22.Add(positionBuff, 0, wx.EXPAND|wx.ALL)

        gridSizerOne.Add(sizer11, -1, wx.EXPAND)
        gridSizerOne.Add(sizer12, -1, wx.EXPAND)

        gridSizerTwo.Add(sizer21, -1, wx.EXPAND)
        gridSizerTwo.Add(sizer22, -1, wx.EXPAND)


        topSizer.Add(gridSizerOne, 1, wx.EXPAND)
        topSizer.Add(gridSizerTwo, 9, wx.EXPAND)
        self.SetSizer(topSizer)

class PageFour(wx.Panel):
    def __init__(self, parent,size=(450, 500)):
        wx.Panel.__init__(self, parent)
        self.text = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY, size=(-1,295))
        self.text.SetValue(self.fileRead())
        self.l1 = wx.StaticText(self, -1, "", style=wx.ALIGN_CENTRE)


        topSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer.Add(self.text,15,wx.EXPAND|wx.ALL)
        topSizer.Add(self.l1,1,wx.EXPAND|wx.ALL)
        self.SetSizer(topSizer)
        self.l1.timer = wx.Timer(self)
        self.l1.timer.Start(1000./5)


        self.Bind(wx.EVT_TIMER, self.textBanner)

    def fileRead(self):
        try:
            f=open("LICENCE.txt")
            print 'Licence opened'
            text=f.read()
            f.close()
            return text
        except:
            return "Licence file could not be read."
        
    def textBanner(self,evt):
        text=settingsCon['banner']
        #settingsCon = singleton.settings()
        text = text[1:] + text [0]
        settingsCon['banner']=text
        self.l1.SetLabel(settingsCon['banner'])



class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,size = (1250, 600))

        sizer = wx.GridSizer(rows=1, cols=3, hgap=5, vgap=5)
   
        self.SetBackgroundColour((100,123,189))
        panel1 = ShowCapture(self, queue)
        panel2 = wx.Panel(self, -1,size = (200, 600))
        panel3 = wx.Panel(self, -1,size = (450, 600))
        #panel1.SetBackgroundColour("BLUE")
        panel2.SetBackgroundColour((100,123,189))
        panel3.SetBackgroundColour((100,123,189))
        p1size = panel1.GetSize()
        p2size = panel2.GetSize()
        p3size = panel3.GetSize()
        fsize = (p1size[0]+p2size[0]+p3size[0]+20,p1size[1]+p2size[1]+p3size[1]+0)
        
        button1 = wx.Button(panel2, -1, label="CAPTURE")
        button2 = wx.Button(panel2, -1, label="DEBUG")
        #button3 = wx.Button(panel2, -1, label="QUIT")

        button1.Bind(wx.EVT_BUTTON, lambda event: captureBg(queue))
        button2.Bind(wx.EVT_BUTTON, lambda event: debugMode())
        #button3.Bind(wx.EVT_BUTTON, lambda event: quit_(p))

        self.rb1 = wx.RadioButton(panel2, label='MODE 1', style=wx.RB_GROUP)
        self.rb2 = wx.RadioButton(panel2, label='MODE 2' )
        self.rb3 = wx.RadioButton(panel2, label='MODE 3' )
        self.rb4 = wx.RadioButton(panel2, label='MODE 4' )
        self.rb1.SetValue(False)
        self.rb2.SetValue(True)
        self.rb3.SetValue(False)
        self.rb4.SetValue(False)
        self.Bind(wx.EVT_RADIOBUTTON, self.SetMode)


        tb1 = wx.ToggleButton(panel2, label='MUTE')
        tb2 = wx.ToggleButton(panel2, label='PLAY')
        button4 = wx.Button(panel2, -1, label="CONFIG")
        button4.Bind(wx.EVT_BUTTON, self.Config)

        tb1.Bind(wx.EVT_TOGGLEBUTTON, self.Mute)
        tb2.Bind(wx.EVT_TOGGLEBUTTON, self.Play)

        nb = wx.Notebook(panel3, -1, style=wx.NB_TOP, size = (450, 600))
        #nb.SetBackgroundColour("BLUE")

        sheet1 = PageOne(nb)
        sheet2 = PageTwo(nb)
        sheet3 = PageThree(nb)
        sheet4 = PageFour(nb)
        nb.AddPage(sheet1, "Video")
        nb.AddPage(sheet2, "Speed/Frequency")
        nb.AddPage(sheet3, "Audio")
        nb.AddPage(sheet4, "Licence")
        sheet1.SetFocus()

        sizerN = wx.BoxSizer(wx.VERTICAL)
        sizerN.Add(nb, -1, wx.EXPAND|wx.ALL)
        panel3.SetSizer(sizerN)

        

        sizerB = wx.BoxSizer(wx.VERTICAL)
        sizerB.Add(button1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(button2,0,wx.EXPAND|wx.ALL,border=10)
        #sizerB.Add(button3,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(self.rb1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(self.rb2,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(self.rb3,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(self.rb4,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(tb1,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(tb2,0,wx.EXPAND|wx.ALL,border=10)
        sizerB.Add(button4,0,wx.EXPAND|wx.ALL,border=10)
        panel2.SetSizer(sizerB)

        print panel1.GetSize()
        print panel2.GetSize()
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(panel1,0,wx.EXPAND|wx.ALL,border=10)
        sizer.Add(panel2,0,wx.EXPAND|wx.ALL,border=10)
        sizer.Add(panel3,0,wx.EXPAND|wx.ALL,border=10)

        self.SetSizer(sizer)

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

    def OnCloseWindow(self, evt):
        quit_(p)
        self.Destroy()


    
    def Mute(self, e):

            obj = e.GetEventObject()
            isPressed = obj.GetValue()
                
            if isPressed:
                settingsCon['mute']=1
            else:
                settingsCon['mute']=0

    def Play(self, e):

            obj = e.GetEventObject()
            isPressed = obj.GetValue()
                    
            if isPressed:
                settingsCon['newdata']=1
            else:
                settingsCon['newdata']=0
            print settingsCon['newdata']

    def Config(self, e):
        
        print "CONFIG"
        settingsWindow.settingsWindow()
        print "CONFIG DONE"
        
    def SetMode(self, e):
        
        state1 = self.rb1.GetValue()
        state2 = self.rb2.GetValue()
        state3 = self.rb3.GetValue()
        state4 = self.rb4.GetValue()
        global var1
        if(state1):
            if (background == None):
                captureBg(queue)

            var1=1
        elif(state2):
            var1=2
        elif(state3):
            var1=3
        else:
            var1=4
        print "Mode changed"
        print var1


        



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
                        settingsCon['freq']=tf
                        settingsCon['xy']=txy
                        

def getProcMet(var, input):
        v = var
        settingsCon = singleton.settings()
        settPlay=(float(settingsCon['minSpeed']),float(settingsCon['maxSpeed']),
                  float(settingsCon['minFreq']),float(settingsCon['maxFreq']),
                  float(settingsCon['audioRate']),float(settingsCon['positionBuff']),settingsCon['mute'])
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
        
def quit_(process):
   SaveProperties()
   play_move.end()
   global runTk
   runTk = 0
   cv2.destroyAllWindows()
   print "Quit"
   
   

def camProperties():
        print "Trying to open settings file"
        try:
                f=open("settings.txt")
                print 'file opened'
                var=f.readlines()
                f.close()
                print 'lines read'
                x=float((var[0][:-1]))
                print 'var added'
                y=float((var[1][:-1]))
                hc=float((var[2][:-1]))
                dc=float((var[3][:-1]))
                print 'close'
                
                prmsg = (x*math.pi/180, y*math.pi/180, hc, dc)
                print prmsg
                return (x*math.pi/180, y*math.pi/180, hc, dc)

        except:
                print "Opening failed, using degoult values"
                print sys.exc_info()[0]
                
                return (3.14/4, 3.14/5, 10, 10)
def Properties():
        print "Trying to open settings file"
        try:
                f=open("settings.txt")
                print 'file opened'
                var=f.readlines()
                f.close()
                settingsCon['minArea']=float((var[5][:-1]))
                settingsCon['maxArea']=float((var[6][:-1]))
                settingsCon['bgHistory']=float((var[7][:-1]))
                settingsCon['bgTresh']=float((var[8][:-1]))
                settingsCon['minSpeed']=float((var[9][:-1]))
                settingsCon['maxSpeed']=float((var[10][:-1]))
                settingsCon['minFreq']=float((var[11][:-1]))
                settingsCon['maxFreq']=float((var[12][:-1]))
                settingsCon['audioRate']=float((var[13][:-1]))
                settingsCon['positionBuff']=float((var[14][:-1]))

                

        except:
                print "Opening failed, using defoult values"
                settingsCon['minArea']=1000
                settingsCon['maxArea']=5000
                settingsCon['bgHistory']=10
                settingsCon['bgTresh']=50
                settingsCon['minSpeed']=1
                settingsCon['maxSpeed']=10
                settingsCon['minFreq']=40
                settingsCon['maxFreq']=500
                settingsCon['audioRate']=10
                settingsCon['positionBuff']=5

 
def SaveProperties():
        try:
            f = open("settings.txt")
            var = f.readlines()
            f.close()
            var[5]=str(settingsCon['minArea'])+'\n'
            var[6]=str(settingsCon['maxArea'])+'\n'
            var[7]=str(settingsCon['bgHistory'])+'\n'
            var[8]=str(settingsCon['bgTresh'])+'\n'
            var[9]=str(settingsCon['minSpeed'])+'\n'
            var[10]=str(settingsCon['maxSpeed'])+'\n'
            var[11]=str(settingsCon['minFreq'])+'\n'
            var[12]=str(settingsCon['maxFreq'])+'\n'
            var[13]=str(settingsCon['audioRate'])+'\n'
            var[14]=str(settingsCon['positionBuff'])+'\n'
            print "Save complete!"
            f = open("settings.txt", "w")
            f.writelines(var)
            f.close()
            print "Save complete!"
            print settingsCon['minSpeed']
            print settingsCon['maxSpeed']
        except:
            print "Save not complete!" 





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
                         if settingsCon['newdata']:
                                 flag, frame=vidFile.read()
                                 #print "Image queued"
                                 if(None==settingsCon['ccam']):
                                   (h,w,c)= frame.shape
                                   camSet=camProperties()
                                   settingsCon['ccam']=projection.cammera(w,h,camSet[0],camSet[1])
                                   settingsCon['ccam'].set_position(camSet[2], camSet[3])
                         
                         if flag==0:
                            print "\nflag kill this thread\n"
                            break
                         #cv2.imshow("Input file", frame)
                         queue.put(frame)
                         cv2.waitKey(20)
                       
                        
                      except:
                         print "continue"
                         continue
        vidFile.release()
        print "Gotov je tred ovo nije problem"        

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
   Properties()
   print "Singleton initialised" 
   source =  0  
   global runTk
   runTk = 1
   queue = Queue.Queue(maxsize=5)
   global var1
   var1=2  
   settingsCon['ccam']=None
   settingsCon['banner']='   Program created by Slobodan: slobacartoonac@hotmail.com and Marko: markoni985@hotmail.com'   
   settingsCon['mute'] = 0
   settingsCon['freq'] = ''
   settingsCon['xy'] = ''
   settingsCon['newdata']=0
   settingsCon['bgHistoryOld']=-1
   settingsCon['bgTreshOld']=-1
   print settingsCon['minArea']
   print settingsCon['maxArea']
   print settingsCon['bgHistory']
   print settingsCon['bgTresh']
 
   settingsCon['oldTime']=time.time()
   p = threading.Thread(target=image_capture,args=(queue, runTk, source))
   p.start()


   app = MyApp(0)
   app.MainLoop()
   
   print 'mainloop exit'
   runTk=0
   quit_(p)
   p.join()
   print 'image capture process exit'

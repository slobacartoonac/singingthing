from Tkinter import *
import Tkinter as tk
import time
import ttk
import settingsWindow
import os




if __name__ == '__main__': 
   root = tk.Tk()
   root.title('SingThing')
   var1 = IntVar()

   def runImg():

       os.system("console.py %d %d %d %d %d %d %d %d %d %d %d"%(var1.get(),minAreaSk.get(),maxArea.get(),\
                                  bgHistory.get(),bgTresh.get(),minSpeed.get(),maxSpeed.get(),\
                                  minFreq.get(),maxFreq.get(),audioRate.get(), positionBuff.get()))
   
   def bannerF():
       text = banner.get()
       text = text[1:] + text [0]
       banner.set(text)
       root.after(150, bannerF)
   
   def setValues():
       try:
           f=open("settings.txt")
           settings=f.readlines()
           f.close()
           var1.set(settings[4][:-1])
           minArea.set(settings[5][:-1])
           maxArea.set(settings[6][:-1])
           bgHistory.set(settings[7][:-1])
           bgTresh.set(settings[8][:-1])
           minSpeed.set(settings[9][:-1])
           maxSpeed.set(settings[10][:-1])
           minFreq.set(settings[11][:-1])
           maxFreq.set(settings[12][:-1])
           audioRate.set(settings[13][:-1])
           newdata.set(0)
           mute.set(0)
           #newdata.set(settings[15][:-1])
           print 'settings loaded'
       except:   
           var1.set('2')
           minArea.set('1000')
           maxArea.set('5000')
           bgHistory.set('10')
           bgTresh.set('50')
           bgHistoryOld=-1
           bgTreshOld=-1
           minSpeed.set('1')
           maxSpeed.set('10')
           minFreq.set('40')
           maxFreq.set('500')
           audioRate.set('10')
           positionBuff.set('5')
           newdata.set(0)
           mute.set(0)
           
           print 'default values set'
   def save():
       
       try:
           f = open("settings.txt")
           setdata = f.readlines()
           f.close()
           global mod1Btn
           print 'fclose'
           print var1.get()
           setdata[4]= str(var1.get())+'\n'
           print 'test'
           setdata[5]=str(minAreaSk.get())+'\n'
           print 'test'
           setdata[6]=str(maxAreaSk.get())+'\n'
           print 'test'
           setdata[7]=str(history.get())+'\n'
           print 'test'
           setdata[8]=str(Threshold.get())+'\n'
           print 'test'
           setdata[9]=str(minSpeedSk.get())+'\n'
           print 'test'
           setdata[10]=str(maxSpeedSk.get())+'\n'
           print 'test'
           setdata[11]=str(minFreqSk.get())+'\n'
           print 'test'
           setdata[12]=str(maxFreqSk.get())+'\n'
           print 'test'
           setdata[13]=str(audioRateSk.get())+'\n'
           print 'test'
           setdata[14]=str(positionBuffSk.get())+'\n'
           
           
           print 'data gaddered'
           f = open("settings.txt", "w")
           f.writelines(setdata)
           f.close()
           #print newdata.get()
        
       except:
           print 'data save failed'
      
       root.destroy()

   def ende():
       save()
       #root.destory()


   banner = StringVar()
   banner.set('   Program created by Slobodan: slobacartoonac@hotmail.com and Marko: markoni985@hotmail.com')

   
   mute = IntVar()
   minArea = IntVar()
   maxArea = IntVar()
   bgHistory = IntVar()
   bgTresh = IntVar()
   freq = StringVar()
   xy = StringVar()
   minSpeed = IntVar()
   maxSpeed = IntVar()
   minFreq = IntVar()
   maxFreq = IntVar()
   audioRate = IntVar()
   positionBuff = IntVar()
   newdata=IntVar()
       
   oldTime=time.time()
   frame2= Frame(root, height=500, width=500)
   frame2.grid(row=0, column=1)
   # Controll buttons
   tk.Button(frame2, text='CAPTURE', command=lambda: runImg(), height=5, width=20).grid(row=0, column=0)
   #tk.Button(frame2, text='DEBUG  ', command=lambda: debugMode(), height=5, width=20).grid(row=1, column=0, sticky = N)
   tk.Button(frame2, text='QUIT   ', command=lambda: save(), height=5, width=20).grid(row=1, column=0, sticky = N)
   # Mode buttons
   mod1Btn=Radiobutton(frame2, text="Mode 1", variable=var1, value=1, indicatoron = 0,width = 14,padx = 20,).grid(row=2, column=0,sticky=N)#, sticky=W)  
   Radiobutton(frame2, text="Mode 2", variable=var1, value=2, indicatoron = 0,width = 14,padx = 20,).grid(row=3, column=0,sticky=N)#, sticky=W)
   Radiobutton(frame2, text="Mode 3", variable=var1, value=3, indicatoron = 0,width = 14,padx = 20,).grid(row=4, column=0,sticky=N)#, sticky=W)
   Radiobutton(frame2, text="Mode 4", variable=var1, value=4, indicatoron = 0,width = 14,padx = 20,).grid(row=5, column=0,sticky=N)#, sticky=W)
   # Volume
   #tk.Checkbutton(frame2, text="Mute", variable=mute,indicatoron = 0).grid(column=0, row=8, sticky=('W', 'E'))
   #pBtn=tk.Checkbutton(frame2, text="Play", variable=newdata,indicatoron = 0).grid(column=0, row=9, sticky=('W', 'E'))

   tk.Button(frame2, text='CONFIGURE   ', command=lambda: settingsWindow.settingsWindow(), height=2, width=20).grid(row=10, column=0, sticky = N)

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
   minAreaSk = Scale(f1, from_=5000, to=0,variable=minArea,length=400)
   minAreaSk.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   maxAreaSk = Scale(f1, from_=15000, to=0,variable=maxArea,length=400)
   maxAreaSk.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   history = Scale(f1, from_=300, to=0,variable=bgHistory,length=400)
   history.grid(column=2, row=1,rowspan =9, sticky=('S', 'N'))
   Threshold = Scale(f1, from_=1000, to=0,variable=bgTresh,length=400)
   Threshold.grid(column=3, row=1,rowspan =9, sticky=('S', 'N'))
   tk.Label(f2, text="Min Speed").grid(column=0, row=0)
   tk.Label(f2, text="Max speed").grid(column=1, row=0)
   tk.Label(f2, text="Min Freq").grid(column=2, row=0)
   tk.Label(f2, text="Max Freq").grid(column=3, row=0)
   tk.Label(f3, text="Audio Rate").grid(column=0, row=0)
   tk.Label(f3, text="Buffer").grid(column=1, row=0)
   minSpeedSk = Scale(f2, from_=10, to=0,variable=minSpeed,length=400)
   minSpeedSk.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   maxSpeedSk = Scale(f2, from_=20, to=5,variable=maxSpeed,length=400)
   maxSpeedSk.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   minFreqSk = Scale(f2, from_=2000, to=40,variable=minFreq,length=400)
   minFreqSk.grid(column=2, row=1,rowspan =9, sticky=('S', 'N'))
   maxFreqSk = Scale(f2, from_=2000, to=40,variable=maxFreq,length=400)
   maxFreqSk.grid(column=3, row=1,rowspan =9, sticky=('S', 'N'))
   audioRateSk = Scale(f3, from_=30, to=1,variable=audioRate,length=400)
   audioRateSk.grid(column=0, row=1,rowspan =9, sticky=('S', 'N'))
   positionBuffSk = Scale(f3, from_=10, to=3,variable=positionBuff,length=400)
   positionBuffSk.grid(column=1, row=1,rowspan =9, sticky=('S', 'N'))
   creators = tk.Label(root, textvariable=banner, width= 30, justify=LEFT)#, wraplength=200)
   creators.grid(column = 2, row=1 , sticky=E)


   setValues()
   print 'GUI image label initialized...'
   print 'image capture process has started...'
   root.after(150, bannerF)
   root.mainloop()
   print 'mainloop exit'
   print 'image capture process exit'

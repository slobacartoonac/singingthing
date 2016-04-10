#import Tkinter as tk
import time
#import threading
import thread
import Queue
import sys
import math
#sys.path.append("sound1")
import tocall
#sys.path.append("geometry")
from projection import cammera
import walkerModul

#
last=time.time()
lastp=None
playing=None
que=Queue.Queue()
buf=[]
cam=None
ycord=None

w=None

wStime=0;

def distance(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

def updateSound(dist,difference,settingsP):
    
        
    global playing
    if not playing:
        print "created thread"
        try:
            playing=thread.start_new_thread(tocall.start_sin,(que,))
        except:
            mrk=True
    f=0;
    speed= dist/difference
    
    if(speed>settingsP[0]):
        f=settingsP[2]
        f+=(settingsP[3]-settingsP[2])/(settingsP[1]-settingsP[0])*(speed-settingsP[0])
    #print "speed: ",speed,"->f: ",f
    if(f<20): f=0
    if(f>settingsP[3]): f=settingsP[3]
    #print "set F: "+str(f)
    if settingsP[6]==1:
        que.put(0)
    else:
        que.put(f)
        #print "speed "+str(speed)+" -> "+str(f)+"f"
    return f

def updateMotion(inn,settingsP):
        #print "updateMotion"
        #print inn,' ',inn[2]!=-1
        global w
        if not w:
            #(self,ratio,tStarve,lenBuff,tBuff,rStand)
            w=walkerModul.Walkers(10,2,5,1,1)
            
        middle=False
        if not (inn[2]==-1 or (inn[0]==0 and inn[1]==0)):
            #print "naso"
            w.doDots((inn[0],inn[1]),time.time())
        #print "update"
        dist=w.getSpeed(time.time())
        w.draw()
        res=updateSound(dist,1,settingsP)
        
        return res
def updateMotion2(inn,settingsP):
        #print "updateMotion"
        #print inn,' ',inn[2]!=-1
        middle=False
        if(inn[2]!=-1):
            #print "regular: ",inn
            buf.append(inn)
        else:
            middle=True
        while len(buf)>settingsP[5]:
            buf.pop(0)
        if(len(buf)<2):
            return 0
        s1l=0
        s1r=0
        time=0
        for i in buf:
            s1l+=i[0]
            s1r+=i[1]
            time+=i[2]
        time=float(time/len(buf))
        #print "averafe time: ",time
        #print "time: ",time," ",len(buf)
        last=len(buf)-1
        #print "a"
        #print buf
        ts2=((s1l-buf[0][0])/last,(s1r-buf[0][1])/last)
        
        #print "b"
        ts1=((s1l - buf[last][0])/last ,(s1r - buf[last][1])/last)
        #print "c ", s1,s2
        dist=distance(ts1,ts2)
        res=updateSound(dist,time,settingsP)
        if middle:
            #print "utisavam"
            buf.append((ts2[0],ts2[1],time*2));
            #print "utisao"
            #print "distance/time/f: ",dist, time,res
        #print "d"
        
        
        return res
    
def motionE(event):
    x, y = event.x, event.y
    global last,lastp
    if(time.time()-last)>0.1:
        #print('{}, {}'.format(x, y))
        diffrence=time.time()-last
        last=time.time()
        if x==0 and y==0:
            #print "nothing"
            updateMotion((0,0,-1))
            return
        ny=cam.get_distance_pixel(ycord-y)
        nx=cam.get_cord_pixel(ny,x)
        #print('{}, {}'.format(int(nx), int(ny)))
        updateMotion((nx,ny,diffrence),(0.5,10.0,50.0,200.0,10,5,0))
def motion(event,cam,settingsP):
    #print "usaoUmoution"
    x, y = event[0],event[1]
    global last,lastp
    if(time.time()-last)>(1.0/settingsP[4]):
        #print('{}, {}'.format(x, y))
        diffrence=time.time()-last
        last=time.time()
        if lastp!=None:
            event=lastp
            lastp=None
        if event==(0,0):
            #print "nista nista nista"
            return (0,0,updateMotion((0,0,-1),settingsP))
        #print "pre"
        ny=cam.get_distance_pixel(cam.res_y-y)
        #print "posle"
        nx=cam.get_cord_pixel(ny,x)
        #print('{}, {}'.format(int(nx), int(ny)))
        return (nx,ny,updateMotion((nx,ny,diffrence),settingsP))
    else:
        if(event!=(0,0)):
            lastp=event
        
def end():
    que.put(-1)
#planer=threading.Thread(target=updateMotion, args = (quein,))
#planer.start()
if __name__=='__main__':
    root = tk.Tk()
    photo = tk.PhotoImage(file="prvi.gif")
    ycord=photo.height()
    cam=cammera(photo.width(),photo.height(),math.pi/4,math.pi/5)
    cam.set_position(21.0,31.0)
    label = tk.Label(root,image=photo)
    label.image = photo # keep a reference!
    label.pack()
    label.bind('<Motion>', motionE)
    root.mainloop()
    end()
    playing.join()
#planer.join()

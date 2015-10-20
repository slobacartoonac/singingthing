import Tkinter as tk
from Tkinter import *
import math
import singleton
import math
sys.path.append("sound")
import projection


frame=None


msg = None
lb1 = None
lb2 = None
lb3 = None
lb4 = None
#lb5 = Label(frame, text="nesto")
#lb6 = Label(frame, text="nesto")
#lb7 = Label(frame, text="nesto")
#lb8 = Label(frame, text="nesto") 
e1 = None
e2 = None
e3 = None
e4 = None
#e5 = Entry(frame)
#e6 = Entry(frame)
#e7 = Entry(frame)
#e8 = Entry(frame)
button = None
button2 = None
entry1= None
def validate_float(var):
    new_value = var.get()
    try:
        new_value == '' or float(new_value)
        old_value = new_value
    except:
        var.set('0')

def isFloat(var):
    new_value = var.get()
    try:
        new_value == float(new_value)
        return True
    except:
        return False



def settingsWindow():
        global e1, e2, e3, e4, warning            
        top = Toplevel( )#height=300, width=400)
        top.title("Settings")
        #top.geometry("%dx%d%+d%+d" % (310, 210, 250, 125))
        frame= tk.Frame(top)
        frame.grid()
        warning = StringVar()
        entry1 = StringVar()
        entry2 = StringVar()
        entry3 = StringVar()
        entry4 = StringVar()
        e1 = Entry(frame, textvariable=entry1)
        e2 = Entry(frame, textvariable=entry2)
        e3 = Entry(frame, textvariable=entry3)
        e4 = Entry(frame, textvariable=entry4)
        try:
                f=open("settings.txt")
                print 'file opened'
                var=f.readlines()
                print 'lines read'
                entry1.set(var[0][:-1])
                print 'var added'
                entry2.set(var[1][:-1])
                entry3.set(var[2][:-1])
                entry4.set(var[3][:-1])
                print 'close'
                f.close()
        except:
                print 'Problem opening file.'
                entry1.set('0')
                entry2.set('0')
                entry3.set('0')
                entry4.set('0')
        
        msg = Label(frame, text="Enter Settings")
        war = Label(frame, textvariable=warning)
        lb1 = Label(frame, text="Field of view x")
        lb2 = Label(frame, text="Field of view y")
        lb3 = Label(frame, text="Height of camera")
        lb4 = Label(frame, text="Distance of camera")
        #lb5 = Label(frame, text="nesto")
        #lb6 = Label(frame, text="nesto")
        #lb7 = Label(frame, text="nesto")
        #lb8 = Label(frame, text="nesto")
        


        entry1.trace('w', lambda nm, idx, mode, var=entry1: validate_float(entry1))
        entry2.trace('w', lambda nm, idx, mode, var=entry2: validate_float(entry2))
        entry3.trace('w', lambda nm, idx, mode, var=entry3: validate_float(entry3))
        entry4.trace('w', lambda nm, idx, mode, var=entry4: validate_float(entry4))
        #e5 = Entry(frame)
        #e6 = Entry(frame)
        #e7 = Entry(frame)
        #e8 = Entry(frame)
        button = Button(frame, text="Save", command=lambda: close(top))
        #button2 = Button(frame, text="Save", command=save)
        
        msg.grid(row=0, column=0,columnspan=2, sticky=(W,E) )
        war.grid(row=1, column=0,columnspan=2, sticky=(W,E) )
        lb1.grid(row=2, column=0, sticky = W)
        lb2.grid(row=3, column=0, sticky = W)
        lb3.grid(row=4, column=0, sticky = W)
        lb4.grid(row=5, column=0, sticky = W)
        #lb5.grid(row=5, column=0)
        #lb6.grid(row=6, column=0)
        #lb7.grid(row=7, column=0)
        #lb8.grid(row=8, column=0)
        e1.grid(row=2, column=1)
        e2.grid(row=3, column=1)
        e3.grid(row=4, column=1)
        e4.grid(row=5, column=1)
        #e5.grid(row=5, column=1)
        #e6.grid(row=6, column=1)
        #e7.grid(row=7, column=1)
        #e8.grid(row=8, column=1)
        button.grid(row=6, column=0,columnspan=2,sticky=(W, E))
        #button2.grid(row=7, column=0,columnspan=2,sticky=(W, E))
def close(target):
    if isFloat(e1):
        if isFloat(e2):
            if isFloat(e3):
                if isFloat(e4):
                    save()
                    target.destroy()
                    
    else:
        warning.set("Populate fields!")
        print 'Populate fields.'
        

def save():
        settingsCon=singleton.settings()
        f = open("settings.txt", "w")
        f.write(e1.get()+'\n'+e2.get()+'\n'+e3.get()+'\n'+e4.get()+'\n')
        
        f.close()
        x=float(e1.get())*math.pi/180
        y=float(e2.get())*math.pi/180
        hc=float(e3.get())
        dc=float(e4.get())
        settingsCon['ccam'].set_fov(x,y)
        settingsCon['ccam'].set_position(hc, dc)
    
        
        print 'close ', x, y, hc, dc
        f.close()
if '__main__'==__name__:
        root = tk.Tk()
        settingsCon=singleton.settings()
        settingsWindow()
        camSet=(1,1,1,1)
        settingsCon['ccam']=projection.cammera(200,200,camSet[0],camSet[1])
        settingsCon['ccam'].set_position(camSet[2], camSet[3])
        root.mainloop()
        root.destroy()
        

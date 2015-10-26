import pyaudio
import wave
import sys
import math
import time
import equalsound
import thread
import Queue



def start_sin(q):
    p = pyaudio.PyAudio()


    CHUNK = 1024
    BITRATE =16000*2
    FREQUENCY =700.0;
    ramping=210;

    stream = p.open(format=p.get_format_from_width(1),
                    channels=1,
                    rate=BITRATE,
                    output=True)
    print 2*math.pi
    data='1'
    x=0;
    y=0;
    yp=0;
    dividor=BITRATE/FREQUENCY/math.pi
    pom=BITRATE/(FREQUENCY+1)/math.pi
    pom-=dividor
    pi2=2*math.pi;
    print dividor
    mind=CHUNK*2;
    maxd=CHUNK;
    pos=0;
    state=0;
    mulup=127.0/CHUNK
    while data != '':
        data='';
        diference=(y-yp)/CHUNK/4
        if state==1:
            if diference>0:
                #normal riseing
                for x in xrange(CHUNK):
                    yp+=diference
                    dividor=1.0/BITRATE*(yp)*math.pi
                    pos+=dividor;
                    data = data+chr(int(math.sin(pos)*127.0+128))
            else:
                #normal faling
                if (yp+CHUNK*diference)<40:
                    #normal end of sound
                        diference=(40-yp)/CHUNK
                        for x in xrange(CHUNK):
                            yp+=diference
                            dividor=1.0/BITRATE*(yp)*math.pi
                            pos+=dividor;
                            data = data+chr(int(math.sin(pos)*mulup*(CHUNK-x)+128))
                        state=0
                        yp=40
                else:
                    #normal just falling
                    for x in xrange(CHUNK):
                        yp+=diference
                        dividor=1.0/BITRATE*(yp)*math.pi
                        pos+=dividor;
                        data = data+chr(int(math.sin(pos)*127.0+128))
        else:
            if y>39:
                #normal starting
                yp=40
                for x in xrange(CHUNK):
                    yp+=diference
                    dividor=1.0/BITRATE*(yp)*math.pi
                    pos+=dividor;
                    data = data+chr(int(math.sin(pos)*mulup*(x)+128))
                state=1
            else:
                #normal no sound
                dividor=1.0/BITRATE*(5)*math.pi 
                for x in xrange(CHUNK):
                    pos+=dividor;
                    #data = data+chr(int(''';math.sin(pos)*0.5+'''128))
                    data = data+chr(128)
                
        #print diference
        #if x>maxd: maxd=x;
        #if x<mind: mind=x;
        #y+=0.3;
        stream.write(data)
        try:
            pom=q.get_nowait()
            y=pom;

        except:
            y=y
        if(y<0):
                    break;
            


    print "end of sound" 

    stream.stop_stream()
    stream.close()

    p.terminate()
if __name__=='__main__':
    que=Queue.Queue()
    thread.start_new_thread(start_sin,(que,))
    que.put(400)
    time.sleep(2)
    que.put(800)
    time.sleep(2)
    que.put(-1)

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


    CHUNK = 1024*2
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
    while data != '':
        data='';
        soundlevel=equalsound.eqlevel(yp,70)#/150*127
        if(soundlevel>127):soundlevel=127
        for x in xrange(CHUNK):
            diference=(y-yp)/CHUNK/4
            yp+=diference
            dividor=1.0/BITRATE*(yp)*math.pi
            pos+=dividor;
            data = data+chr(int(math.sin(pos)*soundlevel+128))
        #print diference
        if x>maxd: maxd=x;
        if x<mind: mind=x;
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
    que.put(40)
    time.sleep(2)
    que.put(80)
    time.sleep(2)
    que.put(-1)

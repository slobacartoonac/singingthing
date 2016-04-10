import pygame
import math
import random




# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def show_text(screen,msg,color,x,y):
    myfont = pygame.font.SysFont("monospace", 20)
    text = myfont.render(str(msg), 1, color)
    textpos = (x,y)
    screen.blit(text,textpos)

def distance(a,b):
    return math.sqrt((a[0]-b[0])*(a[0]-b[0])+(a[1]-b[1])*(a[1]-b[1]))

class Walkers:

    def __init__(self,ratio,tStarve,lenBuff,tBuff,rStand):
        self.dots=[]
        self.ratio=ratio
        self.tStarve=tStarve
        self.lenBuff=lenBuff
        self.tBuff=tBuff
        self.rStand=rStand
        pygame.init()
        size = [640, 480]
        self.screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
        pygame.display.set_caption("Graphics")
        for event in pygame.event.get(): have_to_do_this=True
        self.reck=[0,0,0,0]
        
    class Walker:
        def __init__(self,pos,tStamp,ratio,tStarve,lenBuff,tBuff,rStand,reck):
            self.postion=(pos[0],pos[1])
            self.toGo=(pos[0],pos[1])
            self.speed=(0,0)
            self.lspeed=(0,0)
            self.stop=0;
            self.places=[];
            self.lPlaceT=tStamp
            self.lMove=tStamp
            #settings
            self.ratio=ratio
            self.tStarve=tStarve
            self.lenBuff=lenBuff
            self.tBuff=tBuff
            self.rStand=rStand
            self.reck=reck
            
        def move(self,tStamp):
            lp=len(self.places)
            toGoX=0;
            toGoY=0;
            toTal=0;
            for i in xrange(lp):
                tmp=self.places.pop(0)
                if tmp[2]>0 and i<self.lenBuff:
                    self.places.append((tmp[0],tmp[1],tmp[2]-tStamp+self.lMove,tmp[3]))
                    toGoX+=tmp[0]*tmp[3];
                    toGoY+=tmp[1]*tmp[3];
                    toTal+=tmp[3];
            
            lp=len(self.places)
            if lp>0: self.toGo=(toGoX/toTal,toGoY/toTal)
            if(lp>1 and tStamp-self.lPlaceT<1):
                self.lspeed=self.speed=(
                                        self.speed[0]+(self.toGo[0]-(self.postion[0]+self.speed[0]*0.3))*(tStamp-self.lMove)*20,
                                        self.speed[1]+(self.toGo[1]-(self.postion[1]+self.speed[1]*0.3))*(tStamp-self.lMove)*20)
                self.stop=1;
            else:
                if self.stop>0:
                    self.stop-=tStamp-self.lMove;
                    self.speed=(self.lspeed[0]*self.stop,self.lspeed[1]*self.stop)
                else:
                    self.speed=(0,0)
            tmp2=self.postion;
            self.postion=(tmp2[0]+self.speed[0]*(tStamp-self.lMove),tmp2[1]+self.speed[1]*(tStamp-self.lMove));
            self.toGo=(self.toGo[0]+self.speed[0]*(tStamp-self.lMove),self.toGo[1]+self.speed[1]*(tStamp-self.lMove))
            self.lMove=tStamp

            
            
            return distance((0,0),self.speed)
            #self.speed=(self.speed[0]*0.8,self.speed[1]*0.8)
        def addPlace(self,place,tStamp):
            if distance(self.toGo,place)<self.rStand+distance((0,0),self.speed)*2:
                    self.places.insert(0,(place[0],place[1],self.tBuff,min(tStamp-self.lPlaceT,1)));
                    self.lPlaceT=tStamp
                    return True;
            for pl in self.places:
                if distance(pl,place)<self.rStand+distance((0,0),self.speed)*2:
                    self.places.insert(0,(place[0],place[1],self.tBuff,min(tStamp-self.lPlaceT,1)));
                    self.lPlaceT=tStamp
                    return True;
            return False;
        def draw(self,screen):
            
            if(self.reck==[0,0,0,0]):self.reck=[
                self.postion[0]-self.rStand,
                self.postion[0]+self.rStand,
                self.postion[1]-self.rStand,
                self.postion[1]+self.rStand]
            if(self.reck[0]>self.postion[0]-self.rStand): self.reck[0]=self.postion[0]-self.rStand#left
            if(self.reck[2]<self.postion[0]+self.rStand): self.reck[2]=self.postion[0]+self.rStand#right
            if(self.reck[1]>self.postion[1]-self.rStand): self.reck[1]=self.postion[1]-self.rStand#up
            if(self.reck[3]<self.postion[1]+self.rStand): self.reck[3]=self.postion[1]+self.rStand#down
            ratio=min(
                640.0/(self.reck[2]-self.reck[0]),
                480.0/(self.reck[3]-self.reck[1])
                )
            for pl in self.places:
                pygame.draw.circle(screen, BLUE, [int((pl[0]-self.reck[0])*ratio), int((pl[1]-self.reck[1])*ratio)],
                                   int(distance((0,0),self.speed)*ratio+self.rStand*ratio))
                pygame.draw.circle(screen, (64,64,255), [int((pl[0]-self.reck[0])*ratio),
                                                         int((pl[1]-self.reck[1])*ratio)],
                                                           int(distance((0,0),self.speed)*ratio))
            pygame.draw.circle(screen, RED, [int(self.postion[0]*ratio-self.reck[0]*ratio)
                                             ,int(self.postion[1]*ratio-self.reck[1]*ratio)], 15)
            return self.reck
        def toDestroy(self,tStamp):
            if tStamp-self.lPlaceT>self.tStarve: return True
            else: return False

    def doDots(self,pos,tStamp):
        newT=True
        for D in self.dots:
            if newT:
                if D.addPlace(pos,tStamp):
                    newT=False
        if newT: self.dots.insert(0,Walkers.Walker(pos,tStamp,
                                                self.ratio,
                                                self.tStarve,
                                                self.lenBuff,
                                                self.tBuff,
                                                self.rStand,
                                                self.reck));
    def getSpeed(self,tStamp):
        maxs=0
        for D in self.dots:
            sp=D.move(tStamp)
            if sp>maxs: maxs=sp
        ld=len(self.dots)
        for i in xrange(ld):
            dot=self.dots.pop(0);
            if not dot.toDestroy(tStamp): self.dots.append(dot)
        return maxs;
    def draw(self):
        
        for event in pygame.event.get(): have_to_do_this=True
        self.screen.fill(WHITE)
        for D in self.dots:
            rec=D.draw(self.screen)
            if(self.reck==[0,0,0,0]): self.reck=list(rec)
            if(self.reck[0]>rec[0]): self.reck[0]=rec[0]#left
            if(self.reck[2]<rec[2]): self.reck[2]=rec[2]#right
            if(self.reck[1]>rec[1]): self.reck[1]=rec[1]#up
            if(self.reck[3]<rec[3]): self.reck[3]=rec[3]#down
            
        pygame.display.flip()
        
#use it like this        
#w=Walkers(1,3,5,1,40)
#repeat
#   (on pos)w.doDots(pos,tStamp)
#   w.getSpeed(tStamp)
#    w.draw()

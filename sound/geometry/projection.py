import math

class cammera:
    def __init__(self,x,y,fov_x,fov_y):
        self.fov_x,self.fov_y=fov_x,fov_y
        self.res_x,self.res_y=x,y
        self.height=10
        #distance of bootmom viewing feeld from camera projecton on surface
        self.bottom_distance=10
        self.bottom_angle=math.atan(self.bottom_distance/self.height)
        #print self.bottom_angle
    def set_height(self,height):
        self.height=float(height)
        self.bottom_angle=math.atan(self.bottom_distance/self.height)
    def set_bottom_distance(self,distance):
        self.bottom_distance=float(distance)
        self.bottom_angle=math.atan(self.bottom_distance/self.height)
    def set_position(self,height,distance):
        self.height=float(height)
        self.bottom_distance=float(distance)
        self.bottom_angle=math.atan(self.bottom_distance/self.height)
    def set_fov(self,fovx,fovy):
        self.fov_x,self.fov_y=fovx,fovy
    def get_distance_radian(self,radian):
        res=math.tan(radian)*self.height
        #print "y cord: ",res
        return res
    def get_distance_pixel(self,pixel):
        #convert pixel to angle
        radian=self.bottom_angle+(pixel*1.0/self.res_y*self.fov_y)
        if(radian<math.pi/2):
            return self.get_distance_radian(radian)
        else:
            #print "not in plane"
            return 0
    def get_cord_radian(self,distance,radian):
        res=math.tan(radian)*math.sqrt(distance*distance+self.height*self.height)
        #print "x cord: ",res
        return res
    def get_cord_pixel(self,distance,pixelx):
        radian= ((pixelx-self.res_x/2)*1.0/self.res_x)*self.fov_x
        #print "angle: ",radian
        return self.get_cord_radian(distance,radian)
if __name__=='__main__':
    cam=cammera(640,480,math.pi/4,math.pi/5)
    cam.set_position(10,10);
    a=cam.get_distance_pixel(1)
    b=cam.get_distance_pixel(480)
    print cam.get_cord_pixel(a,0)
    print cam.get_cord_pixel(a,640)
    print cam.get_cord_pixel(b,0)
    print cam.get_cord_pixel(b,640)
        

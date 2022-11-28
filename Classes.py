import numpy as np

class Sphere:
    def __init__(self,name,pos_x,pos_y,pos_z,scl_x,scl_y,scl_z,r,g,b,ka,kd,ks,kr,n):
        self.name = name 
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.scl_x = scl_x
        self.scl_y = scl_y
        self.scl_z = scl_z 
        self.r = r
        self.g = g
        self.b = b
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.kr = kr
        self.n = n
        self.radius = 1 
    
    def get_normal(self, point):
        return np.vstack([point[0] - self.pos_x, point[1] - self.pos_y, point[2] - self.pos_z])

class Light:
    def __init__(self,name,pos_x,pos_y,pos_z,lr,lg,lb):
        self.name = name 
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.lr = lr
        self.lg = lg
        self.lb = lb 
        
class Ambient:
    def __init__(self,lr,lg,lb):
        self.lr = lr
        self.lg = lg
        self.lb = lb 
        
class Color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b 
        
class Res:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
class Ray:
    def __init__(self,start_point,direction):
        self.start_point = start_point
        self.dir = direction
        self.depth = 1
    
    def set_depth(depth):
        self.depth = depth   
    
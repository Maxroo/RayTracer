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
        self.model_view_matrix = np.array([[self.scl_x,0,0,self.pos_x],
                                            [0,self.scl_y,0,self.pos_y],
                                            [0,0,self.scl_z,self.pos_z],
                                            [0,0,0,1]])
        self.model_inverse_matrix = np.linalg.inv(self.model_view_matrix)
        
        
    def get_normal(self, model_inverse_matrix, point):
        homo_point = np.vstack([point[0], point[1],point[2], 0])
        model_inverse_transpose_matrix = np.transpose(model_inverse_matrix)
        homo_point = homo_point / np.linalg.norm(homo_point)
        
        # print(homo_point)
        # print(homo_point)
        # model_inverse_transpose_matrix = model_inverse_transpose_matrix / np.linalg.norm(model_inverse_transpose_matrix)
        result = model_inverse_transpose_matrix @ homo_point
        # result = result / np.linalg.norm(result)
        return result
    
    

class Light:
    def __init__(self,name,pos_x,pos_y,pos_z,lr,lg,lb):
        self.name = name 
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z
        self.lr = lr
        self.lg = lg
        self.lb = lb 
        
        
class Color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b
    
    def __mul__(self, other):
        if (isinstance(other, float)):
            return Color(np.clip(self.r * other, 0, 1), np.clip(self.g * other, 0, 1), np.clip(self.b * other, 0, 1))
        else:
            return Color(np.clip(self.r * other.r , 0, 1), np.clip(self.g * other.g , 0, 1), np.clip(self.b * other.b , 0, 1))
        
    def __add__(self, other):
        if (isinstance(other, float)):
            return Color(np.clip(self.r + other, 0, 1), np.clip(self.g + other, 0, 1), np.clip(self.b + other, 0, 1))
        else:
            return Color(np.clip(self.r + other.r , 0, 1), np.clip(self.g + other.g , 0, 1), np.clip(self.b + other.b , 0, 1))
        
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
    
import numpy as np
        
class Ray:
    def __init__(self,start_point,direction):
        self.start_point = start_point
        self.dir = direction
        self.depth = 1
    
    def set_depth(self, depth):
        self.depth = depth   
    
import sys;

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
        
class Back_color:
    def __init__(self,r,g,b):
        self.r = r
        self.g = g
        self.b = b 
        
class Res:
    def __init__(self,x,y):
        self.x = x
        self.y = y


near = 0.0
left = 0.0
right = 0.0
bottom = 0.0
top = 0.0
res = Res(0,0)
spheres = []
lights = []
back_color = Back_color(0,0,0)
ambient = Ambient(0,0,0)
output = ''

#read value and phrasing them into the value
def read_file(arg):
    global near,left,right,bottom,top,res,spheres,lights,back_color,ambient,output
    f = open(arg, "r")
    for lines in f:
        line = lines.split()
        if(len(line) != 0):
            if(line[0] == 'OUTPUT'):
                output = line[1]
            elif(line[0] == 'LEFT'):
                left = float(line[1]) 
            elif(line[0] == 'RIGHT'):
                right = float(line[1]) 
            elif(line[0] == 'BOTTOM'):
                bottom = float(line[1]) 
            elif(line[0] == 'TOP'):
                top = float(line[1]) 
            elif(line[0] == 'NEAR'):
                near = float(line[1]) 
            elif(line[0] == 'AMBIENT'):
                ambient = Ambient(float(line[1]) , float(line[2]) , float(line[3]))
            elif(line[0] == 'BACK'):
                back_color = Back_color(float(line[1]) , float(line[2]) , float(line[3]))
            elif(line[0] == 'RES'):
                res = Res(int(line[1]) , int(line[2]))
            elif(line[0] == 'LIGHT'):
                lights.append(Light(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7])))
            elif(line[0] == 'SPHERE'):
                spheres.append(Sphere(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7]),
                                    float(line[8]),float(line[9]),float(line[10]),float(line[11]),float(line[12]),float(line[13]),float(line[14]),
                                    int(line[15])))

read_file(sys.argv[1])
print(near)
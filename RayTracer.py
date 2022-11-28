import Output
import sys 
import numpy as np

from Classes import *

#values 
near = 0.0
left = 0.0
right = 0.0
bottom = 0.0
top = 0.0
res = Res(0,0)
spheres = []
lights = []
back_color = Color(0,0,0)
ambient = Ambient(0,0,0)
output = ''
up = np.array([0,1,0,1])
final_color = []
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
                back_color = Color(float(line[1]) , float(line[2]) , float(line[3]))
            elif(line[0] == 'RES'):
                res = Res(int(line[1]) , int(line[2]))
            elif(line[0] == 'LIGHT'):
                lights.append(Light(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7])))
            elif(line[0] == 'SPHERE'):
                spheres.append(Sphere(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7]),
                                    float(line[8]),float(line[9]),float(line[10]),float(line[11]),float(line[12]),float(line[13]),float(line[14]),
                                    int(line[15])))
    f.close()

read_file(sys.argv[1])

# image = np.zeros([2*right,2*top,res.x,res.y])
eye = np.array([0,0,0])
u = np.array([1,0,0])
v = np.array([0,1,0])
n = np.array([0,0,1])
camera = np.column_stack((eye,u,v,n))

uc = -right + right*2*(225)/res.x
vr  = -top + top*2*(375)/res.y
p_world = eye - near*n + uc*u + vr * v
ray = Ray(np.vstack(eye), np.vstack(p_world - eye))
# print(p_world)
# print(ray.dir)
# print(uc)


def check_pixel():
    
    for h in range(res.y-1,-1,-1):
        width_color = []
        for w in range(res.x):
            uc = -right + right*2*(w)/res.x
            vr  = -top + top*2*(h)/res.y
            p_world = eye - near*n + uc*u + vr * v
            ray = Ray(eye, p_world - eye)
            color = ray_trace(ray, 1)
            width_color.append(color)
        final_color.append(width_color)
    print("done")
    return final_color

def ray_trace(ray, t):
    
    for sphere in spheres:

        model_view_matrix = np.array([[sphere.scl_x,0,0,sphere.pos_x],
                                        [0,sphere.scl_y,0,sphere.pos_y],
                                        [0,0,sphere.scl_z,sphere.pos_z],
                                        [0,0,0,1]])
        model_inverse_matrix = np.linalg.inv(model_view_matrix)
        # print(sphere.b)
        # if(sphere.b == 0.5):
        #     print(model_view_matrix)
        #matrix multiplication to find inverse transformed ray
        sp = ray.start_point
        sd = ray.dir
        #calculate inverse transformed ray with Homogeneous coord 
        ivr = Ray(model_inverse_matrix@np.vstack([sp[0],sp[1],sp[2],1]), model_inverse_matrix@np.vstack([sd[0],sd[1],sd[2],0]))
        #drop inverse transformed ray Homogeneous coord
        ivr = Ray(np.vstack([ivr.start_point[0],ivr.start_point[1],ivr.start_point[2]]), 
                  np.vstack([ivr.dir[0],ivr.dir[1],ivr.dir[2]])) 
        #find quadratic equation 
        
        a = np.square(np.sqrt(np.squeeze(ivr.dir).dot(np.squeeze(ivr.dir))))
        b = np.dot(np.squeeze(ivr.start_point),np.squeeze((ivr.dir)))
        c = np.square(np.sqrt(np.squeeze(ivr.start_point).dot(np.squeeze(ivr.start_point)))) - sphere.radius*sphere.radius
        
        # print(b)
        if (np.square(b) - a * c) > 0:
            # print(np.square(b) - a * c)
            # print(sphere.r)
            color = Color(sphere.r,sphere.g,sphere.b)
            return color
    return back_color
        
# ray_trace(ray, 1)
# check_pixel()
Output.output(output, res.x, res.y,check_pixel())

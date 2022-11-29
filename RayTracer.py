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
ambient = Color(0,0,0)
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
                ambient = Color(float(line[1]) , float(line[2]) , float(line[3]))
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


def normalize (x):
    return x /np.sqrt(np.squeeze(x).dot(np.squeeze(x)))

# image = np.zeros([2*right,2*top,res.x,res.y])
eye = np.array([0,0,0])
u = np.array([1,0,0])
v = np.array([0,1,0])
n = np.array([0,0,1])
camera = np.column_stack((eye,u,v,n))

uc = -right + right*2*(300)/res.x
vr  = -top + top*2*(300)/res.y
p_world = eye - near*n + uc*u + vr * v
ray = Ray(np.vstack(eye), np.vstack(p_world - eye))

def check_pixel():
    for h in range(res.y-1,-1,-1):
        width_color = []
        for w in range(res.x):
            uc = -right + right*2*(w)/res.x
            vr  = -top + top*2*(h)/res.y
            p_world = eye - near*n + uc*u + vr * v
            # print(h, end = " ")
            # print(w)
            ray = Ray(eye, p_world - eye)
            color = ray_trace(ray)
            width_color.append(color)
        final_color.append(width_color)
        
    print("done")
    return final_color

def check_sphere_intersect(ray, current_sphere):
        temp_th = np.inf
        #matrix multiplication to find inverse transformed ray
        sp = ray.start_point
        sd = ray.dir
        #calculate inverse transformed ray with Homogeneous coord 
        #@ for np multiplication operator 
        # print(np.vstack([sd[0],sd[1],sd[2],0]))
        # print(sd)
        ivr = Ray(current_sphere.model_inverse_matrix@np.vstack([sp[0],sp[1],sp[2],1]), 
                current_sphere.model_inverse_matrix@np.vstack([sd[0],sd[1],sd[2],0]))
        # print(current_sphere.model_inverse_matrix, end="  ")
        #drop inverse transformed ray Homogeneous coord
        ivr = Ray(np.vstack([ivr.start_point[0],ivr.start_point[1],ivr.start_point[2]]), 
                  np.vstack([ivr.dir[0],ivr.dir[1],ivr.dir[2]])) 
        #find quadratic equation 
        a = np.square(np.sqrt(np.squeeze(ivr.dir).dot(np.squeeze(ivr.dir))))
        b = np.dot(np.squeeze(ivr.start_point),np.squeeze((ivr.dir)))
        c = np.square(np.sqrt(np.squeeze(ivr.start_point).dot(np.squeeze(ivr.start_point)))) - current_sphere.radius*current_sphere.radius
        #check if interset 
        if (np.square(b) - a * c) > 0:
            #check closest intersetion 
            th1 = -b/a + np.sqrt(np.square(b) - a * c)/a
            th2 = -b/a - np.sqrt(np.square(b) - a * c)/a
            temp_th = th1
            if th2 < th1:
                temp_th = th2
        return temp_th

def ray_trace(ray):
    th = np.inf
    r = back_color.r
    g = back_color.g
    b = back_color.b
    interset_sphere = 0
    for sphere in spheres:
        temp_th = check_sphere_intersect(ray, sphere)
        if temp_th < th and temp_th > 1:
            th = temp_th
            interset_sphere = sphere    
    # print(th)
    if th == np.inf:
        return back_color
    p = ray.start_point + ray.dir * th
    # print(p[0])
    sphere_color = Color(interset_sphere.r,interset_sphere.g,interset_sphere.b)
    
    normal = sphere.get_normal(interset_sphere.model_inverse_matrix,p)
    # print(normalize(p))
    
    color = sphere_color * ambient * interset_sphere.ka
    # po = normalize(origin - p)
    normal = np.vstack([normal[0],normal[1],normal[2]])
    v = normalize(np.vstack(eye) - np.vstack(p))
    # print(normal)
    for light in lights:
        light_color = Color(light.lr,light.lg,light.lb)
        light_pos = np.array([light.pos_x,light.pos_y,light.pos_z])
        # print(light_pos)
        # print(p)
        # print(p[1])
        # print(p)
        # print(light_pos)
        p_dir = normalize(np.vstack(light_pos) - np.vstack(p) )
        # print(p_dir)
        light_ray = Ray(p, p_dir)
        ray_th = np.inf
        for sphere in spheres:
            if(sphere != interset_sphere):
                temp_th = check_sphere_intersect(light_ray,sphere)
                if(temp_th < ray_th):
                    ray_th = temp_th
        if(ray_th == np.inf):
            # print(np.squeeze(normal))
            ndotL = np.dot(np.squeeze(normal),np.squeeze((np.vstack(p_dir))))
            diffuse_color = light_color * sphere_color * ndotL * interset_sphere.kd
            r = 2*ndotL*normal  - np.vstack(p_dir)
            # print(interset_sphere.ks)
            # print(r)
            specular_color = light_color * sphere_color * np.power(np.dot(np.squeeze(r), np.squeeze(v)), sphere.n) * interset_sphere.ks
            # print(np.power(np.dot(np.squeeze(r), np.squeeze(v)), sphere.n))
            # print(sphere.n)
            color += diffuse_color + specular_color
            # print(diffuse_color.r)
            # print(np.power(np.dot(np.squeeze(r), np.squeeze(v)), sphere.n))
    # print(color.r)
    # print(color.g)
    # print(color.b)
            # print("add point light color")    
    # print(color.g)
    return color
    
# ray_trace(ray)
# check_pixel()
Output.output(output, res.x, res.y,check_pixel())

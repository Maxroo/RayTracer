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
res = []
spheres = []
lights = []
back_color = []
ambient = []
output = ''
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
                ambient = np.array([float(line[1]) , float(line[2]) , float(line[3])])
                # ambient = Color(float(line[1]) , float(line[2]) , float(line[3]))
            elif(line[0] == 'BACK'):
                back_color = np.array([float(line[1]) , float(line[2]) , float(line[3])])
                # back_color = Color(float(line[1]) , float(line[2]) , float(line[3]))
            elif(line[0] == 'RES'):
                res = [int(line[1]), int(line[2])]
            elif(line[0] == 'LIGHT'):
                light = {
                "name" : line[1] ,"pos_x" : float(line[2]),"pos_y" : float(line[3]), "pos_z" : float(line[4]),
                "lr" : float(line[5]),"lg" : float(line[6]),"lb" : float(line[7])
                }
                lights.append(light)
                # lights.append(Light(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7])))
            elif(line[0] == 'SPHERE'):
                sphere = {
                "name" : line[1],"pos_x" : float(line[2]),"pos_y" : float(line[3]),"pos_z" : float(line[4]),
                "scl_x" : float(line[5]),"scl_y" : float(line[6]),"scl_z" : float(line[7]) ,
                "r" : float(line[8]),"g" : float(line[9]),"b" : float(line[10]),
                "ka" : float(line[11]),"kd" : float(line[12]),"ks" : float(line[13]),"kr" : float(line[14]),"n" : int(line[15]),"radius" : 1 
                }
                model_matrix = np.array([[sphere.get("scl_x"),0,0,sphere.get("pos_x")],
                                            [0,sphere.get("scl_y"),0,sphere.get("pos_y")],
                                            [0,0,sphere.get("scl_z"),sphere.get("pos_z")],
                                            [0,0,0,1]])
                sphere.update({"model_matrix" : model_matrix})
                sphere.update({"model_inverse_matrix": np.linalg.inv(sphere.get("model_matrix"))})
                spheres.append(sphere)
                # spheres.append(Sphere(line[1], float(line[2]), float(line[3]), float(line[4]),float(line[5]), float(line[6]), float(line[7]),
                #                     float(line[8]),float(line[9]),float(line[10]),float(line[11]),float(line[12]),float(line[13]),float(line[14]),
                #                     int(line[15])))
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



def check_pixel():
    for h in range(res[1]-1,-1,-1):
        width_color = []
        for w in range(res[0]):
            uc = -right + right*2*(w)/res[0]
            vr  = -top + top*2*(h)/res[1]
            p_world = eye - near*n + uc*u + vr * v
            ray = Ray(eye, p_world - eye)
            color = ray_trace(ray)
            if(w == 400 and h == 400):
                color = [0,0,0]
            width_color.append(color)
        final_color.append(width_color)
        
    print("done")
    return final_color

def check_sphere_intersect(ray, current_sphere):
        if ray.depth > 3:
            return np.array([0, 0, 0])
        
        temp_th = np.inf
        #matrix multiplication to find inverse transformed ray
        sp = ray.start_point
        sd = ray.dir
        p = 0
        #calculate inverse transformed ray with Homogeneous coord 
        #@ for np multiplication operator 
        ivr = Ray(current_sphere.get("model_inverse_matrix")@np.vstack([sp[0],sp[1],sp[2],1]), 
                current_sphere.get("model_inverse_matrix")@np.vstack([sd[0],sd[1],sd[2],0]))
        # print(current_sphere.model_inverse_matrix, end="  ")
        #drop inverse transformed ray Homogeneous coord
        ivr = Ray(np.vstack([ivr.start_point[0],ivr.start_point[1],ivr.start_point[2]]), 
                  np.vstack([ivr.dir[0],ivr.dir[1],ivr.dir[2]])) 
        #find quadratic equation 
        a = np.square(np.sqrt(np.squeeze(ivr.dir).dot(np.squeeze(ivr.dir))))
        b = np.dot(np.squeeze(ivr.start_point),np.squeeze((ivr.dir)))
        c = np.square(np.sqrt(np.squeeze(ivr.start_point).dot(np.squeeze(ivr.start_point)))) - 1
        #check if interset 
        if (np.square(b) - a * c) > 0:
            #check closest intersetion 
            th1 = -b/a + np.sqrt(np.square(b) - a * c)/a
            th2 = -b/a - np.sqrt(np.square(b) - a * c)/a 
            temp_th = th1
            if th2 < th1:
                temp_th = th2
            p = ivr.start_point + ivr.dir * temp_th
        elif(np.square(b) - a * c == 0):
            temp_th = 0.1
        if(temp_th > -5*10**-4 and temp_th < 5*10**-4):
            temp_th = 0
        return temp_th, p

def ray_trace(ray):
    th = np.inf
    interset_sphere = 0
    p_sphere_space = 0
    for sphere in spheres:
        temp_th, temp_p = check_sphere_intersect(ray, sphere)
        # print(temp_th)
        if temp_th < th and temp_th >= 0.4:
            th = temp_th
            interset_sphere = sphere    
            p_sphere_space = temp_p    
    # print(th)
    if th == np.inf:
        # print("not hit")
        return back_color
    p = ray.start_point + ray.dir * th
    sphere_color = np.array([interset_sphere.get("r"),interset_sphere.get("g"),interset_sphere.get("b")])

    homo_p_sphere_space = np.vstack([p_sphere_space[0],p_sphere_space[1],p_sphere_space[2],0])
    normal = np.transpose(interset_sphere.get("model_inverse_matrix"))@homo_p_sphere_space
    color = sphere_color * ambient * interset_sphere.get("ka")
    N = normalize(p)
    V = normalize(np.vstack(ray.start_point) - np.vstack(p))
    # print((normal))
    normal = np.vstack([normal[0],normal[1],normal[2]])
    normal = normalize(normal)
    # print(color)
    for light in lights:
        light_color = np.array([light.get("lr"),light.get("lg"),light.get("lb")])
        light_pos = np.array([light.get("pos_x"),light.get("pos_y"),light.get("pos_z")])
        # print(p)
        L = normalize(np.vstack(light_pos) - np.vstack(p) )
        # print(str(L) + light.get("name"))
        light_ray = Ray(p, L)
        ray_th = np.inf
        p_light_space = 0
        for sphere in spheres:
            # print("current sphere : " + interset_sphere.get("name"), end="")
            temp_th,temp_p = check_sphere_intersect(light_ray,sphere)
            # print(" "+ str(temp_th) + " with sphere "+ sphere.get("name") + " on light" + light.get("name"), end="")  
                
            if(temp_th < ray_th and temp_th >= 0):
                # print(" :intersect")
                ray_th = temp_th
                p_light_space = temp_p
                break
            # else:
                # print(" :not intersect")
        # if(light.get("name") == "l3"):
        # print(temp_th)            
        if(ray_th == np.inf):
            ndotL = np.dot(np.squeeze(normal),np.squeeze((np.vstack(L))))
            diffuse_color = light_color * sphere_color * ndotL * interset_sphere.get("kd")
            # print(diffuse_color)
            R = 2*ndotL*normal - L
            color += diffuse_color
            specular_color = light_color *(np.power(np.dot(np.squeeze(R), np.squeeze(V)), interset_sphere.get("n"))) * interset_sphere.get("ks")
            # print(specular_color)
            color += specular_color
        # else:
        #     color = np.array([0,0,0])
    
    #reflected Ray 
    ndotc = np.dot(np.squeeze(np.vstack(normal)),np.squeeze((np.vstack(ray.dir))))
    v = -2* ndotc * np.vstack(normal) + np.vstack(ray.dir)
    reflect_ray = Ray(np.vstack(p),np.vstack(v))
    reflect_ray.set_depth(reflect_ray.depth + 1)
    color += ray_trace(reflect_ray) * interset_sphere.get("kr")
    print(ray_trace(reflect_ray) * interset_sphere.get("kr"))
    color = np.clip(color,0,1)
    print(color)
    return color

def debug_check_pixel(w,h):
    uc = -right + right*2*(w)/res[0]
    vr  = -top + top*2*(h)/res[1]
    p_world = eye - near*n + uc*u + vr * v
    ray = Ray(np.vstack(eye), np.vstack(p_world - eye))
    ray_trace(ray)
    
debug_check_pixel(300, 250)
# check_pixel()

# Output.output(output, res[0], res[1],check_pixel()) 


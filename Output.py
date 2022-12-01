import sys
# import numpy as np

def output(name,width,height,output):
    f = open(name, "w")
    f.write("P3 \n") #image format 
    f.write(str(width) + " " + str(height) + " \n") #width,height
    f.write("255\n") #maximum color value
    pixel = ""
    
    for h in range(height):
        for w in range(width):
            color = output[h][w]
            pixel += "   " + str(color[0] * 255) + " " + str(color[1] * 255) + " " + str(color[2] * 255)
            
        f.write(pixel + "\n")
        pixel = ""
    f.close()
    

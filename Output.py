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
            pixel += "   " + str(color.r * 255) + " " + str(color.g * 255) + " " + str(color.b * 255)
            
        f.write(pixel + "\n")
        pixel = ""
    f.close()
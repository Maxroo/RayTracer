import sys
def output(name,width,height):
    f = open(name, "w")
    f.write("P3 \n") #image format 
    f.write(str(width) + " " + str(height) + " \n") #width,height
    f.write("1\n") #maximum color value
    pixel = ""
    for h in range(height):
        for w in range(width):
            pixel += "   1 1 1"
        f.write(pixel + "\n")
        pixel = ""
    f.close()
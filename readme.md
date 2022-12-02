# Backwards RayTracer

## Description 
The file RayTracer.py takes a txt scene file as input, output image as ppm(text-based (P3)) file. 

## Requirements
To get this RayTracer to work you will need to install *numpy* and *python* in your machine 

- txt file contains scene info as in the test folder

## Test
You will need to call (use 1 if there are more python function in the system):
1. python3 lp_solver.py  file_name.txt
                    or
2. python lp_solver.py  file_name.txt

## input file format 
Content: 
1. The near plane**, left**, right**, top**, and bottom**
2. The resolution of the image nColumns* X nRows*
3. The position** and scaling** (non-uniform), color***, Ka***, Kd***, Ks***, Kr*** and the specular exponent n* of a sphere
4. The position** and intensity*** of a point light source
5. The background colour ***
6. The scene’s ambient intensity***
7. The output file name (you should limit this to 20 characters with no spaces)

* (*)int  
* (**)float  
* (***)float between 0 and 1

## output 
To view ppm file you can:
1. use a online ppm viewer e.g. https://www.cs.rhodes.edu/welshc/COMP141_F16/ppmReader.html
2. use local applications that supports ppm file 


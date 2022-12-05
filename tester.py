import subprocess
import os
import time
# PROGRAM_COMMAND = "RayTracer" # executable called "RayTracer" or "RayTracer.exe"
# PROGRAM_COMMAND = "python3 RayTracer.py" # python3 on unix-like systems#
#PROGRAM_COMMAND = "python RayTracer.py" # python 3 on windows OR python 2.7 on any system

def execute_all_tests(verbose = False):
                       
    out = None
    if not verbose:
        out = subprocess.DEVNULL
    
    for filename in os.listdir("Tests/"):
        if filename.endswith(".txt"):
            tic = time.perf_counter()
            print(f"RUNNING {filename}")
            filename = " Tests/"+ filename
            PROGRAM_COMMAND = "python3 RayTracer.py" + filename
            subprocess.run([PROGRAM_COMMAND],shell=True)
            toc = time.perf_counter()
            print(f"DONE {filename} in {toc - tic: 0.4f} seconds")

if __name__ == "__main__":
    execute_all_tests(verbose=False)
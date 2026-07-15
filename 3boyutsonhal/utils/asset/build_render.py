import os
import subprocess
import sys

def build_render():
    cwd = os.getcwd()
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    src = 'render.c'
    out = 'render.dll'
    
    # Try MSVC (cl.exe)
    try:
        print("Attempting to compile with MSVC...")
        subprocess.check_call(['cl', '/LD', '/O2', src, '/Fe' + out])
        print("Successfully compiled with MSVC.")
        os.chdir(cwd)
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("MSVC failed or not found.")

    # Try GCC
    try:
        print("Attempting to compile with GCC...")
        subprocess.check_call(['gcc', '-shared', '-Wall', '-O3', src, '-o', out])
        print("Successfully compiled with GCC.")
        os.chdir(cwd)
        return
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("GCC failed or not found.")
        
    print("Failed to compile render.c. Please install a C compiler (Visual Studio or MinGW).")
    os.chdir(cwd)

if __name__ == '__main__':
    build_render()

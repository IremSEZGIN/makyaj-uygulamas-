import os
import sys
import traceback

print("--- DIAGNOSTIC START ---")
print(f"Python: {sys.version}")
print(f"CWD: {os.getcwd()}")

def debug_import(module_name):
    print(f"Importing {module_name}...", end=" ", flush=True)
    try:
        __import__(module_name)
        print("Done.")
    except Exception as e:
        print(f"FAILED: {e}")
        traceback.print_exc()

debug_import("fastapi")
debug_import("uvicorn")
debug_import("cv2")
debug_import("numpy")
debug_import("makeup")
debug_import("color_analysis")

try:
    print("Loading 'app' from 'server'...")
    from server import app
    print("App loaded. Starting uvicorn...")
    import uvicorn
    # Use 127.0.0.1 and a different port to eliminate network/binding doubt
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="debug")
except Exception:
    print("!!! FATAL ERROR !!!")
    traceback.print_exc()

print("--- DIAGNOSTIC END ---")

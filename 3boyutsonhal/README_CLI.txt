
3DDFA_V2 CLI Demo Instructions
==============================

This project allows you to reconstruct a 3D face model from a single 2D photo.

Prerequisites
-------------
You need Python installed.
Install the required packages:
pip install -r requirements.txt

How to Run via Command Line
---------------------------
1. Open a terminal (Command Prompt or PowerShell).
2. Navigate to this directory.
3. Run the following command:

   python cli_demo.py --img <path_to_your_image.jpg>

   Example:
   python cli_demo.py --img solvay.jpg

4. The output will be a ZIP file (e.g., `results_....zip`) containing the textured 3D model.
   Extract this zip file and open the .obj file to view the 3D model with colors.

Optional Arguments
------------------
--out <filename> : Specify the output filename (e.g., --out my_result)

How to Run the Web Demo
-----------------------
   python gradiodemo.py

Then open the URL shown in the terminal (usually http://127.0.0.1:7860).

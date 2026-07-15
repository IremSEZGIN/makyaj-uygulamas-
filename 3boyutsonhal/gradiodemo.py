# before import, make sure FaceBoxes and Sim3DR are built successfully, e.g.,
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import sys
from subprocess import call
import torch

torch.hub.download_url_to_file('https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Solvay_conference_1927.jpg/1400px-Solvay_conference_1927.jpg', 'solvay.jpg')

def run_cmd(command):
    try:
        print(command)
        call(command, shell=True)
    except Exception as e:
        print(f"Errorrrrr: {e}!")
        
# Build commands removed. Using pre-compiled or python fallback.
print(os.getcwd())


import cv2
import yaml

from FaceBoxes import FaceBoxes
from TDDFA import TDDFA
from utils.render_ctypes import render
# from utils.depth import depth
# from utils.pncc import pncc
# from utils.uv import uv_tex
from utils.pose import viz_pose
from utils.serialization import ser_to_ply, ser_to_obj
from utils.functions import draw_landmarks, get_suffix

import matplotlib.pyplot as plt
from skimage import io
import gradio as gr

# load config
cfg = yaml.load(open('configs/mb1_120x120.yml'), Loader=yaml.SafeLoader)

# Init FaceBoxes and TDDFA, recommend using onnx flag
onnx_flag = True  # or True to use ONNX to speed up
if onnx_flag:    
    import os
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ['OMP_NUM_THREADS'] = '4'
    from FaceBoxes.FaceBoxes_ONNX import FaceBoxes_ONNX
    from TDDFA_ONNX import TDDFA_ONNX

    face_boxes = FaceBoxes_ONNX()
    tddfa = TDDFA_ONNX(**cfg)
else:
    face_boxes = FaceBoxes()
    tddfa = TDDFA(gpu_mode=False, **cfg)
    


from utils.serialization import ser_to_obj, ser_to_obj_textured
import uuid
import zipfile
import os

def inference (img):
    # Gradio input is RGB, but models expect BGR
    img_bgr = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # face detection
    boxes = face_boxes(img_bgr)
    # regress 3DMM params
    param_lst, roi_box_lst = tddfa(img_bgr, boxes)
    # reconstruct vertices and render
    ver_lst = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=True)
    
    if not ver_lst:
        print("No face detected.")
        return img, None
    
    # Render image (returns BGR)
    res_img_bgr = render(img_bgr, ver_lst, tddfa.tri, alpha=0.6, show_flag=False)
    # Convert back to RGB for Gradio display
    res_img_rgb = cv2.cvtColor(res_img_bgr, cv2.COLOR_BGR2RGB)
    
    # Save 3D model to obj (expects BGR image for texture sampling)
    # Save 3D model to obj (expects BGR image for texture sampling)
    base_name = f'results_{uuid.uuid4().hex}'
    obj_filename = f'{base_name}.obj'
    ser_to_obj_textured(img_bgr, ver_lst, tddfa.tri, height=img.shape[0], wfp=obj_filename)
    
    # Zip the files
    zip_filename = f'{base_name}.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        zipf.write(obj_filename)
        if os.path.exists(f'{base_name}.mtl'):
            zipf.write(f'{base_name}.mtl')
        if os.path.exists(f'{base_name}.jpg'):
            zipf.write(f'{base_name}.jpg')
            
    return res_img_rgb, zip_filename

title = "3DDFA V2"
description = "demo for 3DDFA V2. To use it, simply upload your image, or click one of the examples to load them. Read more at the links below."
article = "<p style='text-align: center'><a href='https://arxiv.org/abs/2009.09960'>Towards Fast, Accurate and Stable 3D Dense Face Alignment</a> | <a href='https://github.com/cleardusk/3DDFA_V2'>Github Repo</a></p>"
examples = [
    ['solvay.jpg']
]
gr.Interface(
    fn=inference, 
    inputs=gr.Image(label="Input"), 
    outputs=[
        gr.Image(label="Output Image"),
        gr.File(label="Download 3D Model (.zip)")
    ],
    title=title,
    description=description,
    article=article,
    examples=examples
    ).launch()

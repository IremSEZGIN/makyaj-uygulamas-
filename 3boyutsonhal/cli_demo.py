import argparse
import os
import sys
import cv2
import yaml
import zipfile
import time

# Add current directory to sys.path
sys.path.append(os.getcwd())

from FaceBoxes import FaceBoxes
from TDDFA import TDDFA
from utils.serialization import ser_to_obj_textured


def main(args):
    start = time.time()

    # Load config
    cfg = yaml.load(open(args.config), Loader=yaml.SafeLoader)

    # Init FaceBoxes and TDDFA (ONNX hızlıdır)
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
    os.environ['OMP_NUM_THREADS'] = '4'

    from FaceBoxes.FaceBoxes_ONNX import FaceBoxes_ONNX
    from TDDFA_ONNX import TDDFA_ONNX

    face_boxes = FaceBoxes_ONNX()
    tddfa = TDDFA_ONNX(**cfg)

    # Read image
    img = cv2.imread(args.img)
    if img is None:
        print(f"Error: Could not read image {args.img}")
        return

    # Face detection
    boxes = face_boxes(img)
    print(f"Detected {len(boxes)} faces")

    if len(boxes) == 0:
        print("No faces detected.")
        return

    # Regress 3DMM params
    param_lst, roi_box_lst = tddfa(img, boxes)

    # Reconstruct vertices
    ver_lst = tddfa.recon_vers(param_lst, roi_box_lst, dense_flag=True)

    # --------- SABİT DOSYA İSİMLERİ ---------
    out_dir = "."
    base_name = "model"

    obj_filename = os.path.join(out_dir, f"{base_name}.obj")

    print(f"Exporting textured model to {obj_filename}...")
    ser_to_obj_textured(
        img,
        ver_lst,
        tddfa.tri,
        height=img.shape[0],
        wfp=obj_filename
    )

    # Zip oluştur
    zip_filename = os.path.join(out_dir, f"{base_name}.zip")
    print(f"Creating zip archive {zip_filename}...")

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        obj_path = os.path.join(out_dir, f"{base_name}.obj")
        mtl_path = os.path.join(out_dir, f"{base_name}.mtl")
        jpg_path = os.path.join(out_dir, f"{base_name}.jpg")

        if os.path.exists(obj_path):
            zipf.write(obj_path, f"{base_name}.obj")
        if os.path.exists(mtl_path):
            zipf.write(mtl_path, f"{base_name}.mtl")
        if os.path.exists(jpg_path):
            zipf.write(jpg_path, f"{base_name}.jpg")

    end = time.time()
    print("Gerçek model üretim süresi:", round(end - start, 2), "saniye")
    print("Done!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='3DDFA_V2 CLI Demo')
    parser.add_argument('-c', '--config', type=str, default='configs/mb1_120x120.yml',
                        help='path to config file')
    parser.add_argument('-i', '--img', type=str, required=True,
                        help='path to image file')

    args = parser.parse_args()
    main(args)

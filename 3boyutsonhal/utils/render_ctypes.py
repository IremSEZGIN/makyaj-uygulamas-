# coding: utf-8

"""
Borrowed from https://github.com/1996scarlet/Dense-Head-Pose-Estimation/blob/main/service/CtypesMeshRender.py

To use this render, you should build the clib first:
```
cd utils/asset
gcc -shared -Wall -O3 render.c -o render.so -fPIC
cd ../..
```
"""

import sys

sys.path.append('..')

import os.path as osp
import cv2
import numpy as np
import ctypes
from utils.functions import plot_image

make_abs_path = lambda fn: osp.join(osp.dirname(osp.realpath(__file__)), fn)


class TrianglesMeshRender(object):
    def __init__(
            self,
            clibs,
            light=(0, 0, 5),
            direction=(0.6, 0.6, 0.6),
            ambient=(0.3, 0.3, 0.3)
    ):
        if not osp.exists(clibs):
            raise Exception(f'{clibs} not found, please build it first, by run '
                            f'"gcc -shared -Wall -O3 render.c -o render.so -fPIC" in utils/asset directory')

        self._clibs = ctypes.CDLL(clibs)

        self._light = np.array(light, dtype=np.float32)
        self._light = np.ctypeslib.as_ctypes(self._light)

        self._direction = np.array(direction, dtype=np.float32)
        self._direction = np.ctypeslib.as_ctypes(self._direction)

        self._ambient = np.array(ambient, dtype=np.float32)
        self._ambient = np.ctypeslib.as_ctypes(self._ambient)

    def __call__(self, vertices, triangles, bg):
        self.triangles = np.ctypeslib.as_ctypes(3 * triangles)  # Attention
        self.tri_nums = triangles.shape[0]

        self._clibs._render(
            self.triangles, self.tri_nums,
            self._light, self._direction, self._ambient,
            np.ctypeslib.as_ctypes(vertices),
            vertices.shape[0],
            np.ctypeslib.as_ctypes(bg),
            bg.shape[0], bg.shape[1]
        )


import platform

class PyTrianglesMeshRender(object):
    def __init__(self, light=(0, 0, 5), direction=(0.6, 0.6, 0.6), ambient=(0.3, 0.3, 0.3)):
        self.light = np.array(light, dtype=np.float32)
        self.direction = np.array(direction, dtype=np.float32)
        self.ambient = np.array(ambient, dtype=np.float32)

    def __call__(self, vertices, triangles, bg):
        # Simple Painter's Algorithm
        # Calculate depth of each triangle
        tri_verts = vertices[triangles] # (ntri, 3, 3)
        depths = tri_verts[:, :, 2].mean(axis=1) # (ntri,)
        
        # Sort triangles by depth (far to near)
        order = np.argsort(depths)
        
        h, w = bg.shape[:2]
        
        # Calculate normals for shading (simplified)
        v0 = tri_verts[:, 1] - tri_verts[:, 0]
        v1 = tri_verts[:, 2] - tri_verts[:, 0]
        normals = np.cross(v0, v1)
        norms = np.linalg.norm(normals, axis=1, keepdims=True)
        normals = normals / (norms + 1e-6)
        
        # Directional light
        intensity = np.dot(normals, self.direction)
        intensity = np.clip(intensity, 0, 1)[:, np.newaxis]
        
        # Color calculation (simplified, assuming white mesh)
        colors = self.ambient + intensity * 0.5 # Simple lighting model
        colors = np.clip(colors, 0, 1) * 255
        
        for i in order:
            tri = triangles[i]
            pts = vertices[tri, :2].astype(np.int32)
            color = tuple(colors[i].tolist())
            cv2.fillConvexPoly(bg, pts, color)

try:
    lib_name = 'render.dll' if platform.system() == 'Windows' else 'render.so'
    render_app = TrianglesMeshRender(clibs=make_abs_path(f'asset/{lib_name}'))
except Exception as e:
    print(f"Could not load compiled render library: {e}. Using pure Python fallback (slower).")
    render_app = PyTrianglesMeshRender()



def render(img, ver_lst, tri, alpha=0.6, show_flag=False, wfp=None, with_bg_flag=True):
    if with_bg_flag:
        overlap = img.copy()
    else:
        overlap = np.zeros_like(img)

    for ver_ in ver_lst:
        ver = np.ascontiguousarray(ver_.T)  # transpose
        render_app(ver, tri, bg=overlap)

    if with_bg_flag:
        res = cv2.addWeighted(img, 1 - alpha, overlap, alpha, 0)
    else:
        res = overlap

    if wfp is not None:
        cv2.imwrite(wfp, res)
        print(f'Save visualization result to {wfp}')

    if show_flag:
        plot_image(res)

    return res

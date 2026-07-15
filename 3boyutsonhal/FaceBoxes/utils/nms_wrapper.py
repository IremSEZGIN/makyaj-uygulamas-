# coding: utf-8

# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

try:
    from .nms.cpu_nms import cpu_nms, cpu_soft_nms
except ImportError:
    pass # Will fallback to py_cpu_nms in nms()



def nms(dets, thresh):
    """Dispatch to either CPU or GPU NMS implementations."""

    if dets.shape[0] == 0:
        return []
    
    try:
        return cpu_nms(dets, thresh)
    except NameError:
        from .nms.py_cpu_nms import py_cpu_nms
        return py_cpu_nms(dets, thresh)

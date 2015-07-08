__author__ = 'james'

import matplotlib.pyplot as plt
import SimpleITK as sitk
import numpy as np
from tempfile import TemporaryFile
import nrrd
import os
import sys

windows = sys.platform == "win32" or sys.platform == "win64"

def autocrop(stack):

    # Compute MIP
    mip = maximum_intensity_projection(stack)

    # Get bounding box
    bbox, cropped_dims = get_cropbox(mip)

    # Add third dimension
    cropped_dims = list(cropped_dims)
    cropped_dims.append(stack.dims[2])

    tmp_file = TemporaryFile(mode='w+b')
    for i, im in enumerate(stack):
        print i
        cropped = im[bbox[2]:bbox[3], bbox[0]:bbox[1]]
        cropped.tofile(tmp_file)

    nrrd_out = os.path.join(os.path.dirname(stack.recon_dir), 'stack.nrrd')
    mmap = np.memmap(tmp_file, dtype=stack.dtype, shape=tuple(cropped_dims))
    nrrd.write(nrrd_out, np.swapaxes(mmap, 1, 2))

    return nrrd_out

def get_cropbox(max_im):

    max_im = sitk.GetImageFromArray(max_im)
    seg = sitk.OtsuThreshold(max_im, 0, 255, 128)
    seg = sitk.ConnectedComponent(seg)
    seg = sitk.RelabelComponent(seg)  # relabel components in order of ascending size
    seg = seg == 1  # discard all but largest component

    # Get bounding box
    label_stats = sitk.LabelStatisticsImageFilter()
    label_stats.Execute(max_im, seg)
    bbox = list(label_stats.GetBoundingBox(1))

    # Pad bounding box and crop
    max_im = sitk.GetArrayFromImage(max_im)
    bbox = pad_bounding_box(bbox, max_im.shape)
    cropped = max_im[bbox[2]:bbox[3], bbox[0]:bbox[1]]

    return bbox, cropped.shape

def pad_bounding_box(bbox, dims):

    padding = np.mean(dims) * 0.025

    bbox[0] -= padding  # xmin
    if bbox[0] < 0:
        bbox[0] = 0

    bbox[1] += padding  # xmax
    if bbox[1] > dims[0] - 1:
        bbox[1] = dims[0] - 1

    bbox[2] -= padding  # ymin
    if bbox[2] < 0:
        bbox[2] = 0

    bbox[3] += padding  # ymax
    if bbox[3] > dims[1] - 1:
        bbox[3] = dims[1]

    return bbox

def maximum_intensity_projection(stack):

    step_size = 10
    sparse_list = np.arange(0, stack.dims[2], step_size)
    max_im = np.zeros(shape=stack.dims[:2], dtype=stack.dtype)

    for i in sparse_list:
        im = stack[i]
        idx = im > max_im
        max_im[idx] = im[idx]

    return max_im

__author__ = 'james'

import numpy as np
from vispy.geometry.isosurface import isosurface

NO_BLOCKS = 20

def compute_curvature(stack):

    block_size = stack.no_slices / NO_BLOCKS
    block_intervals = range(0, stack.no_slices, block_size)

    curve = np.zeros(NO_BLOCKS, 3)
    return curve

def create_mesh(seg):

    vertices, faces = isosurface(seg, 1)
    return vertices, faces

def compute_surface_normals(vertices, faces):
    raise NotImplementedError

def compute_vertex_normals(face_normals, faces):
    raise NotImplementedError

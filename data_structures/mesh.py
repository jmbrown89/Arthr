__author__ = 'james'

import image_processing.processing as proc

class Mesh(object):

    def __init__(self, vertices, faces, curve, name='Untitled mesh'):

        self.vertices = vertices
        self.faces = faces
        self.curve = curve
        self.name = name

        self.face_normals = proc.compute_surface_normals(vertices, faces)
        self.vertex_normals = proc.compute_vertex_normals(self.face_normals, self.faces)

    def write_ply(self, out_dir):

        raise NotImplementedError

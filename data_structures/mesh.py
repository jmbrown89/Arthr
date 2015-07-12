__author__ = 'james'

import image_processing.processing as proc
import os

class Mesh(object):

    def __init__(self, vertices, faces, name='Untitled mesh'):

        self.vertices = vertices
        self.faces = faces
        self.name = name

        self.face_normals = proc.compute_surface_normals(vertices, faces)
        self.vertex_normals = proc.compute_vertex_normals(self.face_normals, self.faces)

    def write_ply(self, out_dir):
        ply_out = os.path.join(out_dir, self.name + '.ply')
        return ply_out

    def transform(self, T, bone):
        raise NotImplementedError


class Model(Mesh):

    # TODO implement constraints and hierarchy
    def __init__(self, vertices, faces, labels, joints, name='Untitled model'):

        # Call super constructor
        super(Model).__init__(self, vertices, faces, name=name)

        # Store labels
        self.labels = labels

        # Store joints
        self.joints = joints

    def write_ply(self, out_dir):
        ply_out = os.path.join(out_dir, self.name + '.ply')
        return ply_out

def load_model(model_dir):
    return None


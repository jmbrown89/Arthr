__author__ = 'james'

import os
import glob
import tifffile
from mesh import Mesh
from image_processing import cropping
import image_processing.segment as segment

class Stack:

    def __init__(self, recon_dir, name='Untitled mesh'):

        self.recon_dir = recon_dir
        self.name = name
        self.dims = [-1, -1, -1]
        self.no_slices = -1
        self.slice_files = None
        self.stack = None
        self.dtype = None

        # Get list of slice files and data type
        self.get_data()

    def get_data(self):

        # Find files in recon dir
        self.slice_files = glob.glob(os.path.join(self.recon_dir, '*{}.tif'.format('[0-9]' * 4)))
        self.slice_files = sorted(self.slice_files)
        self.no_slices - len(self.slice_files)

        # Get slice dimensions
        im = tifffile.imread(self.slice_files[0])
        self.dims = list(im.shape)
        self.dims.append(len(self.slice_files))
        self.dims = tuple(self.dims)

        # Get datatype
        self.dtype = im.dtype

    def __iter__(self):
        for i in range(0, self.dims[2]):
            yield self.__getitem__(i)

    def __getitem__(self, item):
        return tifffile.imread(self.slice_files[item])

if __name__ == "__main__":

    rec_path = '/media/removable/Seagate Expansion Drive/Newan/AA_01 LR'
    s = Stack(rec_path, name='Test stack')

    # Crop and write NRRD
    nrrd_path = cropping.autocrop(s)

    # Segment bony structures
    seg = segment.otsu_threshold(nrrd_path)

    # Create mesh
    vertices, faces = segment.create_mesh(seg)
    m = Mesh(vertices, faces, s.curve, name='Test mesh')

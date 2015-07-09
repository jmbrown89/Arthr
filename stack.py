__author__ = 'james'

import os
import numpy as np
import glob
import tifffile
from image_processing import cropping

class Stack:

    def __init__(self, recon_dir):

        self.recon_dir = recon_dir
        self.dims = [-1, -1, -1]
        self.no_slices = -1
        self.slice_files = []
        self.stack = []

        self.get_slice_files()

    def get_slice_files(self):

        # Find files in recon dir
        self.slice_files = glob.glob(os.path.join(self.recon_dir, '*{}.tif'.format('[0-9]' * 4)))
        self.slice_files = sorted(self.slice_files)

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

    def compute_curvature(self):

        no_blocks = 20
        block_size = self.no_slices / no_blocks
        return NotImplemented


if __name__ == "__main__":

    rec_path = '/media/removable/Seagate Expansion Drive/Newan/AA_01 LR'
    s = Stack(rec_path)

    cropping.autocrop(s)

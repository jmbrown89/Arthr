__author__ = 'james'

import os
import numpy as np
import tifffile
from image_processing import cropping

class Stack:

    def __init__(self, recon_dir):

        self.recon_dir = recon_dir
        self.dims = [-1, -1, -1]
        self.no_slices = -1
        self.exclude = ['.log', '.crv', '.spr.tif', 'spr.bmp']
        self.slice_files = []
        self.stack = []

        self.get_slice_files()

    def get_slice_files(self):

        # Determine whether recon dir is valid
        try:
            recon_files = os.listdir(self.recon_dir)
        except IOError as err:
            print "Invalid recon directory specified: {}".format(err)
            return None

        for file_ in recon_files:

            if any(e in file_ for e in self.exclude) is False:
                self.slice_files.append(os.path.join(self.recon_dir, file_))

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

    rec_path = '/media/removable/Seagate Expansion Drive/Intenso/Wild types - 06012014/S4/newRec'
    s = Stack(rec_path)

    cropping.autocrop(s)

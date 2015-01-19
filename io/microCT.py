__author__ = 'james'

import os
import numpy as np
import SimpleITK as sitk


class Stack:

    def __init__(self, recon_dir):

        self.recon_dir = recon_dir
        self.slice_dims = (-1, -1)
        self.no_slices = -1
        self.exclude = []
        self.slice_files = []
        self.stack = []

    def get_slice_files(self):

        # Determine whether recon dir is valid
        try:
            recon_files = os.listdir(self.recon_dir)
        except IOError as err:
            print "Invalid recon directory specified: {}".format(err)
            return None

        for file_ in recon_files:

            if any(e in file_ for e in self.exclude) is False:
                self.slice_files.append(file_)

        # Get slice dimensions
        self.slice_dims = list(sitk.ReadImage(self.slices[0]).shape)
        self.slice_dims[2] = len(self.slice_files)

    def load_slice_data(self):

        self.stack = np.ndarray(shape=tuple(self.slice_dims), dtype=np.uint16)
        for index, file_ in enumerate(self.slice_files):

            im = sitk.GetArrayFromImage(sitk.ReadImage(file_))
            self.stack[:, :, index] = im

    def write_stack_as_NRRD(self, output_dir):

        output_path = os.path.join(output_dir, self.recon_dir, ".nrrd")
        sitk.WriteImage(self.stack, output_path)

    def compute_curvature(self):

        no_blocks = 20
        block_size = self.no_slices / no_blocks
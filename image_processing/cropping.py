__author__ = 'james'

import SimpleITK as sitk
import numpy as np

class Cropper:

    def __init__(self, file_list, slice_dims):

        self.file_list = file_list
        self.slice_dims = slice_dims
        self.auto_crop()

    def auto_crop(self):

        print "Doing automatic crop"

        for file_ in self.file_list:
            im = sitk.GetArrayFromImage(sitk.ReadImage(file_))
            cb = self.get_cropbox()
            im = im[cb[0], cb[1]]

        return None

    def get_cropbox(self):

        max_p = self.maximum_intensity_projection()
        binary_im = sitk.OtsuThreshold(max_p)

        return None

    def maximum_intensity_projection(self):

        step_size = 10
        sparse_list = self.file_list[::step_size]
        max_im = np.zeros(shape=tuple(self.slice_dims))

        for slice_ in sparse_list:

            im = sitk.GetArrayFromImage(sitk.ReadImage(slice_))
            idx = im > max_im
            max_im[idx] = im[idx]

        return max_im
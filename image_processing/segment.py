__author__ = 'james'

import SimpleITK as sitk

def default_threshold(nrrd_path, lower, upper):
    raise NotImplemented

def otsu_threshold(nrrd_path, min_obj_size=10):

    # Read image
    vol = sitk.ReadImage(nrrd_path)

    # Segment using otsu method
    seg = sitk.OtsuThreshold(vol, 0, 255, 128, False, 1)

    # Clean up
    seg = sitk.ConnectedComponent(seg)
    seg = sitk.RelabelComponent(seg, min_obj_size)

    return seg


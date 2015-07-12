__author__ = 'james'

import numpy as np

import vtk
from vtk.util import numpy_support

from base.error_handling import RegistrationError


# Largely based on this: http://www.vtk.org/Wiki/VTK/Examples/Python/IterativeClosestPoints
def icp(source_points, target_points, mode='rigid', no_iterations=100, threshold=0.01, debug=False):

    # Create VTK objects for source and target points
    source = create_vtk_points(source_points)
    target = create_vtk_points(target_points)

    # Create ICP object and set source and target points
    icp = vtk.vtkIterativeClosestPointTransform()
    icp.SetSource(source)
    icp.SetTarget(target)

    # Turn on debugging to get info
    if debug:
        icp.DebugOn()

    # Set transform type
    if mode == 'rigid':
        icp.GetLandmarkTransform().SetModeToRigidBody()
    elif mode == 'affine':
        icp.GetLandmarkTransform().SetModeToAffine()
    else:
        raise RegistrationError("Invalid registration mode: '{}'".format(mode))

    # Set parameters
    icp.SetMaximumNumberOfIterations(no_iterations)
    icp.SetMaximumMeanDistance(threshold)
    icp.Modified()

    # Run ICP
    icp.Update()

    # Transform the source points
    icp_transform_filter = vtk.vtkTransformPolyDataFilter()
    if vtk.VTK_MAJOR_VERSION <= 5:
        icp_transform_filter.SetInput(source)
    else:
        icp_transform_filter.SetInputData(source)

    icp_transform_filter.SetTransform(icp.GetLandmarkTransform())
    icp_transform_filter.Update()

    # Get transformed points as numpy array
    transformed_source = icp_transform_filter.GetOutput().GetPoints().GetData()
    transformed_source = numpy_support.vtk_to_numpy(transformed_source)

    return icp.GetLandmarkTransform(), transformed_source

def create_vtk_points(point_arr):

    vtk_points = vtk.vtkPoints()
    vtk_vertices = vtk.vtkCellArray()

    # Insert points into vtk object
    for pt in point_arr:
        id = vtk_points.InsertNextPoint(*pt)
        vtk_vertices.InsertNextCell(1)
        vtk_vertices.InsertCellPoint(id)

    # Create vtkPolyData object
    points = vtk.vtkPolyData()
    points.SetPoints(vtk_points)
    points.SetVerts(vtk_vertices)
    if vtk.VTK_MAJOR_VERSION <= 5:
        points.Update()

    return points

if __name__ == '__main__':

    source = np.random.rand(10, 3)
    target = np.random.rand(10, 3)

    T, source_aligned = icp(source, target, mode='rigid')

    print T
    print source_aligned





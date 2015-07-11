__author__ = 'james'

from argparse import ArgumentParser
import yaml
from data_structures import io
from data_structures.stack import Stack, Mesh
from image_processing import cropping, segment, processing
from registration.register import register
import numpy as np
import os

def build_model(model_dict, output_dir):

    # Create directory for processed recons
    processed_dir = os.path.join(output_dir, 'processed')
    mkdir_force(processed_dir)

    # Process input data
    model_path = model_dict['model_path']
    sample_dict = process_inputs(model_dict['input_recons'], processed_dir)

    # Create directory for registration results
    reg_dir = os.path.join(output_dir, 'registration')
    mkdir_force(reg_dir)

    # Register inputs
    register_inputs(model_path, sample_dict, reg_dir)

    # TODO Label registered samples

    # TODO Invert registrations

    # TODO Compute statistical shape models


def register_inputs(model_path, sample_dict, reg_dir):

    # Register model to input samples
    for sample_name, sample in sample_dict.values():

        # Load model
        model = io.load_model(model_path)

        # Create registration directory
        reg_dir = os.path.join(reg_dir, sample_name)

        # Register model with sample
        registered_model = register(model, sample)

        # Save registered model
        io.save_model(registered_model, reg_dir)

def label_inputs():
    pass

def process_inputs(input_recons, processed_dir, force=True):

    sample_dict = {}
    for recon_name, recon_dir in input_recons.items():

        # Create directory within processed directory
        out_dir = os.path.join(processed_dir, recon_name)

        # If the directory does not exist, or force is True
        if not os.path.isdir(out_dir) or force:
            mkdir_force(out_dir)

        # Create stack and compute curvature
        stack = Stack(recon_dir, name=recon_name)
        curve = processing.compute_curvature(stack)
        np.save(os.path.join(out_dir, 'curve.npy'), curve)

        # Crop volume
        cropped_path = cropping.autocrop(stack, out_dir)

        # Segment and generate mesh
        seg = segment.otsu_threshold(cropped_path)
        vertices, faces = processing.create_mesh(seg)
        m = Mesh(vertices, faces)
        ply_path = m.write_ply(out_dir)

        # Append to dict
        sample_dict[recon_name] = ply_path

    return sample_dict

def mkdir_force(dir_name):

    try:
        os.mkdir(dir_name)
    except OSError:
        os.rmdir(dir_name)
        os.mkdir(dir_name)

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--inputs', '-i', dest='config', help='.yaml file with list of input recons', required=True)
    args = parser.parse_args()

    # Load from yaml file
    with open(args.config) as conf:
        yaml_dict = yaml.load(conf)

    # Process recons
    build_model(yaml_dict, os.path.dirname(os.path.abspath(args.config)))

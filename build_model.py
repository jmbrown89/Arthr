__author__ = 'james'

from argparse import ArgumentParser
import yaml
from data_structures.stack import Stack, Mesh
from image_processing import cropping, segment, processing
import os

def build_model(model_dict, model_path):

    # Create directory for processed recons and process
    try:
        processed_dir = os.path.mkdir(model_path, 'processed')
    except OSError:
        print 'Processed directory already exists!'
        return

    process_inputs(model_dict['input_recons'], processed_dir)

def process_inputs(input_recons, processed_dir, force=True):

    # For each recon in the list
    for recon_name, recon_dir in input_recons.items():

        # Create directory within processed directory
        out_dir = os.path.join(processed_dir, recon_name)

        if not os.path.isdir(out_dir) or force:
            mkdir_force(out_dir)

        # Create stack
        s = Stack(recon_dir, name=recon_name)

        # Crop volume
        cropped_path = cropping.autocrop(s, out_dir)

        # Segment and generate mesh
        seg = segment.otsu_threshold(cropped_path)
        vertices, faces = segment.create_mesh(seg)
        m = Mesh(vertices, faces, s.compute_curvature())
        m.write_ply()


def mkdir_force(dir):

    try:
        os.path.mkdir(dir)
    except OSError:
        os.rmdir(dir)
        os.path.mkdir(dir)

if __name__ == "__init__":

    parser = ArgumentParser()
    parser.add_argument('--inputs', '-i', dest='config', help='.yaml file with list of input recons')
    args = parser.parse_args()

    # Load from yaml file
    with open(args.config) as conf:
        model_dict = yaml.load(conf)

    # Process recons
    build_model(model_dict, os.path.dirname(args.config))

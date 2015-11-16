__author__ = 'james'

from argparse import ArgumentParser
import yaml
from scipy.io import loadmat
import pandas as pd
from pandas import Series, DataFrame
import seaborn as sns
from os.path import join

BONE_NAMES = ''


def plot_areas(model_name, area_dict, output_dir):

    # For each sample
    cols = ('Sample no.', 'Legend', '% surface area', 'group')
    df = DataFrame(columns=cols)

    i = 0
    for sample_name, areas_file in area_dict.iteritems():

        # Attempt to load MATLAB file
        mat = loadmat(areas_file['path'])

        # Per sample data
        totalErosion = (surface_area(mat['measuredErosions'][0]) / surface_area(mat['totalArea'][0])) * 100
        totalFormation = (surface_area(mat['measuredGrowths'][0]) / surface_area(mat['totalArea'][0])) * 100

        # Add rows to data frame
        group = areas_file.setdefault('group', None)
        df.loc[i] = [sample_name, 'erosion', totalErosion, group]
        df.loc[i+1] = [sample_name, 'formation', totalFormation, group]
        i += 2

    # Plot
    plot_samples(df, model_name, join(output_dir, model_name + '.png'))


def plot_samples(df, title, out_path):

    g = sns.factorplot(x="Sample no.", y="% surface area", hue="Legend", data=df,
                       size=6, kind="bar", palette=[sns.xkcd_rgb["denim blue"], sns.xkcd_rgb["pale red"], ])
    sns.plt.title(title)
    sns.plt.savefig(out_path, bbox_inches='tight')


def surface_area(values):

    total_area = 0
    for item in values:
        total_area += sum(lesion[0] for lesion in item)
    return total_area


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-i', '--input', dest='results', required=True)
    args = parser.parse_args()

    with open(args.results, 'rb') as r:
        result_dict = yaml.load(r)

    # Loop through arthritis models
    output_dir = result_dict['output_dir']
    BONE_NAMES = result_dict['bone_names']

    for model, areas in result_dict['results'].iteritems():
        plot_areas(model, areas, output_dir)

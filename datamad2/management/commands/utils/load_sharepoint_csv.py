# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '20 Nov 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import pandas as pd


def load_sharepoint_csv(filename):
    """

    :param filename: CSV file to load
    :return: pandas DataFrame
    """

    # Load file
    df = pd.read_csv(filename, header=0, skipinitialspace=True)

    # Transform columns
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '') \
        .str.replace(')', '').str.replace('?', '').str.replace('/', '_').str.replace('\'', '') \
        .str.replace('-', '')

    return df
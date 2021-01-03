import os

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

import numpy as np

import seamless as ss


def load_buildings_data():
    path = os.path.join(ss.paths.seamless_data_dir(), 'dissertation', 'san_fran_buildings.pkl')
    df = ss.io.read_pickle(path)
    return df


def load_buildings_json():
    path = os.path.join(ss.paths.seamless_data_dir(), 'dissertation', 'san_fran_json_resp.json')
    json = ss.io.read_json(path)
    return json


def plot_locations():
    df = load_buildings_data()
    plt.scatter(df['longlitude'], df['latitude'], s=0.01)
    plt.show()


def plot_shapes():
    json = load_buildings_json()
    for j in near:
        x = np.array(j['geometry']['coordinates'][0][0])
        if x[0][0] > -122.44 and x[0][1] > 37.76:
            plt.plot(x[:, 0], x[:, 1], linewidth=0.5)
    plt.show()

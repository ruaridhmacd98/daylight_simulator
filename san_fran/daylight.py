import os
import math

import numpy as np

import seamless as ss
from san_fran import city_model
from ddf import DDF


BUILDINGS_RADIUS_CUTOFF = 300


def get_centre_of_building(b):
    coords = np.array(b['geometry']['coordinates'][0][0])
    return coords[:, 0].mean(), coords[:, 1].mean()


def get_distance_between_two_points(la1, lo1, la2, lo2):
    RADIUS_OF_EARTH = 6371000.
    constant = RADIUS_OF_EARTH * math.pi / 180.
    return constant * ((la2 - la1) ** 2 + (lo2 - lo1) ** 2) ** 0.5


def is_building_near(lat, lon, b):
    b_lo, b_la = get_centre_of_building(b)
    distance = get_distance_between_two_points(lat, lon, b_la, b_lo)
    return distance < BUILDINGS_RADIUS_CUTOFF


def get_nearby_buildings(lat, lon, buildings):
    output = []
    for b in buildings:
        if is_building_near(lat, lon, b):
            output.append(b)
    return output


def get_polar_coords(lat, lon, b):
    coords = np.array(b['geometry']['coordinates'][0][0])
    rads = []
    phis = []
    for c in coords:
        r = get_distance_between_two_points(lon, lat, c[0], c[1])
        phi = get_phi_of_point(lon, lat, c[0], c[1])
        rads.append(r)
        phis.append(phi)
    rads = np.array(rads)
    phis = np.array(phis)
    return {'distance': rads.mean(), 'phi_min': phis.min(), 'phi_max': phis.max()}


def get_phi_of_point(lon, lat, b_lon, b_lat):
    delta_x = b_lon - lon
    delta_y = b_lat - lat
    phi = np.arctan2(delta_y, delta_x)
    if delta_y < 0:
        phi = phi + 2 * math.pi
    return phi


def get_buildings_polar_coords(lat, lon, buildings):
    output = []
    for b in buildings:
        polar = get_polar_coords(lat, lon, b)
        polar['height'] = b['properties']['height']
        output.append(polar)
    df = DDF(output)
    df = _drop_itself(df)
    return df


def _drop_itself(df):
    drop_ix = df['distance'] == df['distance'].min()
    return df.drop_rows(drop_ix)


def get_buildings_in_direction(phi, df):
    ix = []
    for row in df.iterrows():
        span_zero = row['phi_max'][0] - row['phi_min'][0] > math.pi
        between_points = row['phi_min'][0] <= phi <= row['phi_max'][0]
        if between_points and not span_zero:
            ix.append(True)
        elif span_zero and not between_points:
            ix.append(True)
        else:
            ix.append(False)
    return df.rowslice(ix)


if __name__ == '__main__':
    json = city_model.load_buildings_json()
    buildings = json['features']

    path = os.path.join(ss.paths.seamless_data_dir(), 'dissertation', 'full_worksheet_repeat_sales.pkl')
    offices = ss.io.read_pickle(path)

    df = offices[offices['Market'] == 'San Francisco']
    for office in df.head(1).iterrows():
        lat = office['latitude']
        lon = office['longlitude']
        nearby = get_nearby_buildings(lat, lon, buildings)
        polar = get_buildings_polar_coords(lat, lon, nearby)

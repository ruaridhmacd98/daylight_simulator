import pytest
import math

from san_fran import daylight
from ddf import DDF

TEST_ANGLES = [
    (5, 5, 6, 5, 0),
    (5, 5, 5, 6, math.pi / 2),
    (5, 5, 4, 5, math.pi),
    (5, 5, 5, 4, 3. * math.pi / 2),
]


@pytest.mark.parametrize('lon, lat, b_lon, b_lat, phi', TEST_ANGLES)
def test_get_phi_for_point(lon, lat, b_lon, b_lat, phi):
    res = daylight.get_phi_of_point(lon, lat, b_lon, b_lat)
    assert res == phi


def test_get_buildings_in_certain_direction():
    buildings = DDF({
        'phi_min': [2, 2.1, 1.5, 0.05],
        'phi_max': [2.1, 2.2, 2.15, 6.18],
    })
    res = daylight.get_buildings_in_direction(2.05, buildings)
    expected = DDF({
        'phi_min': [2, 1.5],
        'phi_max': [2.1, 2.15],
    })
    assert res.equals(expected)


def test_get_buildings_in_certain_direction_around_zero():
    buildings = DDF({
        'phi_min': [0.05],
        'phi_max': [6.18],
    })
    res = daylight.get_buildings_in_direction(0.01, buildings)
    expected = DDF({
        'phi_min': [0.05],
        'phi_max': [6.18],
    })
    assert res.equals(expected)

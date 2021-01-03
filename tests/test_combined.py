from ddf import DDF
from hedonic import combined


def test_add_height_relative_to_others():
    df = DDF({
        'number_of_stories': [5, 2, 1, 5, 3],
        'average_surrounding_building_heights': [5, 6, 1, 5, 1],
        'number_of_buildings_in_city': [1, 2, 1, 1, 2],
    })
    expected = DDF({
        'number_of_stories': [5, 2, 1, 5, 3],
        'average_surrounding_building_heights': [5, 6, 1, 5, 1],
        'number_of_buildings_in_city': [1, 2, 1, 1, 2],
        'relative_height': [5, -4, 1, 5, 2],
    })
    output = combined.add_height_relative_to_others(df)
    assert expected.equals(output)

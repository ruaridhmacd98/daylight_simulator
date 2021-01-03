import numpy as np

from ddf import DDF
from hedonic import datasets


def test_clean_rent():
    df = DDF({'rent': ['$26.57/fs', '-', '$24.92/+util']})
    expected = DDF({'rent': [26.57, np.nan, 24.92]})
    output = datasets.clean_rent(df)
    assert expected.equals(output)


def test_drop_rows_with_missing_rent():
    df = DDF({'rent': [26.57, np.nan, 24.92, 550.35]})
    expected = DDF({'rent': [26.57, 24.92]})
    output = datasets.drop_rows_with_missing_rent(df)
    assert expected.equals(output)

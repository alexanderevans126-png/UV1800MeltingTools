from uv1800meltingtools.concentration import concentration_series
from uv1800meltingtools.extinctioncoeff import epsilon_nn


def test_concentration_series_length():
    values = concentration_series(592540, 5)
    assert len(values) == 5


def test_concentration_series_values():
    values = concentration_series(592540, 5)
    assert values == [0.675, 0.983, 1.432, 2.086, 3.038]


def test_extinction_coefficient_dna():
    eps = epsilon_nn("ATGC", molecule="DNA")
    assert eps == 39760
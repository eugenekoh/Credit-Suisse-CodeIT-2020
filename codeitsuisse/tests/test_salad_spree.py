import pytest

from codeitsuisse.routes.salad_spree import salad_spree


@pytest.mark.parametrize(
    "n,streets,expected",
    (
            (3, [["12", "12", "3", "X", "3"], ["23", "X", "X", "X", "3"], ["33", "21", "X", "X", "X"],
                 ["9", "12", "3", "X", "X"], ["X", "X", "X", "4", "5"]], 24),
            (3, [["X", "X", "2"], ["2", "3", "X"], ["X", "3", "2"]], 0),
            (2, [["2", "3", "X", "2"], ["4", "X", "X", "4"], ["3", "2", "X", "X"], ["X", "X", "X", "5"]], 5)
    )
)
def test_salad_spree(n, streets, expected):
    assert salad_spree(n, streets) == expected

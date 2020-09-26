import pytest
from codeitsuisse.routes.revisit_geometry import revisit_geometry


@pytest.mark.parametrize(
    "input,output",
    (
            ({
                 "shapeCoordinates": [
                     {"x": 21, "y": 70},
                     {"x": 72, "y": 70},
                     {"x": 72, "y": 127}
                 ],
                 "lineCoordinates": [
                     {"x": -58, "y": 56},
                     {"x": -28, "y": 68}
                 ]
             }, [
                 {"x": 72, "y": 108},
                 {"x": 45.52, "y": 97.41}
             ]
            ),
            ({
                 "shapeCoordinates": [
                     {"x": -21, "y": -18},
                     {"x": 71, "y": -18},
                     {"x": 71, "y": 71},
                     {"x": -21, "y": 71}
                 ],
                 "lineCoordinates": [
                     {"x": 68, "y": -8},
                     {"x": 108, "y": 42}
                 ]
             },
             [
                 {"x": 60, "y": -18},
                 {"x": 71, "y": -4.25}
             ]

            ),
            (
                    {
                        "shapeCoordinates": [
                            {
                                "x": 63,
                                "y": 26
                            },
                            {
                                "x": 115,
                                "y": 26
                            },
                            {
                                "x": 115,
                                "y": 54
                            },
                            {
                                "x": 63,
                                "y": 54
                            }
                        ],
                        "lineCoordinates": [
                            {
                                "x": -88,
                                "y": 85
                            },
                            {
                                "x": -58,
                                "y": 97
                            }
                        ]
                    },
                    []
            )
    )
)
def test_revisit_geometry(input, output):

    sort_func = lambda pt: (pt["x"], pt["y"])
    result = sorted((d["x"], d["y"]) for d in revisit_geometry(input))
    output = sorted((d["x"], d["y"]) for d in output)
    assert len(result) == len(output)
    for a, b in zip(result, output):
        assert a[0] == b[0]
        assert a[1] == b[1]


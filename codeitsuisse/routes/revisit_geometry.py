import logging
import json

from flask import request
import sympy

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/revisitgeometry', methods=['POST'])
def evaluate_revisit_geometry():
    data = request.get_json()
    result = revisit_geometry(data)

    logging.info("data sent for evaluation {}".format(data))
    logging.info("result :{}".format(result))

    return json.dumps(result)


def revisit_geometry(json_data):
    """
    https://cis2020-revisit-geometry.herokuapp.com/instructions

    Wrapper around revisit_geometry

    :param json_data: raw json data
    :rtype: dict
    """

    # parse data
    shape_coord = json_data["shapeCoordinates"]
    shape_coord = [(d["x"], d["y"]) for d in shape_coord]

    line_coord = json_data["lineCoordinates"]
    line_coord = [(d["x"], d["y"]) for d in line_coord]

    # sympy logic
    polygon = sympy.Polygon(*shape_coord)
    line = sympy.Line(*line_coord)

    intersections = polygon.intersection(line)

    json_results = [{"x": round(float(pt.x), 2), "y": round(float(pt.y), 2)} for pt in intersections]
    return json_results

import logging

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/yin-yang', methods=['POST'])
def evaluate_yy():
    """
    {
        "number_of_elements" : n,
        "number_of_operations" : k,
        "elements" :  E,
    }
    :return:
    """

    data = request.get_json()
    logger.info(f"yin-yang data: {data}")
    n = data["number_of_elements"]
    k = data["number_of_operations"]
    elements = data["number_of_operations"]

    result = None
    return jsonify(result)

import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/driverless-car', methods=['POST'])
def evaluate_driverless_car():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = {}
    logging.info("result :{}".format(results))

    return jsonify(results)



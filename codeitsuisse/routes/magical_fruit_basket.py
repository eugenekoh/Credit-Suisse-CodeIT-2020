import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    weightApple = 11
    weightWatermelon = 22
    weightBanana = 42
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    
    sumFruits = weightApple * 1 + weightWatermelon * 2 + weightBanana * 3


    return jsonify(sumFruits)
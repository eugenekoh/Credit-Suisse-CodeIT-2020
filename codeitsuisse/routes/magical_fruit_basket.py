import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    weightApple = 950
    weightWatermelon = 1112
    weightBanana = 1333
    data = request.get_json()
    apple = data["maApple"]
    watermelon = data["maWatermelon"]
    banana = data["maBanana"]
    logging.info("data sent for evaluation {}".format(data))
    
    sumFruits = weightApple * apple + weightWatermelon * watermelon + weightBanana * banana


    return jsonify(sumFruits)
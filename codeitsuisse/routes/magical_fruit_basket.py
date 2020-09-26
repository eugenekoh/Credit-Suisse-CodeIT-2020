import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    weightApple = 900
    weightWatermelon = 1112
    weightBanana = 1333
    data = ast.literal_eval(request.get_data())
    jsonData = json.loads(data)
    apple = jsonData["maApple"]
    watermelon = jsonData["maWatermelon"]
    banana = jsonData["maBanana"]
    logging.info("data sent for evaluation {}".format(data))
    
    sumFruits = weightApple * apple + weightWatermelon * watermelon + weightBanana * banana


    return jsonify(sumFruits)
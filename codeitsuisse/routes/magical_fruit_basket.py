import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    weight1 = 900
    weight2 = 1112
    weight3 = 1333
    data = request.get_data(as_text=True)
    jsonData = json.loads(data)
    apple = jsonData.get("maRamubutan",0)
    watermelon = jsonData.get("maApple",0)
    banana = jsonData.get("maWatermelon",0)
    logging.info("data sent for evaluation {}".format(data))
    
    sumFruits = weight1 * apple + weight2 * watermelon + weight3 * banana


    return jsonify(sumFruits)
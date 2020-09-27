import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# GLOBAL VARIABLES
WEIGHT_1 = 900
WEIGHT_2 = 1112
WEIGHT_3 = 1333

FRUIT_1 = "maPomegranate"
FRUIT_2 = "maPineapple"
FRUIT_3 = "maWatermelon"

@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruitbasket():
    data = request.get_data(as_text=True)
    jsonData = json.loads(data)
    fruit1 = jsonData.get(FRUIT_1,0)
    fruit2 = jsonData.get(FRUIT_2,0)
    fruit3 = jsonData.get(FRUIT_3,0)
    logging.info("data sent for evaluation {}".format(data))
    
    sumFruits = WEIGHT_1 * fruit1 + WEIGHT_2 * fruit2 + WEIGHT_3 * fruit3

    return jsonify(sumFruits)

@app.route('/fruitbasket-set', methods=['POST'])
def evaluate_fruit_basket_set():
    data = request.get_json()
    global WEIGHT_1, WEIGHT_2, WEIGHT_3, FRUIT_1, FRUIT_2, FRUIT_3
    WEIGHT_1 = data["weight_1"]
    WEIGHT_2 = data["weight_2"]
    WEIGHT_3 = data["weight_3"]
    FRUIT_1 = data["fruit_1"]
    FRUIT_2 = data["fruit_2"]
    FRUIT_3 = data["fruit_3"]

    return jsonify({
        "message": f"weights: {FRUIT_1} - {WEIGHT_1}, {FRUIT_2} - {WEIGHT_2}, {FRUIT_3} - {WEIGHT_3}"
    })

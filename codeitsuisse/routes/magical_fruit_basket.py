import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

# GLOBAL VARIABLES
WEIGHT_APPLE = 900
WEIGHT_WATERMELON = 1112
WEIGHT_BANANA = 1333


@app.route('/fruitbasket', methods=['POST'])
def evaluate_fruit_basket():
    data = request.get_data(as_text=True)
    jsonData = json.loads(data)
    apple = jsonData.get("maApple", 0)
    watermelon = jsonData.get("maWatermelon", 0)
    banana = jsonData.get("maBanana", 0)
    logging.info(f"fruit-basket data:{data}")
    logging.info(f"weights: apple - {WEIGHT_APPLE}, watermelon - {WEIGHT_WATERMELON}, banana - {WEIGHT_BANANA}")

    sumFruits = WEIGHT_APPLE * apple + WEIGHT_WATERMELON * watermelon + WEIGHT_BANANA * banana

    return jsonify(sumFruits)


@app.route('/fruitbasket-set', methods=['POST'])
def evaluate_fruit_basket_set():
    data = request.get_json()
    global WEIGHT_BANANA, WEIGHT_APPLE, WEIGHT_WATERMELON
    WEIGHT_APPLE = data["apple"]
    WEIGHT_WATERMELON = data["watermelon"]
    WEIGHT_BANANA = data["banana"]

    return jsonify({
        "message": f"weights: apple - {WEIGHT_APPLE}, watermelon - {WEIGHT_WATERMELON}, banana - {WEIGHT_BANANA}"
    })

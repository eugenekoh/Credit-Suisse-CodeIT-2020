import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

@app.route('/sort', methods=['POST'])
def evaluateSort():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    data.sort()
    logging.info("My result :{}".format(data))
    return json.dumps(data)




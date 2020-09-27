import logging
from flask import request, jsonify
from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/pre-tick', methods=['POST'])
def evaluate_pre_tick():
    data = request.get_json()
    logger.info(f"data: {data}")
    result = {}

    return jsonify(result)

import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

import heapq

logger = logging.getLogger(__name__)

@app.route('/contact_trace', methods=['POST'])
def evaluate_contact_tracing():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    infected = data.get("infected")
    origin = data.get("origin")
    cluster = data.get("cluster")
    infectedName = infected.get("name")
    infectedGenome = infected.get("genome").split("-")
    originName = origin.get("name")
    originGenome = origin.get("genome").split("-")
    response = []
    if infectedGenome == originGenome:
        s = "{} -> {}".format(infectedName, originName)
        response.append(s)
    for node in cluster:
        clusterGenome = node.get("genome").split("-")
        clusterName = node.get("name")
        if clusterGenome == infectedGenome:
            s = "{} -> {}".format(infectedName, clusterName)
            response.append(s)

    logging.info("My result :{}".format(response))
    return jsonify(response)




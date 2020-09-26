# def bucket_fill():


# class Circle():


# class Bucket():


# class Pipe():

import xml.etree.ElementTree as ET
import re
import logging
import json
from flask import request, jsonify
import xmltodict


from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/bucket-fill', methods=['POST'])
def evaluate_bucket_fill():
    image = xmltodict.parse(request.data)
    output = bucket_fill(image["svg"]["circle"], image["svg"]["polyline"])
    return

# def bucket_fill(circles, polylines):


# def generateGraph(circles, polylines):
    

# <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1024" height="1024">
#     <circle cx="500" cy="0" r="1" stroke="blue" fill="none" />
#     <polyline fill="none" stroke="black" points="360,175 360,225 400,225 400,175" />
#     <polyline fill="none" stroke="black" points="480,5 480,40 520,40 520,5" />
#     <polyline fill="none" stroke="black" points="500,50 400,150" />
# </svg>
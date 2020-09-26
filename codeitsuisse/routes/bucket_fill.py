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
import sys

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/bucket-fill', methods=['POST'])
def evaluate_bucket_fill():
    image = xmltodict.parse(request.data)
    output = bucket_fill(image["svg"]["circle"], image["svg"]["polyline"])
    response = {}
    response["result"] = int(output)
    return jsonify(response)

def bucket_fill(circles, polylines):
    waterXArr = []
    for water in circles:
        waterXArr.append(int(water["@cx"]))
    # waterY = int(circles["@cy"])
    buckets = []
    coordRanges = []
    pipesX = []
    for bucket in polylines:
        points = bucket["@points"].split(" ")
        # means is a pipe
        if len(points) == 2:
            x1 = points[0].split(",")
            x2 = points[1].split(",")
            x = [int(x1[0]), int(x2[0])]
            x.sort()
            pipesX.append(x)
            continue
        # else is bucket, calculate area
        xArr = []
        yArr = []
        yTop = 0
        for p in points:
            coord = p.split(",")
            x, y = int(coord[0]), int(coord[1])
            xArr.append(x)
            yArr.append(y)
            yTop = max(y, yTop)
        topRange = []
        btmRange = []
        for i in range(len(xArr)):
            if yArr[i] == yTop:
                topRange.append(xArr[i])
            else:
                btmRange.append(xArr[i])
        xArr.sort()
        yArr.sort()
        topRange.sort()
        btmRange.sort()
        bigArea = (xArr[-1] - xArr[0]) * (yArr[-1] - yArr[0])
        smallArea = (1/2 * (xArr[1]-xArr[0])*(yArr[-1] - yArr[0])) + (1/2* (xArr[-1]-xArr[-2])*(yArr[-1] - yArr[0]))
        area = bigArea - smallArea
        
        coordRange = [topRange, btmRange]
        bucket = {}
        bucket["area"] = area
        bucket["ranges"] = coordRange
        coordRanges.append(coordRange)
        buckets.append(bucket)
    # TODO: get rid of overlapping buckets
    areas = 0
    # remove overlapping buckets
    for i in range(len(buckets)):
        if buckets[i]["ranges"] not in coordRanges:
            del buckets[i]
            continue
    
    ## create graph from pipes start with waterX
    ## DFS via x coordinates only
    for waterX in waterXArr:
        stack = []
        for i in range(len(buckets)):
            bucketRange = buckets[i]["ranges"]
            if bucketRange[0][0] <= waterX <= bucketRange[0][1]:
                areas += buckets[i]["area"]
                stack.append((bucketRange[1][0], bucketRange[1][1]))
                del buckets[i]
                break
        while stack:
            bucketRange = stack.pop()
            btmPipe = 0
            found = False
            for i in range(len(pipesX)):
                btmPipe = pipesX[i][1]
                if bucketRange[0] <= pipesX[i][0] <= bucketRange[1]:
                    found = True
                    del pipesX[i]
                    break
                elif bucketRange[0] <= pipesX[i][1] <= bucketRange[1]:
                    found = True
                    btmPipe = pipesX[i][0]
                    del pipesX[i]
                    break
            if found:
                for i in range(len(buckets)):
                    bucketRange = buckets[i]["ranges"]
                    if bucketRange[0][0] <= btmPipe <= bucketRange[0][1]:
                        areas += buckets[i]["area"]
                        stack.append((bucketRange[1][0], bucketRange[1][1]))
                        del buckets[i]
                        break
    return areas



        


            



    


# def generateGraph(circles, polylines):
    

# <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1024" height="1024">
#     <circle cx="500" cy="0" r="1" stroke="blue" fill="none" />
#     <polyline fill="none" stroke="black" points="360,175 360,225 400,225 400,175" />
#     <polyline fill="none" stroke="black" points="480,5 480,40 520,40 520,5" />
#     <polyline fill="none" stroke="black" points="500,50 400,150" />
# </svg>
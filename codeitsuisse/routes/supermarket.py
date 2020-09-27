import logging
import json
import sys

from flask import request, jsonify;

from collections import deque 

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/supermarket', methods=['POST'])
def evaluate_supermarket():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    test = data.get("tests")
    response = {}
    response["answers"] = {}
    for key,value in test.items():
        maze = value.get("maze")
        start = value.get("start")
        end = value.get("end")
        ans = find_supermarket(maze, start, end)
        response["answers"][key] = ans
    
    return jsonify(response)

def find_supermarket(maze, start, end):
    # bfs
    queue = deque()
    start.append(1)
    queue.append(start)
    print(len(maze))
    print(len(maze[0]))
    while queue:
        j, i, level = queue.popleft()
        for x, y in ((1,0), (-1,0), (0,1), (0,-1)):
            row, col = i+x, y+j
            if row < 0 or col < 0 or row >= len(maze) or col >= len(maze[0]):
                continue
            if row == end[1] and col == end[0]:
                return level + 1
            if maze[row][col] == 0:
                maze[row][col] = -1
                appendQ = (col, row, level+1)
                queue.append(appendQ)
    return -1

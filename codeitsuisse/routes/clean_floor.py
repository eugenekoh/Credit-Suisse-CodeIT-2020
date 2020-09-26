import logging
import json

from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/clean_floor', methods=['POST'])
def evaluate_clean_floor():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    results = {"answers":{}}
    for test_num in data['tests']:
        results['answers'][test_num] = clean_floor(data['tests'][test_num]["floor"])
    logging.info("result :{}".format(results))

    return json.dumps(results)

def clean_floor(arr):
    firstNonZero = 0
    lastNonZero = len(arr)-1

    while lastNonZero >= 0:
        if arr[lastNonZero] != 0:
            break
        lastNonZero -= 1
    moves = 0
    currPos = 0
    direction = 0
    while firstNonZero != lastNonZero:
        # print(direction,currPos,firstNonZero,lastNonZero)
        # print(arr)
        # print("=====")
        if direction == 0:
            moves += (lastNonZero-currPos)
            for i in range(currPos+1,lastNonZero+1):
                if arr[i] > 0:
                    arr[i] -= 1
                elif arr[i] == 0:
                    arr[i] += 1
            currPos = lastNonZero
            while arr[firstNonZero] == 0 and firstNonZero < lastNonZero:
                firstNonZero += 1
            direction = 1
        elif direction == 1:
            moves += (currPos - firstNonZero)
            for i in range(currPos-1,firstNonZero-1,-1):
                if arr[i] > 0:
                    arr[i] -= 1
                elif arr[i] == 0:
                    arr[i] += 1
            currPos = firstNonZero
            while arr[lastNonZero] == 0 and firstNonZero < lastNonZero:
                lastNonZero -= 1
            direction = 0
        

    if arr[firstNonZero] % 2 == 0:
        moves += 2*arr[firstNonZero]
    else:
        moves += 2*arr[firstNonZero]+1
    # print(moves)
    return moves

# arr = [1,2,0,1]
# clean_floor(arr)
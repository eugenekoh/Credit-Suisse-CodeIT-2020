import logging
import json
import sys

from flask import request, jsonify;

from codeitsuisse import app;


logger = logging.getLogger(__name__)

@app.route('/social_distancing', methods=['POST'])
def evaluate_social_distance():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    test = data.get("tests")
    response = {}
    response["answers"] = {}
    for key,value in test.items():
        seats = value.get("seats")
        people = value.get("people")
        spaces = value.get("spaces")
        ans = find_social_distance(seats, people, spaces)
        response["answers"][key] = ans
    
    return jsonify(response)

def find_social_distance(seats, people, spaces):
    ans = 0    
    seatArr = [False] * seats
    def backtrack(seatsLeft, peopleLeft, spaces, arr, i):
        if peopleLeft == 0:
            nonlocal ans
            ans += 1
            return
        if seatsLeft <= 0:
            return
        minusSeat = 1
        arr[i] = True
        for j in range(i+1, i+1+spaces):
            if j < seats:
                arr[j] = False
                minusSeat += 1
        backtrack(seatsLeft-minusSeat, peopleLeft-1, spaces, arr, i+minusSeat)
        minusSeat = 1
        arr[i] = False
        backtrack(seatsLeft-minusSeat, peopleLeft, spaces, arr, i+minusSeat)
    backtrack(seats, people, spaces, seatArr, 0)
    return ans

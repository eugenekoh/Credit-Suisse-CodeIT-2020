import logging
import json

from flask import request

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/salad-spree', methods=['POST'])
def evaluate_salad_spree():
    data = request.get_json()
    result = salad_spree_json(data)

    logging.info("data sent for evaluation {}".format(data))
    logging.info("result :{}".format(result))

    return json.dumps(result)


def salad_spree_json(json_data):
    """
    https://cis2020-salad-spree.herokuapp.com/

    Wrapper around salad_spree

    :param json_data: raw json data
    :rtype: dict
    """
    n = json_data["number_of_salads"]
    streets = json_data["salad_prices_street_map"]

    result = {"result": salad_spree(n, streets)}
    return result


def salad_spree(n, streets):
    """
    :param n:
    :param street:
    :return:
    """

    # stores sum of minimum sum sublist found so far
    min_window = float('inf')

    for street in streets:
        # splice arrays by X character
        sub_arrays = []
        tmp = []
        for num in street:
            if num == "X" and tmp:
                sub_arrays.append(tmp)
                tmp = []
            elif num != "X":
                tmp.append(int(num))

        # remainder
        if tmp:
            sub_arrays.append(tmp)

        for arr in sub_arrays:
            if len(arr) < n:
                continue

            # stores sum of element in current window
            window_sum = 0

            for i in range(len(arr)):
                # add current element to the window
                window_sum += arr[i]

                # if window size is more than equal to n
                if i + 1 >= n:
                    # update minimum sum window
                    min_window = min(min_window, window_sum)

                    # remove leftmost element from the window
                    window_sum -= arr[i + 1 - n]

    return min_window if min_window != float('inf') else 0

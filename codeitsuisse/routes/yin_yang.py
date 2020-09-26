import logging
import math

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/yin-yang', methods=['POST'])
def evaluate_yy():
    """
    {
        "number_of_elements" : n,
        "number_of_operations" : k,
        "elements" :  E,
    }
    :return:
    """

    data = request.get_json()
    logger.info(f"yin-yang data: {data}")
    n = data["number_of_elements"]
    k = data["number_of_operations"]
    elements = data["elements"]

    s = Solution()
    result = s.yy(elements, k)

    return jsonify(result)


class Solution:
    def __init__(self):
        self.memo = {}

    def yy(self, elem, k):
        branches = math.ceil(len(elem) / 2)

        # check memo
        if elem in self.memo:
            return self.memo[elem]

        # base case
        if k == 0:
            return 0

        # recursive
        expected_yang = 0
        for i in range(branches):

            # choose most rational decision
            left_elem = elem[:i] + elem[i + 1:]
            left_yang = self.yy(left_elem, k - 1)
            if elem[i] == "Y":
                left_yang += 1

            right = len(elem) - 1 - i
            right_elem = elem[:right] + elem[right + 1:]
            right_yang = self.yy(right_elem, k - 1)
            if elem[right] == "Y":
                right_yang += 1

            # add expectation from this branch
            max_yang = max(left_yang, right_yang)
            if i == branches - 1:
                expected_yang += max_yang * 1 / branches
            else:
                expected_yang += max_yang * 2 / branches

        # keep solution to current search node
        if elem not in self.memo:
            self.memo[elem] = expected_yang

        return expected_yang
